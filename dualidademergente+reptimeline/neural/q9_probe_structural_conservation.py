"""Q9: Are distributional structural properties conserved across models?

Probe: Run BitDiscovery on two models trained with different architectures
and datasets, then compare distributional properties rather than specific
bit identities. Q8 showed that specific bit assignments diverge (Jaccard~0),
but both models discover similar QUANTITIES of structure. Q9 tests whether
this quantity-conservation is statistically significant.

Metrics compared:
  - Active/dead bit ratio
  - Number of duals and dependencies
  - S/C/E/A category distribution (chi-squared)
  - Graph density (deps / possible edges)
  - Hierarchy depth distribution

Hypothesis: If triadic structure reflects something intrinsic to the task
(the 72 primitivos ontology), distributional properties should be conserved
even when specific bit assignments differ due to dataset differences.

Requiere: pip install reptimeline
Usage: python q9_probe_structural_conservation.py \
         --checkpoints_v9 <dir> --checkpoints_v8 <dir>
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

# ######################################################################
#  SECTION 0: DATA LOADING
# ######################################################################

with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
    prim_data = json.load(f)

prims = prim_data['primitivos']
bit_to_name = {p.get('bit'): p['nombre'] for p in prims if p.get('bit') is not None}


# ######################################################################
#  SECTION 1: CLASSIFY TRIADIC (same as Q4)
# ######################################################################

def classify_triadic(td):
    """Classify a DiscoveredTriadicDep into S/C/E/A."""
    p_ri = td.p_r_given_i
    p_rj = td.p_r_given_j
    p_rij = td.p_r_given_ij
    HIGH = 0.6
    LOW = 0.2

    if p_ri < LOW and p_rj < LOW and p_rij > HIGH:
        return 'E'
    elif p_ri > HIGH and p_rj > HIGH:
        return 'A'
    elif td.interaction_strength > 0.3 and max(p_ri, p_rj) < HIGH:
        return 'S'
    else:
        return 'C'


# ######################################################################
#  SECTION 2: EXTRACT STRUCTURAL PROFILE
# ######################################################################

def extract_profile(checkpoints_dir, label, concepts, device='cuda'):
    """Run BitDiscovery and compute structural profile for one model."""
    print(f"\n  [{label}] Loading model and running BitDiscovery...")
    extractor = TriadicExtractor(checkpoints_dir)
    ckpts = extractor.discover_checkpoints(checkpoints_dir)
    if not ckpts:
        print(f"  [{label}] ERROR: No checkpoints found.")
        return None
    last_ckpt = ckpts[-1][1]
    snapshot = extractor.extract(last_ckpt, concepts, device=device)

    bd = BitDiscovery(triadic_threshold=0.6, triadic_min_interaction=0.15)
    discovery = bd.discover(snapshot)

    # Basic structure
    n_active = discovery.n_active_bits
    n_dead = discovery.n_dead_bits
    n_total = n_active + n_dead
    n_duals = len(discovery.discovered_duals)
    n_deps = len(discovery.discovered_deps)

    # Hierarchy depth distribution
    layer_counts = {}
    for h in discovery.discovered_hierarchy:
        layer_counts[h.layer] = layer_counts.get(h.layer, 0) + 1
    n_layers = len(layer_counts)

    # Graph density: deps / max possible directed edges among active bits
    max_edges = n_active * (n_active - 1) if n_active > 1 else 1
    density = n_deps / max_edges

    # Triadic S/C/E/A classification
    triadic_deps = discovery.discovered_triadic_deps
    n_triadic = len(triadic_deps)
    scea = {'S': 0, 'C': 0, 'E': 0, 'A': 0}
    for td in triadic_deps:
        scea[classify_triadic(td)] += 1

    profile = {
        'label': label,
        'n_total': n_total,
        'n_active': n_active,
        'n_dead': n_dead,
        'active_ratio': round(n_active / n_total, 4) if n_total > 0 else 0,
        'n_duals': n_duals,
        'n_deps': n_deps,
        'density': round(density, 6),
        'n_layers': n_layers,
        'layer_counts': layer_counts,
        'n_triadic': n_triadic,
        'scea_counts': scea,
        'scea_fracs': {k: round(v / n_triadic, 4) if n_triadic > 0 else 0
                       for k, v in scea.items()},
    }

    print(f"  [{label}] active={n_active}/{n_total}, duals={n_duals}, "
          f"deps={n_deps}, density={density:.4f}, layers={n_layers}")
    print(f"  [{label}] triadic={n_triadic}: "
          f"S={scea['S']}({profile['scea_fracs']['S']:.1%}) "
          f"C={scea['C']}({profile['scea_fracs']['C']:.1%}) "
          f"E={scea['E']}({profile['scea_fracs']['E']:.1%}) "
          f"A={scea['A']}({profile['scea_fracs']['A']:.1%})")

    return profile


# ######################################################################
#  SECTION 3: STATISTICAL COMPARISON
# ######################################################################

def chi_squared_test(counts_a, counts_b, categories):
    """Chi-squared test comparing two categorical distributions.

    Uses the pooled distribution as expected, which tests whether
    both samples come from the same underlying distribution.
    """
    n_a = sum(counts_a[c] for c in categories)
    n_b = sum(counts_b[c] for c in categories)
    n_total = n_a + n_b

    if n_total == 0:
        return 0.0, 1.0

    chi2 = 0.0
    df = 0
    for c in categories:
        pooled = (counts_a[c] + counts_b[c]) / n_total
        if pooled > 0:
            exp_a = pooled * n_a
            exp_b = pooled * n_b
            chi2 += (counts_a[c] - exp_a) ** 2 / exp_a
            chi2 += (counts_b[c] - exp_b) ** 2 / exp_b
            df += 1

    df = max(df - 1, 1)  # degrees of freedom = categories - 1

    # Approximate p-value using chi-squared survival function
    # Using Wilson-Hilferty approximation for chi-squared CDF
    p_value = chi2_survival(chi2, df)
    return chi2, p_value


def chi2_survival(x, df):
    """Approximate chi-squared survival function (no scipy needed)."""
    if x <= 0:
        return 1.0
    # Wilson-Hilferty normal approximation
    z = ((x / df) ** (1/3) - (1 - 2 / (9 * df))) / math.sqrt(2 / (9 * df))
    # Standard normal survival (Abramowitz & Stegun 26.2.17)
    return 0.5 * math.erfc(z / math.sqrt(2))


def ratio_similarity(a, b):
    """Similarity between two ratios: 1 - |a-b| / max(a,b).
    Returns 1.0 for identical, 0.0 for maximally different."""
    if a == 0 and b == 0:
        return 1.0
    return 1.0 - abs(a - b) / max(a, b)


# ######################################################################
#  SECTION 4: ANALYZE
# ######################################################################

def analyze(profile_a, profile_b):
    """Compare structural profiles."""
    print("\n" + "=" * 70)
    print("Q9: Structural conservation across models")
    print("=" * 70)

    la, lb = profile_a['label'], profile_b['label']
    print(f"\n  Comparing: {la} vs {lb}\n")

    # ── Scalar properties ──
    print("  --- Scalar properties ---\n")
    scalars = [
        ('Active bits',   profile_a['n_active'],    profile_b['n_active']),
        ('Dead bits',     profile_a['n_dead'],       profile_b['n_dead']),
        ('Active ratio',  profile_a['active_ratio'], profile_b['active_ratio']),
        ('Duals',         profile_a['n_duals'],      profile_b['n_duals']),
        ('Dependencies',  profile_a['n_deps'],       profile_b['n_deps']),
        ('Graph density', profile_a['density'],      profile_b['density']),
        ('Hierarchy layers', profile_a['n_layers'],  profile_b['n_layers']),
        ('Triadic deps',  profile_a['n_triadic'],    profile_b['n_triadic']),
    ]

    similarities = []
    scalar_results = []
    print(f"  {'Property':<20} {la:>15} {lb:>15} {'Similarity':>12}")
    print(f"  {'-'*20} {'-'*15} {'-'*15} {'-'*12}")
    for name, va, vb in scalars:
        sim = ratio_similarity(va, vb) if isinstance(va, (int, float)) else 0
        similarities.append(sim)
        scalar_results.append({'property': name, la: va, lb: vb, 'similarity': round(sim, 4)})
        va_s = f"{va:.4f}" if isinstance(va, float) else str(va)
        vb_s = f"{vb:.4f}" if isinstance(vb, float) else str(vb)
        print(f"  {name:<20} {va_s:>15} {vb_s:>15} {sim:>11.1%}")

    mean_scalar_sim = sum(similarities) / len(similarities)
    print(f"\n  Mean scalar similarity: {mean_scalar_sim:.1%}")

    # ── S/C/E/A distribution ──
    print("\n  --- S/C/E/A distribution ---\n")
    cats = ['S', 'C', 'E', 'A']
    print(f"  {'Cat':<5} {la+' (n)':>12} {la+' (%)':>10} {lb+' (n)':>12} {lb+' (%)':>10}")
    print(f"  {'-'*5} {'-'*12} {'-'*10} {'-'*12} {'-'*10}")
    for c in cats:
        na = profile_a['scea_counts'][c]
        nb = profile_b['scea_counts'][c]
        fa = profile_a['scea_fracs'][c]
        fb = profile_b['scea_fracs'][c]
        print(f"  {c:<5} {na:>12} {fa:>9.1%} {nb:>12} {fb:>9.1%}")

    chi2, p_scea = chi_squared_test(profile_a['scea_counts'],
                                     profile_b['scea_counts'], cats)
    print(f"\n  Chi-squared: {chi2:.2f}, p = {p_scea:.4f}")

    if p_scea > 0.05:
        print("  -> Distributions are NOT significantly different (p > 0.05)")
        scea_verdict = 'conserved'
    else:
        print("  -> Distributions ARE significantly different (p < 0.05)")
        scea_verdict = 'divergent'

    # ── Permutation test on scalar vector ──
    # Under null: shuffle profile values randomly between models
    # Test: is the observed mean similarity higher than expected by chance?
    import random
    rng = random.Random(42)
    n_perm = 10000
    observed_sim = mean_scalar_sim
    null_sims = []
    for _ in range(n_perm):
        perm_sims = []
        for _, va, vb in scalars:
            # Randomly swap or not
            if rng.random() < 0.5:
                va, vb = vb, va
            # Add noise proportional to range
            max_val = max(abs(va), abs(vb), 1)
            noise_a = va + rng.gauss(0, max_val * 0.3)
            noise_b = vb + rng.gauss(0, max_val * 0.3)
            perm_sims.append(ratio_similarity(abs(noise_a), abs(noise_b)))
        null_sims.append(sum(perm_sims) / len(perm_sims))

    p_scalar = sum(1 for s in null_sims if s >= observed_sim) / n_perm
    print(f"\n  --- Scalar conservation test ---")
    print(f"  Observed mean similarity: {observed_sim:.3f}")
    print(f"  Null mean (permutation):  {sum(null_sims)/len(null_sims):.3f}")
    print(f"  p-value: {p_scalar:.4f}")

    # ── Register ──
    reg_path = os.path.join(STATS_DIR, 'p_values_registry.json')
    register_pvalue('neural_structural', 'q9_scea_chi2', p_scea,
                    notes=f'chi2={chi2:.2f}, {la} vs {lb}',
                    path=reg_path)
    register_pvalue('neural_structural', 'q9_scalar_conservation', p_scalar,
                    notes=f'mean_sim={observed_sim:.3f}, {la} vs {lb}',
                    path=reg_path)

    # ── Overall verdict ──
    print("\n  --- Interpretation ---\n")
    n_conserved = 0
    n_total_tests = 2

    if p_scea > 0.05:
        n_conserved += 1
    if mean_scalar_sim > 0.8:
        n_conserved += 1

    if n_conserved == n_total_tests:
        verdict = 'positive'
        print("  POSITIVE: Distributional structure is conserved across models.")
        print("  Both S/C/E/A distribution and scalar properties match.")
        print("  This supports the hypothesis that triadic structure reflects")
        print("  task/ontology properties, not model-specific artifacts.")
    elif n_conserved >= 1:
        verdict = 'mixed'
        print("  MIXED: Partial conservation of structural properties.")
        if scea_verdict == 'conserved':
            print("  S/C/E/A distribution conserved, but scalar magnitudes differ.")
        else:
            print("  Scalar magnitudes similar, but S/C/E/A distribution differs.")
    else:
        verdict = 'null'
        print("  NULL: Structural properties diverge across models.")

    print(f"\n  Combined with Q8 (bit-identity NULL): specific assignments are")
    print(f"  model/dataset-dependent, but distributional properties are {verdict}.")

    results = {
        'models': [la, lb],
        'profiles': {
            la: {k: v for k, v in profile_a.items() if k != 'label'},
            lb: {k: v for k, v in profile_b.items() if k != 'label'},
        },
        'scalar_comparison': scalar_results,
        'mean_scalar_similarity': round(mean_scalar_sim, 4),
        'scea_chi2': round(chi2, 4),
        'scea_p_value': round(p_scea, 4),
        'scea_verdict': scea_verdict,
        'scalar_p_value': round(p_scalar, 4),
        'verdict': verdict,
    }
    return results


# ######################################################################
#  SECTION 5: MAIN
# ######################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Q9: Structural conservation across models')
    parser.add_argument('--checkpoints_v9', '--checkpoints', required=True,
                        help='v9 checkpoint dir (GPT-Neo 125M)')
    parser.add_argument('--checkpoints_v8', required=True,
                        help='v8 checkpoint dir (GPT-2 Medium)')
    parser.add_argument('--device', default='cuda')
    args = parser.parse_args()

    if not HAS_REPTIMELINE:
        print("=" * 70)
        print("Q9: Structural Conservation — reptimeline NOT INSTALLED")
        print("=" * 70)
        print("\nInstall with: pip install reptimeline")
        sys.exit(1)

    # Load concepts
    for gold_name in ['gold_primitivos_72.json', 'gold_primitivos_65.json']:
        gold_path = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'model', gold_name))
        if os.path.exists(gold_path):
            with open(gold_path, 'r', encoding='utf-8') as f:
                concepts = list(json.load(f).keys())
            print(f'  Concepts from {gold_name}: {len(concepts)}')
            break
    else:
        print('  ERROR: gold_primitivos_*.json not found')
        sys.exit(1)

    # Extract profiles
    profile_v9 = extract_profile(args.checkpoints_v9, 'v9_gptneo125m',
                                  concepts, args.device)
    profile_v8 = extract_profile(args.checkpoints_v8, 'v8_gpt2medium',
                                  concepts, args.device)

    if profile_v9 is None or profile_v8 is None:
        print("ERROR: Could not extract profiles from both models.")
        sys.exit(1)

    results = analyze(profile_v9, profile_v8)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_path = os.path.join(RESULTS_DIR, 'q9_structural_conservation.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to: {out_path}")
