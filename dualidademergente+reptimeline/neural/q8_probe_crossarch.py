"""Q8: Is the structure consistent across different model architectures?

Probe: Run BitDiscovery on multiple extractor backends (SAE, VQ-VAE,
standard triadic) and compare the discovered structures. If duals, deps,
and hierarchy are consistent across architectures, the structure is
more likely intrinsic to the task than an artifact of one architecture.

Caveat: All architectures share the same training data and loss, so
convergence might reflect data structure, not ontological truth.

Requiere: pip install reptimeline
Usage: python q8_probe_crossarch.py --checkpoints_triadic <dir>
       --checkpoints_sae <dir> --checkpoints_vqvae <dir>
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
sys.path.insert(0, STATS_DIR)

from registry import register_pvalue

try:
    from reptimeline import BitDiscovery
    from reptimeline.extractors import TriadicExtractor
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

def discover_from(extractor_cls, checkpoints_dir, name):
    """Run BitDiscovery on a specific extractor."""
    print(f"\n  Running BitDiscovery on {name}...")
    extractor = extractor_cls(checkpoints_dir)
    snapshots = extractor.load_snapshots(checkpoints_dir)
    snapshot = snapshots[-1]

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


def run_probe(triadic_dir, sae_dir=None, vqvae_dir=None):
    """Run Q8 probe across architectures."""
    if not HAS_REPTIMELINE:
        return None

    architectures = []

    # Triadic (required)
    arch_triadic = discover_from(TriadicExtractor, triadic_dir, 'triadic')
    architectures.append(arch_triadic)

    # SAE (optional)
    if sae_dir and HAS_SAE:
        arch_sae = discover_from(SAEExtractor, sae_dir, 'sae')
        architectures.append(arch_sae)
    elif sae_dir:
        print("  WARN: SAEExtractor not available, skipping.")

    # VQ-VAE (optional)
    if vqvae_dir and HAS_VQVAE:
        arch_vqvae = discover_from(VQVAEExtractor, vqvae_dir, 'vqvae')
        architectures.append(arch_vqvae)
    elif vqvae_dir:
        print("  WARN: VQVAEExtractor not available, skipping.")

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
    parser.add_argument('--checkpoints_triadic', required=True)
    parser.add_argument('--checkpoints_sae', default=None)
    parser.add_argument('--checkpoints_vqvae', default=None)
    args = parser.parse_args()

    if not HAS_REPTIMELINE:
        print("=" * 70)
        print("Q8: Cross-Architecture Probe — reptimeline NOT INSTALLED")
        print("=" * 70)
        print("\nInstall with: pip install reptimeline")
        sys.exit(1)

    architectures = run_probe(args.checkpoints_triadic,
                              args.checkpoints_sae,
                              args.checkpoints_vqvae)
    if architectures is None:
        sys.exit(1)

    results = analyze(architectures)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_path = os.path.join(RESULTS_DIR, 'q8_crossarch.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to: {out_path}")
