"""I3: Sensitivity analysis — perturbation of primitivos.json.

Tests robustness by systematically perturbing dependencies, layers,
duals, and domain classifications. Reports which parts of the
framework are fragile.

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
deps_map = {p['nombre']: list(p['deps']) for p in prims}
capa_map = {p['nombre']: p['capa'] for p in prims}
total_L14 = sum(1 for p in prims if p['capa'] <= 4)
ejes = prim_data.get('ejes_duales', [])

CIRCLE_ORDER = ['D1_existir', 'D2_espacio', 'D3_tiempo',
                'D4_posibilidad', 'D5_identidad', 'D6_movimiento', 'D7_orden']
SPIRAL_ORDER = ['D8_uno_muchos', 'D9_dentro_fuera', 'D10_parte_todo',
                'D11_vida_muerte', 'D12_causa_efecto',
                'D13_semejante_diferente', 'D14_sujeto_objeto']
ALL_14 = CIRCLE_ORDER + SPIRAL_ORDER

SPIRAL_TREE = {
    'D8_uno_muchos': [],
    'D9_dentro_fuera': ['D8_uno_muchos'],
    'D10_parte_todo': ['D9_dentro_fuera'],
    'D11_vida_muerte': ['D10_parte_todo'],
    'D12_causa_efecto': ['D8_uno_muchos'],
    'D13_semejante_diferente': ['D8_uno_muchos'],
    'D14_sujeto_objeto': ['D11_vida_muerte'],
}


# ######################################################################
#  SECTION 1: METRIC FUNCTIONS (from emergence_analysis_14.py)
# ######################################################################

def build_dep_pairs(prim_list):
    """Build list of (parent, child) from primitivos."""
    pairs = []
    for p in prim_list:
        for d in p['deps']:
            pairs.append((d, p['nombre']))
    return pairs


def compute_ancestors(prim_list):
    """Compute transitive ancestors for each primitive via BFS."""
    deps = {p['nombre']: set(p['deps']) for p in prim_list}
    children_map = defaultdict(set)
    for p in prim_list:
        for d in p['deps']:
            children_map[d].add(p['nombre'])

    ancestors = {n: set() for n in deps}
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
    """Compute dependency matrix between dualidades.

    M[i][j] = fraction of Dj's anchor ancestors that are Dk's anchors.
    Triangularity = fraction of (i<j) pairs where M[i][j] > 0.
    """
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
    """Fraction of upper-triangle pairs where M[i][j] > 0."""
    above = 0
    total = 0
    for i in range(n):
        for j in range(i + 1, n):
            total += 1
            if matrix[i][j] > 0:
                above += 1
    return above / total if total > 0 else 0.0


def tree_fidelity(prim_list, dual_map, spiral_tree):
    """Check how many expected spiral tree edges are present."""
    ancestors = compute_ancestors(prim_list)
    verified = 0
    total = 0
    for child_d, parent_ds in spiral_tree.items():
        for parent_d in parent_ds:
            total += 1
            c_info = dual_map['dualidades'].get(child_d, {})
            p_info = dual_map['dualidades'].get(parent_d, {})
            c_anchors = set(c_info.get('anclas', []))
            p_anchors = set(p_info.get('anclas', []))
            # Check if any child anchor has any parent anchor as ancestor
            for ca in c_anchors:
                if ancestors.get(ca, set()) & p_anchors:
                    verified += 1
                    break
    return verified / total if total > 0 else 0.0


def compute_idvs(domain_classes, dep_pairs):
    """IDVS = Coverage_L14 * Monotonicity."""
    if total_L14 == 0:
        return 0.0
    nulls_L14 = sum(1 for name, cls in domain_classes.items()
                    if capa_map.get(name, 99) <= 4 and cls == 'N')
    coverage = 1.0 - nulls_L14 / total_L14

    rank = {'D': 2, 'A': 1, 'N': 0}
    total_pairs = 0
    ok_pairs = 0
    for parent, child in dep_pairs:
        if parent in domain_classes and child in domain_classes:
            total_pairs += 1
            if rank.get(domain_classes[child], 0) <= rank.get(domain_classes[parent], 0):
                ok_pairs += 1

    mono = ok_pairs / total_pairs if total_pairs > 0 else 1.0
    return coverage * mono


# ######################################################################
#  SECTION 2: BASELINE METRICS
# ######################################################################

dep_pairs = build_dep_pairs(prims)
ancestors = compute_ancestors(prims)
matrix = dependency_matrix(ALL_14, dual_data, ancestors)
baseline_tri = triangularity(matrix, 14)
baseline_tree = tree_fidelity(prims, dual_data, SPIRAL_TREE)

# Baseline IDVS (mean across positive domains)
positive_domains = {k: v for k, v in dom_data['domains'].items()
                    if k.lower() != 'astrology'}
baseline_idvs_list = []
for dom_name, dom_info in positive_domains.items():
    classes = dom_info.get('classes', dom_info)
    if isinstance(classes, dict) and 'classes' in classes:
        classes = classes['classes']
    baseline_idvs_list.append(compute_idvs(classes, dep_pairs))
baseline_idvs_mean = sum(baseline_idvs_list) / len(baseline_idvs_list)

print("=" * 70)
print("I3: Sensitivity Analysis of primitivos.json")
print("=" * 70)
print(f"\n  Baseline triangularity: {baseline_tri:.3f}")
print(f"  Baseline tree fidelity: {baseline_tree:.3f}")
print(f"  Baseline mean IDVS:    {baseline_idvs_mean:.3f}")

# ######################################################################
#  SECTION 3: PERTURBATION A — REMOVE ONE DEPENDENCY EDGE
# ######################################################################

N_REPS = 500
rng = random.Random(42)

print(f"\n--- Bloque A: Remove 1 dependency edge ({N_REPS} replicas) ---\n")

delta_tri_a = []
delta_tree_a = []

for _ in range(N_REPS):
    # Pick random edge to remove
    perturbed = deepcopy(prims)
    edges = [(p['nombre'], d) for p in perturbed for d in p['deps']]
    if not edges:
        continue
    child, parent = rng.choice(edges)
    for p in perturbed:
        if p['nombre'] == child and parent in p['deps']:
            p['deps'].remove(parent)
            break

    anc = compute_ancestors(perturbed)
    mat = dependency_matrix(ALL_14, dual_data, anc)
    tri = triangularity(mat, 14)
    tree = tree_fidelity(perturbed, dual_data, SPIRAL_TREE)
    delta_tri_a.append(tri - baseline_tri)
    delta_tree_a.append(tree - baseline_tree)

mean_delta_tri = sum(delta_tri_a) / len(delta_tri_a)
mean_delta_tree = sum(delta_tree_a) / len(delta_tree_a)
pct_big_tri = sum(1 for d in delta_tri_a if abs(d) > 0.05) / len(delta_tri_a)
pct_big_tree = sum(1 for d in delta_tree_a if abs(d) > 0.05) / len(delta_tree_a)

print(f"  Mean delta triangularity: {mean_delta_tri:+.4f}")
print(f"  % perturbations with |delta_tri| > 5%: {pct_big_tri*100:.1f}%")
print(f"  Mean delta tree fidelity: {mean_delta_tree:+.4f}")
print(f"  % perturbations with |delta_tree| > 5%: {pct_big_tree*100:.1f}%")

# ######################################################################
#  SECTION 4: PERTURBATION B — MOVE ONE PRIMITIVE TO ADJACENT LAYER
# ######################################################################

print(f"\n--- Bloque B: Move 1 primitive to adjacent layer ({N_REPS} replicas) ---\n")

delta_tri_b = []

for _ in range(N_REPS):
    perturbed = deepcopy(prims)
    idx = rng.randint(0, len(perturbed) - 1)
    p = perturbed[idx]
    direction = rng.choice([-1, 1])
    new_capa = max(1, min(6, p['capa'] + direction))
    p['capa'] = new_capa

    anc = compute_ancestors(perturbed)
    mat = dependency_matrix(ALL_14, dual_data, anc)
    tri = triangularity(mat, 14)
    delta_tri_b.append(tri - baseline_tri)

mean_delta_b = sum(delta_tri_b) / len(delta_tri_b)
pct_big_b = sum(1 for d in delta_tri_b if abs(d) > 0.02) / len(delta_tri_b)
print(f"  Mean delta triangularity: {mean_delta_b:+.4f}")
print(f"  % perturbations with |delta| > 2%: {pct_big_b*100:.1f}%")

# ######################################################################
#  SECTION 5: PERTURBATION C — FLIP 5% DOMAIN CLASSIFICATIONS
# ######################################################################

print(f"\n--- Bloque C: Flip 5% of D-A-N classifications ({N_REPS} replicas) ---\n")

delta_idvs_c = []
states = ['D', 'A', 'N']

for _ in range(N_REPS):
    deltas_per_domain = []
    for dom_name, dom_info in positive_domains.items():
        classes = dom_info.get('classes', dom_info)
        if isinstance(classes, dict) and 'classes' in classes:
            classes = classes['classes']
        perturbed_classes = dict(classes)

        # Flip 5% of classifications
        n_flip = max(1, int(0.05 * len(perturbed_classes)))
        flip_keys = rng.sample(list(perturbed_classes.keys()), n_flip)
        for k in flip_keys:
            current = perturbed_classes[k]
            alternatives = [s for s in states if s != current]
            perturbed_classes[k] = rng.choice(alternatives)

        new_idvs = compute_idvs(perturbed_classes, dep_pairs)
        orig_idvs = compute_idvs(classes, dep_pairs)
        deltas_per_domain.append(new_idvs - orig_idvs)

    mean_delta_dom = sum(deltas_per_domain) / len(deltas_per_domain)
    delta_idvs_c.append(mean_delta_dom)

mean_delta_c = sum(delta_idvs_c) / len(delta_idvs_c)
pct_big_c = sum(1 for d in delta_idvs_c if abs(d) > 0.05) / len(delta_idvs_c)
print(f"  Mean delta IDVS: {mean_delta_c:+.4f}")
print(f"  % perturbations with |delta_IDVS| > 5%: {pct_big_c*100:.1f}%")

# ######################################################################
#  SECTION 6: SAVE RESULTS
# ######################################################################

os.makedirs(RESULTS_DIR, exist_ok=True)
output = {
    'baseline': {
        'triangularity': round(baseline_tri, 4),
        'tree_fidelity': round(baseline_tree, 4),
        'mean_idvs': round(baseline_idvs_mean, 4),
    },
    'n_replicas': N_REPS,
    'perturbation_A_remove_edge': {
        'mean_delta_tri': round(mean_delta_tri, 4),
        'pct_big_tri': round(pct_big_tri, 4),
        'mean_delta_tree': round(mean_delta_tree, 4),
        'pct_big_tree': round(pct_big_tree, 4),
    },
    'perturbation_B_move_layer': {
        'mean_delta_tri': round(mean_delta_b, 4),
        'pct_big': round(pct_big_b, 4),
    },
    'perturbation_C_flip_dan': {
        'mean_delta_idvs': round(mean_delta_c, 4),
        'pct_big': round(pct_big_c, 4),
    },
}

out_path = os.path.join(RESULTS_DIR, 'i3_sensitivity.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nResults saved to: {out_path}")
