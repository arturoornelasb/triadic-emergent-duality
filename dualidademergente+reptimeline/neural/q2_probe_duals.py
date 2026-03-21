"""Q2: Do dual pairs show anti-correlation in the model?

Probe: For each of the 13 dual axes, check if the two anchor bits
show negative correlation. Compare against 1000 random pairs as null.

Caveat: Anti-correlation can arise from mutual exclusion in training
data (e.g., 'hot' vs 'cold' rarely co-occur), not from structural
duality. We report this confounder explicitly.

Requiere: pip install reptimeline
Usage: python q2_probe_duals.py --checkpoints <dir>
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import argparse
import json
import math
import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(SCRIPT_DIR, 'results')
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))
STATS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'stats'))
sys.path.insert(0, STATS_DIR)

from bh_fdr import benjamini_hochberg
from bootstrap import bootstrap_ci
from registry import register_pvalue

try:
    from reptimeline import PrimitiveOverlay, BitDiscovery
    from reptimeline.extractors import TriadicExtractor
    HAS_REPTIMELINE = True
except ImportError:
    HAS_REPTIMELINE = False

# ######################################################################
#  SECTION 0: DATA LOADING
# ######################################################################

with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
    prim_data = json.load(f)

prims = prim_data['primitivos']
ejes = prim_data.get('ejes_duales', [])

# Build dual pairs: (bit_a, bit_b, axis_name)
dual_pairs = []
name_to_bit = {p['nombre']: p.get('bit') for p in prims}
for eje in ejes:
    polo_a = eje.get('polo_a') or eje.get('primitivo_a')
    polo_b = eje.get('polo_b') or eje.get('primitivo_b')
    bit_a = name_to_bit.get(polo_a)
    bit_b = name_to_bit.get(polo_b)
    if bit_a is not None and bit_b is not None:
        dual_pairs.append({
            'axis': eje.get('nombre', f'{polo_a}-{polo_b}'),
            'polo_a': polo_a,
            'polo_b': polo_b,
            'bit_a': bit_a,
            'bit_b': bit_b,
        })


# ######################################################################
#  SECTION 1: CORRELATION HELPERS
# ######################################################################

def pearson_r(x, y):
    """Pearson correlation coefficient."""
    n = len(x)
    if n < 3:
        return 0.0
    mx = sum(x) / n
    my = sum(y) / n
    num = sum((x[i] - mx) * (y[i] - my) for i in range(n))
    dx = math.sqrt(sum((x[i] - mx) ** 2 for i in range(n)))
    dy = math.sqrt(sum((y[i] - my) ** 2 for i in range(n)))
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)


def correlation_perm_p(x, y, n_perms=5000, seed=42):
    """Permutation p-value for Pearson r (two-tailed)."""
    rng = random.Random(seed)
    observed = abs(pearson_r(x, y))
    count = 0
    y_copy = list(y)
    for _ in range(n_perms):
        rng.shuffle(y_copy)
        if abs(pearson_r(x, y_copy)) >= observed:
            count += 1
    return (count + 1) / (n_perms + 1)


# ######################################################################
#  SECTION 2: RUN PROBE
# ######################################################################

def run_probe(checkpoints_dir):
    """Run Q2 probe on saved checkpoints."""
    if not HAS_REPTIMELINE:
        print("ERROR: reptimeline not installed.")
        return None

    extractor = TriadicExtractor(checkpoints_dir)
    snapshots = extractor.load_snapshots(checkpoints_dir)

    # Use the last snapshot for correlation analysis
    snapshot = snapshots[-1]
    codes = snapshot.codes  # dict: concept -> list[int] (binary code)

    # BitDiscovery for discovered duals
    bd = BitDiscovery(dual_threshold=-0.3)
    discovery = bd.discover(snapshot)

    return codes, discovery


def analyze(codes, discovery):
    """Compute dual correlations and compare with null."""
    print("=" * 70)
    print("Q2: Do dual pairs show anti-correlation?")
    print("=" * 70)

    n_concepts = len(codes)
    concepts = list(codes.keys())
    n_bits = len(next(iter(codes.values())))

    print(f"\n  Concepts: {n_concepts}, Bits: {n_bits}")
    print(f"  Theoretical dual axes: {len(dual_pairs)}")
    print(f"  Discovered duals: {len(discovery.discovered_duals)}")

    # Extract bit activation vectors
    def bit_vector(bit_idx):
        return [codes[c][bit_idx] for c in concepts]

    # Theoretical dual correlations
    print("\n  --- Theoretical dual pair correlations ---\n")
    theo_results = []
    theo_p_values = []

    for dp in dual_pairs:
        vec_a = bit_vector(dp['bit_a'])
        vec_b = bit_vector(dp['bit_b'])
        r = pearson_r(vec_a, vec_b)
        p = correlation_perm_p(vec_a, vec_b)
        theo_results.append({
            'axis': dp['axis'],
            'polo_a': dp['polo_a'],
            'polo_b': dp['polo_b'],
            'bit_a': dp['bit_a'],
            'bit_b': dp['bit_b'],
            'correlation': round(r, 4),
            'p_value': round(p, 4),
        })
        theo_p_values.append(p)
        anti = 'ANTI' if r < -0.1 else 'pos' if r > 0.1 else 'near-zero'
        print(f"  {dp['axis']:<30} r={r:+.3f} p={p:.4f} [{anti}]")

    # BH-FDR correction
    significant = benjamini_hochberg(theo_p_values, 0.05)
    n_sig = sum(significant)
    n_anti = sum(1 for tr in theo_results if tr['correlation'] < -0.1)

    print(f"\n  Anti-correlated (r < -0.1): {n_anti}/{len(dual_pairs)}")
    print(f"  Significant after BH-FDR: {n_sig}/{len(dual_pairs)}")

    # Random pair baseline (1000 random pairs)
    rng = random.Random(42)
    all_bits = list(range(n_bits))
    random_corrs = []

    for _ in range(1000):
        ba, bb = rng.sample(all_bits, 2)
        r = pearson_r(bit_vector(ba), bit_vector(bb))
        random_corrs.append(r)

    random_mean = sum(random_corrs) / len(random_corrs)
    random_anti = sum(1 for r in random_corrs if r < -0.1)

    print(f"\n  --- Random pair baseline (1000 pairs) ---")
    print(f"  Mean correlation: {random_mean:.3f}")
    print(f"  Anti-correlated (r < -0.1): {random_anti}/1000 ({random_anti/10:.1f}%)")

    # Compare: are theoretical duals more anti-correlated than random?
    theo_corrs = [tr['correlation'] for tr in theo_results]
    theo_mean = sum(theo_corrs) / len(theo_corrs) if theo_corrs else 0

    print(f"\n  Theoretical mean correlation: {theo_mean:.3f}")
    print(f"  Random mean correlation: {random_mean:.3f}")

    # Discovered duals that match theory
    print("\n  --- Discovered duals matching theory ---\n")
    matches = 0
    for dd in discovery.discovered_duals:
        for dp in dual_pairs:
            if ((dd.bit_a == dp['bit_a'] and dd.bit_b == dp['bit_b']) or
                    (dd.bit_a == dp['bit_b'] and dd.bit_b == dp['bit_a'])):
                matches += 1
                print(f"  MATCH: {dp['axis']} (model r={dd.anti_correlation:.3f})")
                break

    print(f"\n  Matches: {matches}/{len(dual_pairs)} theoretical axes")
    print(f"  Discovered but not in theory: "
          f"{len(discovery.discovered_duals) - matches}")

    # Register p-values
    reg_path = os.path.join(STATS_DIR, 'p_values_registry.json')
    for tr, sig in zip(theo_results, significant):
        register_pvalue('neural_duals', f"q2_{tr['axis']}",
                        tr['p_value'],
                        notes=f"r={tr['correlation']}, n_concepts={n_concepts}",
                        path=reg_path)

    # Interpretation
    print("\n  --- Interpretation ---\n")
    frac_anti = n_anti / len(dual_pairs) if dual_pairs else 0

    if frac_anti > 0.7 and n_sig > len(dual_pairs) // 2:
        print("  POSITIVE: Majority of dual axes show significant anti-correlation.")
        print("  Confounder: semantic exclusion in training data.")
        verdict = 'positive_with_caveats'
    elif frac_anti > 0.3:
        print("  MIXED: Some dual axes anti-correlate, others do not.")
        verdict = 'mixed'
    else:
        print("  NULL: Dual axes do not show systematic anti-correlation.")
        verdict = 'null'

    results = {
        'n_concepts': n_concepts,
        'n_bits': n_bits,
        'n_dual_axes': len(dual_pairs),
        'theoretical_duals': theo_results,
        'n_significant_bh': n_sig,
        'n_anti_correlated': n_anti,
        'random_baseline': {
            'mean_correlation': round(random_mean, 4),
            'pct_anti': round(random_anti / 10, 2),
        },
        'discovered_matches': matches,
        'discovered_total': len(discovery.discovered_duals),
        'verdict': verdict,
    }
    return results


# ######################################################################
#  SECTION 3: MAIN
# ######################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Q2: Dual coherence probe')
    parser.add_argument('--checkpoints', required=True)
    args = parser.parse_args()

    if not HAS_REPTIMELINE:
        print("=" * 70)
        print("Q2: Dual Coherence Probe — reptimeline NOT INSTALLED")
        print("=" * 70)
        print("\nInstall with: pip install reptimeline")
        sys.exit(1)

    result = run_probe(args.checkpoints)
    if result is None:
        sys.exit(1)

    codes, discovery = result
    results = analyze(codes, discovery)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_path = os.path.join(RESULTS_DIR, 'q2_duals.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to: {out_path}")
