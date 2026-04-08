"""Q8: Is the structure consistent across different model architectures?

Probe: Run BitDiscovery on multiple extractor backends (SAE, VQ-VAE,
standard triadic) and compare the discovered structures. If duals, deps,
and hierarchy are consistent across architectures, the structure is
more likely intrinsic to the task than an artifact of one architecture.

Cross-model mode (--checkpoints_v8): Compare the same TriadicExtractor
across two different base models (e.g. v8 GPT-2 Medium vs v9 GPT-Neo 125M).
This tests whether triadic structure is intrinsic to the task/ontology
rather than an artifact of one specific backbone.

Requiere: pip install reptimeline
Usage:
  # Multi-extractor mode (original):
  python q8_probe_crossarch.py --checkpoints_triadic <dir>
  # Cross-model mode (v8 vs v9):
  python q8_probe_crossarch.py --checkpoints <v9_dir> --checkpoints_v8 <v8_dir>
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import argparse
import json
import math
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(SCRIPT_DIR, 'results')
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))
STATS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'stats'))
MODEL_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'model'))
sys.path.insert(0, STATS_DIR)
sys.path.insert(0, MODEL_DIR)

from registry import register_pvalue

try:
    from reptimeline import BitDiscovery
    from triadic_extractor import TriadicExtractor
    HAS_REPTIMELINE = True
except ImportError:
    HAS_REPTIMELINE = False

# Try optional extractor backends
try:
    from reptimeline.extractors import SAEExtractor
    HAS_SAE = True
except ImportError:
    HAS_SAE = False

try:
    from reptimeline.extractors import VQVAEExtractor
    HAS_VQVAE = True
except ImportError:
    HAS_VQVAE = False


# ######################################################################
#  SECTION 0: DATA LOADING
# ######################################################################

with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
    prim_data = json.load(f)

prims = prim_data['primitivos']
bit_to_name = {p.get('bit'): p['nombre'] for p in prims if p.get('bit') is not None}


# ######################################################################
#  SECTION 1: COMPARISON METRICS
# ######################################################################

def jaccard(set_a, set_b):
    """Jaccard similarity between two sets."""
    if not set_a and not set_b:
        return 1.0
    inter = len(set_a & set_b)
    union = len(set_a | set_b)
    return inter / union if union > 0 else 0.0


def nmi(labels_a, labels_b):
    """Normalized Mutual Information."""
    from collections import Counter
    n = len(labels_a)
    if n == 0:
        return 0.0

    ca = Counter(labels_a)
    cb = Counter(labels_b)
    joint = Counter(zip(labels_a, labels_b))

    def entropy(counts, total):
        h = 0.0
        for c in counts.values():
            if c > 0:
                p = c / total
                h -= p * math.log(p)
        return h

    ha = entropy(ca, n)
    hb = entropy(cb, n)
    mi = 0.0
    for (a, b), count in joint.items():
        if count > 0:
            p_ab = count / n
            p_a = ca[a] / n
            p_b = cb[b] / n
            mi += p_ab * math.log(p_ab / (p_a * p_b))

    denom = (ha + hb) / 2
    return mi / denom if denom > 1e-12 else 0.0


def shd(edges_a, edges_b):
    """Structural Hamming Distance."""
    return len(edges_a.symmetric_difference(edges_b))


# ######################################################################
#  SECTION 2: RUN PROBE
# ######################################################################

def discover_from(extractor_cls, checkpoints_dir, name, concepts, device='cuda'):
    """Run BitDiscovery on a specific extractor."""
    print(f"\n  Running BitDiscovery on {name}...")
    extractor = extractor_cls(checkpoints_dir)
    ckpts = extractor.discover_checkpoints(checkpoints_dir)
    if not ckpts:
        print(f"  ERROR: No checkpoints found for {name}.")
        return None
    last_ckpt = ckpts[-1][1]  # (step, path) tuple
    snapshot = extractor.extract(last_ckpt, concepts, device=device)

    bd = BitDiscovery()
    discovery = bd.discover(snapshot)

    # Extract structure
    duals = set()
    for d in discovery.discovered_duals:
        duals.add((min(d.bit_a, d.bit_b), max(d.bit_a, d.bit_b)))

    deps = set()
    for d in discovery.discovered_deps:
        deps.add((d.bit_parent, d.bit_child))

    hierarchy = {}
    for h in discovery.discovered_hierarchy:
        hierarchy[h.bit_index] = h.layer

    return {
        'name': name,
        'n_active': discovery.n_active_bits,
        'n_dead': discovery.n_dead_bits,
        'duals': duals,
        'deps': deps,
        'hierarchy': hierarchy,
        'n_duals': len(duals),
        'n_deps': len(deps),
    }


def run_probe(triadic_dir, sae_dir=None, vqvae_dir=None, v8_dir=None, device='cuda'):
    """Run Q8 probe across architectures or across models."""
    if not HAS_REPTIMELINE:
        return None

    # Load concepts from gold primitivos (try 72-bit first, fallback to 65-bit)
    for gold_name in ['gold_primitivos_72.json', 'gold_primitivos_65.json']:
        gold_path = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'model', gold_name))
        if os.path.exists(gold_path):
            with open(gold_path, 'r', encoding='utf-8') as f:
                concepts = list(json.load(f).keys())
            print(f'  Concepts from {gold_name}: {len(concepts)}')
            break
    else:
        print('  ERROR: gold_primitivos_*.json not found')
        return None

    architectures = []

    # ── Cross-model mode: v8 vs v9 using same TriadicExtractor ──
    if v8_dir:
        # Detect model names from checkpoint configs
        v9_name = 'v9_gptneo125m'
        v8_name = 'v8_gpt2medium'
        for ckpt_dir, default_name in [(triadic_dir, v9_name), (v8_dir, v8_name)]:
            # Try to read config from best.pt or last checkpoint
            label = default_name
            best_pt = os.path.join(ckpt_dir, 'best.pt')
            if os.path.exists(best_pt):
                try:
                    import torch
                    ckpt = torch.load(best_pt, map_location='cpu', weights_only=False)
                    cfg = ckpt.get('config', {})
                    model_name = cfg.get('model_name', '')
                    if model_name:
                        short = model_name.split('/')[-1]
                        label = f"{'v9' if ckpt_dir == triadic_dir else 'v8'}_{short}"
                except Exception:
                    pass

            arch = discover_from(TriadicExtractor, ckpt_dir, label, concepts, device)
            if arch is not None:
                architectures.append(arch)

        if not architectures:
            print("  ERROR: No architectures could be loaded.")
            return None
        return architectures

    # ── Multi-extractor mode (original) ──
    # Triadic (required)
    arch_triadic = discover_from(TriadicExtractor, triadic_dir, 'triadic', concepts, device)
    if arch_triadic is not None:
        architectures.append(arch_triadic)

    # SAE (optional)
    if sae_dir and HAS_SAE:
        arch_sae = discover_from(SAEExtractor, sae_dir, 'sae', concepts, device)
        if arch_sae is not None:
            architectures.append(arch_sae)
    elif sae_dir:
        print("  WARN: SAEExtractor not available, skipping.")

    # VQ-VAE (optional)
    if vqvae_dir and HAS_VQVAE:
        arch_vqvae = discover_from(VQVAEExtractor, vqvae_dir, 'vqvae', concepts, device)
        if arch_vqvae is not None:
            architectures.append(arch_vqvae)
    elif vqvae_dir:
        print("  WARN: VQVAEExtractor not available, skipping.")

    if not architectures:
        print("  ERROR: No architectures could be loaded.")
        return None

    return architectures


def analyze(architectures):
    """Compare structures across architectures."""
    print("=" * 70)
    print("Q8: Cross-architecture consistency")
    print("=" * 70)

    n_arch = len(architectures)
    print(f"\n  Architectures compared: {n_arch}")

    for arch in architectures:
        print(f"    {arch['name']}: active={arch['n_active']}, "
              f"duals={arch['n_duals']}, deps={arch['n_deps']}")

    if n_arch < 2:
        print("\n  Need at least 2 architectures for comparison.")
        return {'n_architectures': n_arch, 'verdict': 'insufficient_data'}

    # Pairwise comparisons
    print("\n  --- Pairwise comparisons ---\n")
    comparisons = []

    for i in range(n_arch):
        for j in range(i + 1, n_arch):
            a, b = architectures[i], architectures[j]

            j_duals = jaccard(a['duals'], b['duals'])
            j_deps = jaccard(a['deps'], b['deps'])
            shd_val = shd(a['deps'], b['deps'])

            # NMI on hierarchy (shared bits)
            shared_bits = set(a['hierarchy']) & set(b['hierarchy'])
            if shared_bits:
                la = [a['hierarchy'][bit] for bit in sorted(shared_bits)]
                lb = [b['hierarchy'][bit] for bit in sorted(shared_bits)]
                h_nmi = nmi(la, lb)
            else:
                h_nmi = 0.0

            comp = {
                'arch_a': a['name'],
                'arch_b': b['name'],
                'jaccard_duals': round(j_duals, 4),
                'jaccard_deps': round(j_deps, 4),
                'shd': shd_val,
                'hierarchy_nmi': round(h_nmi, 4),
                'shared_bits': len(shared_bits),
            }
            comparisons.append(comp)

            print(f"  {a['name']} vs {b['name']}:")
            print(f"    Jaccard duals: {j_duals:.3f}")
            print(f"    Jaccard deps:  {j_deps:.3f}")
            print(f"    SHD:           {shd_val}")
            print(f"    Hierarchy NMI: {h_nmi:.3f} "
                  f"(shared bits: {len(shared_bits)})")

    # Summary
    mean_j_duals = sum(c['jaccard_duals'] for c in comparisons) / len(comparisons)
    mean_j_deps = sum(c['jaccard_deps'] for c in comparisons) / len(comparisons)
    mean_nmi = sum(c['hierarchy_nmi'] for c in comparisons) / len(comparisons)

    print(f"\n  --- Summary ---")
    print(f"  Mean Jaccard (duals): {mean_j_duals:.3f}")
    print(f"  Mean Jaccard (deps):  {mean_j_deps:.3f}")
    print(f"  Mean hierarchy NMI:   {mean_nmi:.3f}")

    # Register
    reg_path = os.path.join(STATS_DIR, 'p_values_registry.json')
    register_pvalue('neural_crossarch', 'q8_mean_jaccard_deps',
                    1.0,  # no formal p-value for this
                    notes=f'mean_jaccard={mean_j_deps:.3f}, n_arch={n_arch}',
                    path=reg_path)

    # Interpretation
    print("\n  --- Interpretation ---\n")
    if mean_j_deps > 0.5 and mean_nmi > 0.3:
        print("  POSITIVE: Structure is consistent across architectures.")
        print("  Confounder: shared training data and task objective.")
        verdict = 'positive_with_caveats'
    elif mean_j_deps > 0.2:
        print("  MIXED: Partial consistency, some architecture-specific features.")
        verdict = 'mixed'
    else:
        print("  NULL: Structures diverge significantly across architectures.")
        verdict = 'null'

    results = {
        'n_architectures': n_arch,
        'architectures': [{
            'name': a['name'],
            'n_active': a['n_active'],
            'n_duals': a['n_duals'],
            'n_deps': a['n_deps'],
        } for a in architectures],
        'comparisons': comparisons,
        'summary': {
            'mean_jaccard_duals': round(mean_j_duals, 4),
            'mean_jaccard_deps': round(mean_j_deps, 4),
            'mean_hierarchy_nmi': round(mean_nmi, 4),
        },
        'verdict': verdict,
    }
    return results


# ######################################################################
#  SECTION 3: MAIN
# ######################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Q8: Cross-architecture probe')
    parser.add_argument('--checkpoints_triadic', '--checkpoints', required=True,
                        help='Primary checkpoint dir (v9 in cross-model mode)')
    parser.add_argument('--checkpoints_v8', default=None,
                        help='v8 checkpoint dir for cross-model comparison')
    parser.add_argument('--checkpoints_sae', default=None)
    parser.add_argument('--checkpoints_vqvae', default=None)
    parser.add_argument('--device', default='cuda',
                        help='Device (cuda or cpu)')
    args = parser.parse_args()

    if not HAS_REPTIMELINE:
        print("=" * 70)
        print("Q8: Cross-Architecture Probe — reptimeline NOT INSTALLED")
        print("=" * 70)
        print("\nInstall with: pip install reptimeline")
        sys.exit(1)

    architectures = run_probe(args.checkpoints_triadic,
                              args.checkpoints_sae,
                              args.checkpoints_vqvae,
                              args.checkpoints_v8,
                              args.device)
    if architectures is None:
        sys.exit(1)

    results = analyze(architectures)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_path = os.path.join(RESULTS_DIR, 'q8_crossarch.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to: {out_path}")
