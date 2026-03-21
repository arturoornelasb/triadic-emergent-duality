"""Q4: Do triadic dependencies in the model match S/C/E/A categories?

Probe: Use BitDiscovery to find triadic dependencies (bit_r emerges
from bit_i AND bit_j), then classify each as:
  S (Synergistic): r encodes information beyond i+j
  C (Complementary): r = i AND j (conjunction)
  E (Emergent): r has no pairwise link to i or j alone
  A (Additive): r ~ i OR j

Compare distribution of S/C/E/A against random baseline.

Caveat: Triadic interactions can arise from any nonlinear combination
in the model, not necessarily from the philosophical triad concept.

Requiere: pip install reptimeline
Usage: python q4_probe_triadic.py --checkpoints <dir>
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
from registry import register_pvalue

try:
    from reptimeline import BitDiscovery
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
bit_to_name = {p.get('bit'): p['nombre'] for p in prims if p.get('bit') is not None}


# ######################################################################
#  SECTION 1: CLASSIFY TRIADIC DEPENDENCIES
# ######################################################################

def classify_triadic(td):
    """Classify a DiscoveredTriadicDep into S/C/E/A.

    S (Synergistic): high interaction, r not predictable from i or j alone
    C (Complementary): r ≈ i AND j
    E (Emergent): r has no pairwise link (p_r_given_i and p_r_given_j both low)
    A (Additive): r ≈ i OR j (pairwise links are high)
    """
    p_rij = td.p_r_given_ij
    p_ri = td.p_r_given_i
    p_rj = td.p_r_given_j
    interaction = td.interaction_strength

    # Thresholds
    HIGH = 0.6
    LOW = 0.2

    if p_ri < LOW and p_rj < LOW and p_rij > HIGH:
        return 'E'  # Emergent: only from combination
    elif p_ri > HIGH and p_rj > HIGH:
        return 'A'  # Additive: either alone predicts r
    elif interaction > 0.3 and max(p_ri, p_rj) < HIGH:
        return 'S'  # Synergistic: strong interaction, weak pairwise
    else:
        return 'C'  # Complementary: conjunction-like


# ######################################################################
#  SECTION 2: RUN PROBE
# ######################################################################

def run_probe(checkpoints_dir):
    """Run Q4 probe."""
    if not HAS_REPTIMELINE:
        return None

    extractor = TriadicExtractor(checkpoints_dir)
    snapshots = extractor.load_snapshots(checkpoints_dir)
    snapshot = snapshots[-1]

    bd = BitDiscovery(triadic_threshold=0.6, triadic_min_interaction=0.15)
    discovery = bd.discover(snapshot)

    return discovery, snapshot


def analyze(discovery, snapshot):
    """Classify and analyze triadic dependencies."""
    print("=" * 70)
    print("Q4: Triadic dependencies — S/C/E/A classification")
    print("=" * 70)

    triadic_deps = discovery.discovered_triadic_deps
    n_triadic = len(triadic_deps)
    print(f"\n  Discovered triadic dependencies: {n_triadic}")

    if n_triadic == 0:
        print("  No triadic dependencies found. Cannot analyze.")
        return {'n_triadic': 0, 'verdict': 'no_data'}

    # Classify each
    classifications = []
    for td in triadic_deps:
        cat = classify_triadic(td)
        classifications.append({
            'bit_i': td.bit_i,
            'bit_j': td.bit_j,
            'bit_r': td.bit_r,
            'name_i': bit_to_name.get(td.bit_i, f'bit{td.bit_i}'),
            'name_j': bit_to_name.get(td.bit_j, f'bit{td.bit_j}'),
            'name_r': bit_to_name.get(td.bit_r, f'bit{td.bit_r}'),
            'p_r_given_ij': round(td.p_r_given_ij, 3),
            'p_r_given_i': round(td.p_r_given_i, 3),
            'p_r_given_j': round(td.p_r_given_j, 3),
            'interaction': round(td.interaction_strength, 3),
            'category': cat,
        })

    # Count categories
    counts = {'S': 0, 'C': 0, 'E': 0, 'A': 0}
    for c in classifications:
        counts[c['category']] += 1

    print("\n  --- Category distribution ---\n")
    for cat in ['S', 'C', 'E', 'A']:
        pct = counts[cat] / n_triadic * 100
        label = {'S': 'Synergistic', 'C': 'Complementary',
                 'E': 'Emergent', 'A': 'Additive'}[cat]
        print(f"  {cat} ({label:<15}): {counts[cat]:>4} ({pct:>5.1f}%)")

    # Enrichment test: is E (Emergent) over-represented vs random?
    # Under null: all categories equally likely (25% each)
    # Chi-square-like test via permutation
    rng = random.Random(42)
    expected_frac = 1.0 / 4
    observed_E_frac = counts['E'] / n_triadic

    # Permutation null: assign random categories
    null_E_fracs = []
    for _ in range(5000):
        null_counts = {'S': 0, 'C': 0, 'E': 0, 'A': 0}
        for _ in range(n_triadic):
            null_counts[rng.choice(['S', 'C', 'E', 'A'])] += 1
        null_E_fracs.append(null_counts['E'] / n_triadic)

    n_exceed = sum(1 for f in null_E_fracs if f >= observed_E_frac)
    p_enrichment = (n_exceed + 1) / 5001

    print(f"\n  --- Enrichment test (E category) ---")
    print(f"  Observed E fraction: {observed_E_frac:.3f}")
    print(f"  Expected under null: {expected_frac:.3f}")
    print(f"  Permutation p-value: {p_enrichment:.4f}")

    # Register
    reg_path = os.path.join(STATS_DIR, 'p_values_registry.json')
    register_pvalue('neural_triadic', 'q4_emergent_enrichment', p_enrichment,
                    notes=f'E_frac={observed_E_frac:.3f}, n={n_triadic}',
                    path=reg_path)

    # Top examples per category
    print("\n  --- Top examples per category ---\n")
    for cat in ['E', 'S', 'C', 'A']:
        examples = [c for c in classifications if c['category'] == cat][:3]
        if examples:
            print(f"  {cat}:")
            for ex in examples:
                print(f"    {ex['name_i']} + {ex['name_j']} -> {ex['name_r']} "
                      f"(P(r|i,j)={ex['p_r_given_ij']}, "
                      f"interaction={ex['interaction']})")

    # Interpretation
    print("\n  --- Interpretation ---\n")
    if observed_E_frac > 0.3 and p_enrichment < 0.05:
        print("  POSITIVE: Emergent triadic deps are over-represented.")
        print("  Confounder: any nonlinear activation can produce E patterns.")
        verdict = 'positive_with_caveats'
    elif counts['E'] > 0:
        print("  MIXED: Some emergent triadic deps, but not significantly enriched.")
        verdict = 'mixed'
    else:
        print("  NULL: No emergent triadic dependencies found.")
        verdict = 'null'

    results = {
        'n_triadic': n_triadic,
        'counts': counts,
        'fractions': {k: round(v / n_triadic, 4) for k, v in counts.items()},
        'enrichment_E': {
            'observed': round(observed_E_frac, 4),
            'expected': round(expected_frac, 4),
            'p_value': round(p_enrichment, 4),
        },
        'classifications': classifications[:50],  # cap to avoid huge JSON
        'verdict': verdict,
    }
    return results


# ######################################################################
#  SECTION 3: MAIN
# ######################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Q4: Triadic probe')
    parser.add_argument('--checkpoints', required=True)
    args = parser.parse_args()

    if not HAS_REPTIMELINE:
        print("=" * 70)
        print("Q4: Triadic Probe — reptimeline NOT INSTALLED")
        print("=" * 70)
        print("\nInstall with: pip install reptimeline")
        sys.exit(1)

    result = run_probe(args.checkpoints)
    if result is None:
        sys.exit(1)

    discovery, snapshot = result
    results = analyze(discovery, snapshot)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_path = os.path.join(RESULTS_DIR, 'q4_triadic.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to: {out_path}")
