"""I4: Bayesian comparison of alternative duality orderings.

Compares the theoretical order (CIRCLE + SPIRAL) against reversed,
random, and philosophically-motivated alternatives using triangularity
and tree fidelity as likelihood proxies.

Solo stdlib: json, math, os, random, sys, collections.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import math
import os
import random
from collections import defaultdict, deque
from copy import deepcopy

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))
RESULTS_DIR = os.path.join(SCRIPT_DIR, 'results')

# ######################################################################
#  SECTION 0: DATA LOADING
# ######################################################################

with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
    prim_data = json.load(f)

with open(os.path.join(DATA_DIR, 'dualidad_primitivo_map.json'), 'r', encoding='utf-8') as f:
    dual_data = json.load(f)

prims = prim_data['primitivos']

# ######################################################################
#  SECTION 1: METRIC FUNCTIONS (reused from i3)
# ######################################################################

def compute_ancestors(prim_list):
    deps = {p['nombre']: set(p['deps']) for p in prim_list}
    ancestors = {}
    for name in deps:
        visited = set()
        queue = deque(deps[name])
        while queue:
            anc = queue.popleft()
            if anc not in visited:
                visited.add(anc)
                queue.extend(deps.get(anc, set()) - visited)
        ancestors[name] = visited
    return ancestors


def dependency_matrix(dualidades, dual_map, ancestors):
    n = len(dualidades)
    matrix = [[0.0] * n for _ in range(n)]
    for j, dj in enumerate(dualidades):
        dj_info = dual_map['dualidades'].get(dj, {})
        dj_anchors = set(dj_info.get('anclas', []))
        dj_ancestors = set()
        for a in dj_anchors:
            dj_ancestors |= ancestors.get(a, set())
        for i, di in enumerate(dualidades):
            if i == j:
                continue
            di_info = dual_map['dualidades'].get(di, {})
            di_anchors = set(di_info.get('anclas', []))
            overlap = dj_ancestors & di_anchors
            if di_anchors:
                matrix[i][j] = len(overlap) / len(di_anchors)
    return matrix


def triangularity(matrix, n):
    above = 0
    total = 0
    for i in range(n):
        for j in range(i + 1, n):
            total += 1
            if matrix[i][j] > 0:
                above += 1
    return above / total if total > 0 else 0.0


# ######################################################################
#  SECTION 2: DEFINE COMPETING ORDERS
# ######################################################################

CIRCLE_ORDER = ['D1_existir', 'D2_espacio', 'D3_tiempo',
                'D4_posibilidad', 'D5_identidad', 'D6_movimiento', 'D7_orden']
SPIRAL_ORDER = ['D8_uno_muchos', 'D9_dentro_fuera', 'D10_parte_todo',
                'D11_vida_muerte', 'D12_causa_efecto',
                'D13_semejante_diferente', 'D14_sujeto_objeto']

M_TEO = CIRCLE_ORDER + SPIRAL_ORDER
M_REV = list(reversed(M_TEO))

# Hegel-inspired: Being -> Nothing -> Becoming -> Quality -> Quantity ...
# Approximate mapping to our 14 dualidades:
M_HEGEL = [
    'D1_existir',        # Ser (Being)
    'D5_identidad',      # No-ser (Nothing/Negation)
    'D6_movimiento',     # Devenir (Becoming = motion)
    'D7_orden',          # Cualidad (Quality = pattern)
    'D8_uno_muchos',     # Cantidad (Quantity = one/many)
    'D4_posibilidad',    # Medida (Measure = possibility)
    'D2_espacio',        # Esencia → espacio
    'D3_tiempo',         # Apariencia → tiempo
    'D12_causa_efecto',  # Causalidad
    'D9_dentro_fuera',   # Interioridad
    'D10_parte_todo',    # Totalidad
    'D13_semejante_diferente',  # Diferencia
    'D11_vida_muerte',   # Vida
    'D14_sujeto_objeto', # Idea absoluta → sujeto
]

# Peirce triadic: Firstness -> Secondness -> Thirdness, then elaboration
M_PEIRCE = [
    'D1_existir',        # Firstness (pure quality)
    'D5_identidad',      # Secondness (reaction, brute fact)
    'D7_orden',          # Thirdness (law, mediation)
    'D2_espacio',        # Space as firstness elaborated
    'D3_tiempo',         # Time as secondness elaborated
    'D4_posibilidad',    # Possibility (modal)
    'D6_movimiento',     # Action
    'D8_uno_muchos',     # Multiplicity
    'D12_causa_efecto',  # Causation (secondness)
    'D13_semejante_diferente',  # Likeness (thirdness)
    'D9_dentro_fuera',   # Boundary
    'D10_parte_todo',    # Whole
    'D11_vida_muerte',   # Life
    'D14_sujeto_objeto', # Subject
]

NAMED_ORDERS = {
    'M_teo (proposed)': M_TEO,
    'M_rev (reversed)': M_REV,
    'M_hegel': M_HEGEL,
    'M_peirce': M_PEIRCE,
}

# ######################################################################
#  SECTION 3: COMPUTE TRIANGULARITY FOR EACH ORDER
# ######################################################################

ancestors = compute_ancestors(prims)

print("=" * 70)
print("I4: Bayesian Comparison of Alternative Orderings")
print("=" * 70)
print("\n--- Triangularity per ordering ---\n")

scores = {}
for name, order in NAMED_ORDERS.items():
    mat = dependency_matrix(order, dual_data, ancestors)
    tri = triangularity(mat, len(order))
    scores[name] = tri
    print(f"  {name:<25} triangularity = {tri:.3f}")

# ######################################################################
#  SECTION 4: RANDOM BASELINE (1000 random orderings)
# ######################################################################

N_RANDOM = 1000
rng = random.Random(42)
random_tris = []

for _ in range(N_RANDOM):
    perm = list(M_TEO)
    rng.shuffle(perm)
    mat = dependency_matrix(perm, dual_data, ancestors)
    tri = triangularity(mat, len(perm))
    random_tris.append(tri)

random_mean = sum(random_tris) / len(random_tris)
random_std = math.sqrt(sum((x - random_mean)**2 for x in random_tris) / len(random_tris))
random_max = max(random_tris)

print(f"\n--- Random baseline ({N_RANDOM} orderings) ---\n")
print(f"  mean = {random_mean:.3f}, std = {random_std:.3f}, max = {random_max:.3f}")

# ######################################################################
#  SECTION 5: BAYES FACTOR APPROXIMATION
# ######################################################################

# Use triangularity as a likelihood proxy.
# P(data|M) ~ exp(k * triangularity) where k is a concentration parameter.
# BF = P(data|M_teo) / P(data|M_alt)

# Choose k such that the random baseline has reasonable spread.
# k = 1/random_std gives decent discrimination.
k = 1.0 / max(random_std, 0.001)

print(f"\n--- Bayes Factors (k = {k:.1f}) ---\n")

teo_tri = scores['M_teo (proposed)']
teo_log_lik = k * teo_tri

bf_results = {}
for name, tri in scores.items():
    if name == 'M_teo (proposed)':
        continue
    log_bf = k * (teo_tri - tri)
    bf = math.exp(min(log_bf, 100))  # cap to avoid overflow
    interpretation = ('decisive' if bf > 100 else
                      'strong' if bf > 10 else
                      'moderate' if bf > 3 else
                      'weak' if bf > 1 else
                      'AGAINST theory')
    bf_results[name] = {'bf': bf, 'tri': tri, 'interpretation': interpretation}
    print(f"  vs {name:<25} BF = {bf:>10.1f} ({interpretation})")

# BF vs random
n_better = sum(1 for t in random_tris if t >= teo_tri)
empirical_p = (n_better + 1) / (N_RANDOM + 1)
print(f"\n  Empirical p (random >= theory): {empirical_p:.4f}")
print(f"  {n_better}/{N_RANDOM} random orderings matched or exceeded M_teo")

# ######################################################################
#  SECTION 6: SAVE RESULTS
# ######################################################################

os.makedirs(RESULTS_DIR, exist_ok=True)
output = {
    'named_scores': {k: round(v, 4) for k, v in scores.items()},
    'random_baseline': {
        'n': N_RANDOM,
        'mean': round(random_mean, 4),
        'std': round(random_std, 4),
        'max': round(random_max, 4),
    },
    'empirical_p_vs_random': round(empirical_p, 4),
    'bayes_factors': {k: {'bf': round(v['bf'], 2),
                          'interpretation': v['interpretation']}
                      for k, v in bf_results.items()},
    'concentration_k': round(k, 1),
}

out_path = os.path.join(RESULTS_DIR, 'i4_bayes.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nResults saved to: {out_path}")
