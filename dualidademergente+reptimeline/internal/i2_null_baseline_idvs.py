"""I2: Null baseline for IDVS threshold calibration.

Permutes primitivo-to-dualidad assignments 10000 times, recalculates
IDVS for each, and reports the null distribution. Compares with the
current threshold (0.80).

Solo stdlib: json, math, os, random, sys.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import math
import os
import random
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))
RESULTS_DIR = os.path.join(SCRIPT_DIR, 'results')
STATS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'stats'))
sys.path.insert(0, STATS_DIR)

from bootstrap import percentile

# ######################################################################
#  SECTION 0: DATA LOADING
# ######################################################################

with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
    prim_data = json.load(f)

with open(os.path.join(DATA_DIR, 'reference_domains.json'), 'r', encoding='utf-8') as f:
    dom_data = json.load(f)

with open(os.path.join(DATA_DIR, 'dualidad_primitivo_map.json'), 'r', encoding='utf-8') as f:
    dual_data = json.load(f)

prims = prim_data['primitivos']
names = [p['nombre'] for p in prims]
capa_map = {p['nombre']: p['capa'] for p in prims}
deps_map = {p['nombre']: list(p['deps']) for p in prims}
total_L14 = sum(1 for p in prims if p['capa'] <= 4)

# Domains (exclude astrology control)
domains = dom_data['domains']
positive_domains = {k: v for k, v in domains.items()
                    if k.lower() != 'astrology'}

# ######################################################################
#  SECTION 1: IDVS CALCULATION
# ######################################################################

def compute_idvs(domain_classes, dep_pairs):
    """Compute IDVS = Coverage_L14 * Monotonicity.

    Coverage_L14 counts only nulls in layers 1-4 (matching integration_audit.py).

    Args:
        domain_classes: dict mapping primitive_name -> 'D', 'A', or 'N'.
        dep_pairs: list of (parent_name, child_name) tuples.

    Returns:
        dict with coverage, monotonicity, idvs.
    """
    if total_L14 == 0:
        return {'coverage': 0.0, 'monotonicity': 0.0, 'idvs': 0.0}

    # Coverage L1-4: fraction of L1-4 primitives that are NOT null
    nulls_L14 = sum(1 for name, cls in domain_classes.items()
                    if capa_map.get(name, 99) <= 4 and cls == 'N')
    coverage = 1.0 - nulls_L14 / total_L14

    # Monotonicity: for each dependency (parent, child), check consistency
    # A violation occurs when child is more "active" than parent
    # Ordering: D > A > N
    rank = {'D': 2, 'A': 1, 'N': 0}
    total_pairs = 0
    ok_pairs = 0
    for parent, child in dep_pairs:
        if parent in domain_classes and child in domain_classes:
            total_pairs += 1
            r_parent = rank.get(domain_classes[parent], 0)
            r_child = rank.get(domain_classes[child], 0)
            if r_child <= r_parent:
                ok_pairs += 1

    monotonicity = ok_pairs / total_pairs if total_pairs > 0 else 1.0
    idvs = coverage * monotonicity

    return {'coverage': coverage, 'monotonicity': monotonicity, 'idvs': idvs}


# Build dependency pairs
dep_pairs = []
for p in prims:
    for d in p['deps']:
        dep_pairs.append((d, p['nombre']))

# ######################################################################
#  SECTION 2: OBSERVED IDVS
# ######################################################################

print("=" * 70)
print("I2: Null Baseline for IDVS Threshold")
print("=" * 70)

print("\n--- Observed IDVS ---\n")
observed_idvs = {}
for dom_name, dom_info in positive_domains.items():
    classes = dom_info.get('classes', dom_info)
    if isinstance(classes, dict) and 'classes' in classes:
        classes = classes['classes']
    result = compute_idvs(classes, dep_pairs)
    observed_idvs[dom_name] = result['idvs']
    print(f"  {dom_name:<15} IDVS = {result['idvs']:.3f} "
          f"(cov={result['coverage']:.3f}, mono={result['monotonicity']:.3f})")

# ######################################################################
#  SECTION 3: NULL DISTRIBUTION (PERMUTATION)
# ######################################################################

N_PERMS = 10000
SEED = 42
rng = random.Random(SEED)

# For each permutation: shuffle the D-A-N classifications within each
# domain (preserving the distribution of D/A/N counts), then recalculate
# IDVS. This tests whether the SPECIFIC assignment of primitives to
# classifications matters, or if any assignment with the same distribution
# would score equally high.

print(f"\n--- Running {N_PERMS} permutations ---\n")

null_max_idvs = []  # max IDVS across domains per permutation
null_mean_idvs = []  # mean IDVS across domains per permutation

for perm_i in range(N_PERMS):
    perm_idvs_list = []

    for dom_name, dom_info in positive_domains.items():
        classes = dom_info.get('classes', dom_info)
        if isinstance(classes, dict) and 'classes' in classes:
            classes = classes['classes']

        # Shuffle: assign the same distribution of D/A/N to random primitives
        values = list(classes.values())
        rng.shuffle(values)
        shuffled = dict(zip(names, values))

        result = compute_idvs(shuffled, dep_pairs)
        perm_idvs_list.append(result['idvs'])

    null_max_idvs.append(max(perm_idvs_list))
    null_mean_idvs.append(sum(perm_idvs_list) / len(perm_idvs_list))

    if (perm_i + 1) % 2000 == 0:
        print(f"  {perm_i + 1}/{N_PERMS} permutations done...")

# ######################################################################
#  SECTION 4: THRESHOLD ANALYSIS
# ######################################################################

print("\n--- Null Distribution Statistics ---\n")

null_max_sorted = sorted(null_max_idvs)
null_mean_sorted = sorted(null_mean_idvs)

p50_max = percentile(null_max_sorted, 50)
p90_max = percentile(null_max_sorted, 90)
p95_max = percentile(null_max_sorted, 95)
p99_max = percentile(null_max_sorted, 99)
null_mean_of_max = sum(null_max_idvs) / len(null_max_idvs)

print(f"  Max IDVS across domains per permutation:")
print(f"    mean    = {null_mean_of_max:.3f}")
print(f"    median  = {p50_max:.3f}")
print(f"    p90     = {p90_max:.3f}")
print(f"    p95     = {p95_max:.3f}")
print(f"    p99     = {p99_max:.3f}")

p50_mean = percentile(null_mean_sorted, 50)
p95_mean = percentile(null_mean_sorted, 95)
null_mean_of_mean = sum(null_mean_idvs) / len(null_mean_idvs)

print(f"\n  Mean IDVS across domains per permutation:")
print(f"    mean    = {null_mean_of_mean:.3f}")
print(f"    median  = {p50_mean:.3f}")
print(f"    p95     = {p95_mean:.3f}")

# ######################################################################
#  SECTION 5: COMPARE WITH CURRENT THRESHOLD
# ######################################################################

CURRENT_THRESHOLD = 0.80

# How many permutations produce max IDVS >= threshold?
n_exceed = sum(1 for x in null_max_idvs if x >= CURRENT_THRESHOLD)
p_exceed = n_exceed / N_PERMS

print(f"\n--- Threshold Evaluation (current = {CURRENT_THRESHOLD}) ---\n")
print(f"  P(max_null_IDVS >= {CURRENT_THRESHOLD}) = {p_exceed:.4f} ({n_exceed}/{N_PERMS})")

if p_exceed < 0.05:
    print(f"  >> Threshold {CURRENT_THRESHOLD} is WELL ABOVE the null (p95={p95_max:.3f})")
    print(f"     The observed IDVS scores are NOT achievable by random assignment.")
    verdict = 'threshold_supported'
else:
    print(f"  >> WARNING: Threshold {CURRENT_THRESHOLD} is WITHIN the null distribution!")
    print(f"     Random assignment achieves this threshold {p_exceed*100:.1f}% of the time.")
    verdict = 'threshold_at_risk'

# How many observed domains exceed p95 of null?
print(f"\n  Observed domains vs null p95 ({p95_max:.3f}):")
for dom_name, idvs in sorted(observed_idvs.items(), key=lambda x: -x[1]):
    status = 'ABOVE' if idvs > p95_max else 'WITHIN null'
    print(f"    {dom_name:<15} {idvs:.3f}  [{status}]")

# ######################################################################
#  SECTION 6: SAVE RESULTS
# ######################################################################

os.makedirs(RESULTS_DIR, exist_ok=True)
output = {
    'n_perms': N_PERMS,
    'current_threshold': CURRENT_THRESHOLD,
    'null_max': {
        'mean': round(null_mean_of_max, 4),
        'p50': round(p50_max, 4),
        'p90': round(p90_max, 4),
        'p95': round(p95_max, 4),
        'p99': round(p99_max, 4),
    },
    'null_mean': {
        'mean': round(null_mean_of_mean, 4),
        'p50': round(p50_mean, 4),
        'p95': round(p95_mean, 4),
    },
    'p_exceed_threshold': round(p_exceed, 4),
    'verdict': verdict,
    'observed_idvs': {k: round(v, 4) for k, v in observed_idvs.items()},
}

out_path = os.path.join(RESULTS_DIR, 'i2_null_idvs.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nResults saved to: {out_path}")
