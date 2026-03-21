"""Fase 10: Emergence Analysis — 14 Dualidades.

Extends emergence_analysis.py from 7 to 14 dualidades (circle + spiral).
Adds tree verification, cross-spiral analysis, and before/after comparison.

11 sections: dependency matrix, DAG rank, D-rate, ejes, counterfactual,
reverse deps, tree verification, cross-spiral, before/after, synthesis.
Solo stdlib: json, math, sys, os, collections.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import math
import os
from collections import defaultdict, deque

# ######################################################################
#  SECTION 0: DATA LOADING
# ######################################################################

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data')

with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
    prim_data = json.load(f)

with open(os.path.join(DATA_DIR, 'reference_domains.json'), 'r', encoding='utf-8') as f:
    dom_data = json.load(f)

with open(os.path.join(DATA_DIR, 'dualidad_primitivo_map.json'), 'r', encoding='utf-8') as f:
    dual_data = json.load(f)

prims = prim_data['primitivos']
names = [p['nombre'] for p in prims]
name_set = set(names)
deps_map = {p['nombre']: list(p['deps']) for p in prims}
capa_map = {p['nombre']: p['capa'] for p in prims}

# Build DAG
children = defaultdict(set)
parents = defaultdict(set)
dep_pairs = []
for p in prims:
    for d in p['deps']:
        children[d].add(p['nombre'])
        parents[p['nombre']].add(d)
        dep_pairs.append((d, p['nombre']))

total_edges = len(dep_pairs)

# Duality orderings
# NOTE (from i4_bayesian_orders.py): This order is significantly better than
# random (p=0.005, only 4/1000 exceed it) and decisively better than reversed
# (BF=121.4). However, Hegel-inspired and Peirce-inspired orderings achieve
# comparable triangularity (BF=1.1 and 1.9 respectively). This is ONE valid
# ordering, not THE unique ordering.
CIRCLE_ORDER = ['D1_existir', 'D2_espacio', 'D3_tiempo',
                'D4_posibilidad', 'D5_identidad', 'D6_movimiento', 'D7_orden']
SPIRAL_ORDER = ['D8_uno_muchos', 'D9_dentro_fuera', 'D10_parte_todo',
                'D11_vida_muerte', 'D12_causa_efecto',
                'D13_semejante_diferente', 'D14_sujeto_objeto']
ALL_14 = CIRCLE_ORDER + SPIRAL_ORDER

CIRCLE_LABELS = {k: i + 1 for i, k in enumerate(CIRCLE_ORDER)}
SPIRAL_LABELS = {k: i + 1 for i, k in enumerate(SPIRAL_ORDER)}
ALL_LABELS = {k: i + 1 for i, k in enumerate(ALL_14)}

# Expected tree for D8-D14
SPIRAL_TREE = {
    'D8_uno_muchos': [],
    'D9_dentro_fuera': ['D8_uno_muchos'],
    'D10_parte_todo': ['D9_dentro_fuera'],
    'D11_vida_muerte': ['D10_parte_todo'],
    'D12_causa_efecto': ['D8_uno_muchos'],
    'D13_semejante_diferente': ['D8_uno_muchos'],
    'D14_sujeto_objeto': ['D11_vida_muerte'],
}

dualidades = dual_data['dualidades']
STATE_VAL = {'D': 2, 'A': 1, 'N': 0}

short = {k: k.split('_')[0] + '_' + k.split('_')[1][:4] for k in ALL_14}

print('=' * 78)
print('  EMERGENCE SEQUENCE ANALYSIS — 14 DUALIDADES')
print(f'  {len(ALL_14)} Dualidades x {len(prims)} Primitivos x {total_edges} Edges x '
      f'{len(dom_data["domains"])} Domains')
print('=' * 78)
print()

# ######################################################################
#  SECTION 1: TRANSITIVE CLOSURE
# ######################################################################

def compute_ancestors(node, parents_map, cache):
    """BFS to compute all transitive ancestors of a node."""
    if node in cache:
        return cache[node]
    result = set()
    queue = deque(list(parents_map.get(node, set())))
    while queue:
        n = queue.popleft()
        if n not in result:
            result.add(n)
            for p in parents_map.get(n, set()):
                if p not in result:
                    queue.append(p)
    cache[node] = result
    return result

ancestor_cache = {}
ancestors = {n: compute_ancestors(n, parents, ancestor_cache) for n in names}

roots = [n for n in names if not parents.get(n)]
for r in roots:
    assert len(ancestors[r]) == 0, f'Root {r} should have no ancestors'

print(f'Transitive closure computed for {len(names)} primitives.')
print(f'  Roots ({len(roots)}): {", ".join(roots)}')
print()

# ######################################################################
#  SECTION 2: DEPENDENCY MATRIX 14x14
# ######################################################################

print('=' * 78)
print('  DEPENDENCY MATRIX 14x14')
print('  Fraction of Dj anchors depending transitively on Di anchors')
print('=' * 78)
print()

def get_anchors(dkey):
    return dualidades[dkey]['anclas']

dep_matrix = {}
for di in ALL_14:
    dep_matrix[di] = {}
    di_anchors = set(get_anchors(di))
    for dj in ALL_14:
        if di == dj:
            dep_matrix[di][dj] = None
            continue
        dj_anchors = get_anchors(dj)
        if not dj_anchors:
            dep_matrix[di][dj] = 0.0
            continue
        count = sum(1 for a in dj_anchors if ancestors[a] & di_anchors)
        dep_matrix[di][dj] = count / len(dj_anchors)


def print_block(row_keys, col_keys, title):
    """Print a submatrix block of dep_matrix."""
    print(f'  {title}')
    hdr = ' ' * 14
    for k in col_keys:
        hdr += f'{short[k]:>8}'
    print(hdr)
    for di in row_keys:
        row_str = f'  {short[di]:<12}'
        for dj in col_keys:
            v = dep_matrix[di][dj]
            if v is None:
                row_str += f'{"---":>8}'
            else:
                row_str += f'{v:>8.2f}'
        print(row_str)
    print()


def block_triangularity(row_keys, col_keys):
    """Triangularity relative to ALL_14 ordering."""
    above_s, below_s = 0.0, 0.0
    for di in row_keys:
        pi = ALL_14.index(di)
        for dj in col_keys:
            v = dep_matrix[di][dj]
            if v is None or v == 0:
                continue
            pj = ALL_14.index(dj)
            if pi < pj:
                above_s += v
            elif pi > pj:
                below_s += v
    total = above_s + below_s
    tri = above_s / total if total > 0 else 0.0
    return tri, above_s, below_s


# Block 1: Circle x Circle
print_block(CIRCLE_ORDER, CIRCLE_ORDER, 'Block 1: Circle x Circle (D1-D7 x D1-D7)')
tri_cc, ab_cc, bl_cc = block_triangularity(CIRCLE_ORDER, CIRCLE_ORDER)
print(f'    Triangularity: {tri_cc:.3f}  (above={ab_cc:.2f}, below={bl_cc:.2f})')
print()

# Block 2: Circle x Spiral
print_block(CIRCLE_ORDER, SPIRAL_ORDER, 'Block 2: Circle x Spiral (D1-D7 x D8-D14)')
tri_cs, ab_cs, bl_cs = block_triangularity(CIRCLE_ORDER, SPIRAL_ORDER)
dep_cs_total = sum(dep_matrix[di][dj] for di in CIRCLE_ORDER for dj in SPIRAL_ORDER
                   if dep_matrix[di][dj] is not None and dep_matrix[di][dj] > 0)
print(f'    Forward coupling (circle -> spiral): {dep_cs_total:.2f} total weight')
print()

# Block 3: Spiral x Circle
print_block(SPIRAL_ORDER, CIRCLE_ORDER, 'Block 3: Spiral x Circle (D8-D14 x D1-D7)')
dep_sc_total = sum(dep_matrix[di][dj] for di in SPIRAL_ORDER for dj in CIRCLE_ORDER
                   if dep_matrix[di][dj] is not None and dep_matrix[di][dj] > 0)
print(f'    Reverse coupling (spiral -> circle): {dep_sc_total:.2f} total weight')
print()

# Block 4: Spiral x Spiral
print_block(SPIRAL_ORDER, SPIRAL_ORDER, 'Block 4: Spiral x Spiral (D8-D14 x D8-D14)')
tri_ss, ab_ss, bl_ss = block_triangularity(SPIRAL_ORDER, SPIRAL_ORDER)
print(f'    Triangularity: {tri_ss:.3f}  (above={ab_ss:.2f}, below={bl_ss:.2f})')
print()

# Overall
tri_all, ab_all, bl_all = block_triangularity(ALL_14, ALL_14)
print(f'  Overall 14x14 triangularity: {tri_all:.3f}  '
      f'(above={ab_all:.2f}, below={bl_all:.2f})')
print()

# ######################################################################
#  SECTION 3: DAG EMERGENCE RANK
# ######################################################################

print('=' * 78)
print('  DAG EMERGENCE RANK — 14 DUALIDADES')
print('  Avg depth of anchors per duality vs position')
print('=' * 78)
print()

depth_map = {}
bfs_queue = deque()
for r in roots:
    depth_map[r] = 0
    bfs_queue.append(r)

while bfs_queue:
    node = bfs_queue.popleft()
    for ch in children.get(node, set()):
        candidate = depth_map[node] + 1
        if ch not in depth_map or candidate < depth_map[ch]:
            depth_map[ch] = candidate
            bfs_queue.append(ch)

avg_depths = {}
for dk in ALL_14:
    anch = get_anchors(dk)
    depths = [depth_map.get(a, 0) for a in anch]
    avg_depths[dk] = sum(depths) / len(depths) if depths else 0.0


def spearman(ranks_x, ranks_y):
    """Spearman rank correlation."""
    n = len(ranks_x)
    if n < 3:
        return 0.0
    d_sq = sum((rx - ry) ** 2 for rx, ry in zip(ranks_x, ranks_y))
    return 1 - 6 * d_sq / (n * (n * n - 1))


def log_gamma(z):
    """Lanczos approximation for ln(Gamma(z))."""
    if z <= 0:
        return float('inf')
    coeffs = [
        76.18009172947146, -86.50532032941677,
        24.01409824083091, -1.231739572450155,
        0.1208650973866179e-2, -0.5395239384953e-5
    ]
    x = z
    y = z
    tmp = x + 5.5
    tmp = (x + 0.5) * math.log(tmp) - tmp
    ser = 1.000000000190015
    for c in coeffs:
        y += 1.0
        ser += c / y
    return tmp + math.log(2.5066282746310005 * ser / x)


def beta_fn(a, b):
    """Beta function B(a,b) = Gamma(a)*Gamma(b)/Gamma(a+b)."""
    return math.exp(log_gamma(a) + log_gamma(b) - log_gamma(a + b))


def regularized_beta_cf(x, a, b, max_iter=200, tol=1e-10):
    """Regularized incomplete beta I_x(a,b) via continued fraction (Lentz)."""
    if x < 0 or x > 1:
        return 0.0
    if x == 0:
        return 0.0
    if x == 1:
        return 1.0

    # Use symmetry if x > (a+1)/(a+b+2) for better convergence
    if x > (a + 1.0) / (a + b + 2.0):
        return 1.0 - regularized_beta_cf(1.0 - x, b, a, max_iter, tol)

    # Front factor
    lbeta = log_gamma(a + b) - log_gamma(a) - log_gamma(b)
    front = math.exp(lbeta + a * math.log(x) + b * math.log(1.0 - x)) / a

    # Continued fraction via modified Lentz's method
    TINY = 1e-30
    f = TINY
    c = TINY
    d = 0.0

    for m in range(0, max_iter):
        if m == 0:
            a_m = 1.0
        else:
            m_half = m // 2
            if m % 2 == 0:
                num = m_half * (b - m_half) * x
                den = (a + m - 1) * (a + m)
            else:
                num = -(a + m_half) * (a + b + m_half) * x
                den = (a + 2 * m_half) * (a + 2 * m_half + 1)
            a_m = num / den if den != 0 else 0.0

        d = 1.0 + a_m * d
        if abs(d) < TINY:
            d = TINY
        d = 1.0 / d

        c = 1.0 + a_m / c
        if abs(c) < TINY:
            c = TINY

        delta = c * d
        f *= delta

        if abs(delta - 1.0) < tol:
            break

    return front * f


def t_to_pvalue(t_stat, df):
    """Two-tailed p-value from t-statistic using incomplete beta."""
    if df <= 0:
        return 1.0
    x = df / (df + t_stat * t_stat)
    p_one_tail = 0.5 * regularized_beta_cf(x, df / 2.0, 0.5)
    return 2.0 * p_one_tail


def spearman_pvalue(rho, n):
    """Exact two-tailed p-value for Spearman via t-distribution."""
    if n < 4 or abs(rho) >= 1.0:
        return 0.0
    t = rho * math.sqrt((n - 2) / (1.0 - rho * rho))
    df = n - 2
    return t_to_pvalue(t, df)


def depth_rank_analysis(order, labels, title):
    """Depth rank + Spearman for a group of dualidades."""
    sorted_d = sorted(order, key=lambda k: avg_depths[k])
    d_rank = {k: i + 1 for i, k in enumerate(sorted_d)}

    print(f'  {title}')
    print(f'  {"Dualidad":<20} {"Avg.Depth":>10} {"Rank":>6} {"Pos":>5} {"D":>4}')
    print(f'  {"-"*20} {"-"*10} {"-"*6} {"-"*5} {"-"*4}')
    for dk in order:
        pos = labels[dk]
        rank = d_rank[dk]
        delta = rank - pos
        flag = ' <- mismatch' if abs(delta) >= 3 else ''
        print(f'  {short[dk]:<20} {avg_depths[dk]:>10.2f} {rank:>6} '
              f'{pos:>5} {delta:>+4d}{flag}')

    pos_r = [labels[dk] for dk in order]
    dep_r = [d_rank[dk] for dk in order]
    rho = spearman(pos_r, dep_r)
    p = spearman_pvalue(rho, len(order))
    print(f'\n  Spearman rho = {rho:.3f}  (p ~ {p:.3f})')
    print()
    return rho, p, d_rank


rho_depth_c, p_depth_c, drank_c = depth_rank_analysis(
    CIRCLE_ORDER, CIRCLE_LABELS, 'Circle (D1-D7)')
rho_depth_s, p_depth_s, drank_s = depth_rank_analysis(
    SPIRAL_ORDER, SPIRAL_LABELS, 'Spiral (D8-D14)')
rho_depth_a, p_depth_a, drank_a = depth_rank_analysis(
    ALL_14, ALL_LABELS, 'Combined (D1-D14)')

# ######################################################################
#  SECTION 4: EMPIRICAL UNIVERSALITY (D-rate)
# ######################################################################

print('=' * 78)
print('  EMPIRICAL UNIVERSALITY — D-rate')
print('  Avg D-rate of anchors per duality across 9 domains')
print('=' * 78)
print()

domains = dom_data['domains']
domain_names = sorted(domains.keys())
n_domains = len(domain_names)

d_rate = {}
for pname in names:
    d_count = sum(1 for dn in domain_names if domains[dn]['classes'].get(pname, 'N') == 'D')
    d_rate[pname] = d_count / n_domains

avg_drate = {}
for dk in ALL_14:
    anch = get_anchors(dk)
    rates = [d_rate[a] for a in anch]
    avg_drate[dk] = sum(rates) / len(rates) if rates else 0.0


def drate_rank_analysis(order, labels, title):
    """D-rate rank + Spearman for a group of dualidades."""
    sorted_d = sorted(order, key=lambda k: -avg_drate[k])
    dr_rank = {k: i + 1 for i, k in enumerate(sorted_d)}

    print(f'  {title}')
    print(f'  {"Dualidad":<20} {"Avg.D-rate":>10} {"Rank":>6} {"Pos":>5} {"D":>4}')
    print(f'  {"-"*20} {"-"*10} {"-"*6} {"-"*5} {"-"*4}')
    for dk in order:
        pos = labels[dk]
        rank = dr_rank[dk]
        delta = rank - pos
        flag = ' <- mismatch' if abs(delta) >= 3 else ''
        print(f'  {short[dk]:<20} {avg_drate[dk]:>10.3f} {rank:>6} '
              f'{pos:>5} {delta:>+4d}{flag}')

    pos_r = [labels[dk] for dk in order]
    dep_r = [dr_rank[dk] for dk in order]
    rho = spearman(pos_r, dep_r)
    p = spearman_pvalue(rho, len(order))
    print(f'\n  Spearman rho = {rho:.3f}  (p ~ {p:.3f})')
    print()
    return rho, p, dr_rank


rho_drate_c, p_drate_c, drrank_c = drate_rank_analysis(
    CIRCLE_ORDER, CIRCLE_LABELS, 'Circle (D1-D7)')
rho_drate_s, p_drate_s, drrank_s = drate_rank_analysis(
    SPIRAL_ORDER, SPIRAL_LABELS, 'Spiral (D8-D14)')
rho_drate_a, p_drate_a, drrank_a = drate_rank_analysis(
    ALL_14, ALL_LABELS, 'Combined (D1-D14)')

# ######################################################################
#  SECTION 5: EJE-TO-DUALITY MAPPING
# ######################################################################

print('=' * 78)
print('  EJE-TO-DUALITY MAPPING — 14 DUALIDADES')
print(f'  Mapping {len(prim_data["ejes_duales"])} dual axes to 14 dualidades')
print('=' * 78)
print()

ejes = prim_data['ejes_duales']

# Build lookup: primitive -> duality (anchor priority, then secondary)
prim_to_dual = {}
prim_to_role = {}
for dk in ALL_14:
    for a in dualidades[dk]['anclas']:
        if a not in prim_to_dual:
            prim_to_dual[a] = dk
            prim_to_role[a] = 'anchor'
    for s in dualidades[dk]['secundarios']:
        if s not in prim_to_dual:
            prim_to_dual[s] = dk
            prim_to_role[s] = 'secondary'

print(f'  {"Eje":<30} {"Capa":>5} {"Polo+":<15} {"Polo-":<15} {"Dualidad":<12}')
print(f'  {"-"*30} {"-"*5} {"-"*15} {"-"*15} {"-"*12}')

eje_duality_count = defaultdict(int)
unassigned_ejes = []

for polo_a, polo_b in ejes:
    capa = capa_map.get(polo_a, '?')
    dual_a = prim_to_dual.get(polo_a)
    dual_b = prim_to_dual.get(polo_b)
    if dual_a and dual_b and dual_a == dual_b:
        assigned = dual_a
    elif dual_a:
        assigned = dual_a
    elif dual_b:
        assigned = dual_b
    else:
        assigned = None
        unassigned_ejes.append((polo_a, polo_b))
    if assigned:
        eje_duality_count[assigned] += 1
    label = short.get(assigned, '---') if assigned else '---'
    print(f'  {polo_a + "/" + polo_b:<30} {capa:>5} {polo_a:<15} {polo_b:<15} {label:<12}')

print()
print('  Ejes per duality:')
for dk in ALL_14:
    count = eje_duality_count.get(dk, 0)
    if count > 0:
        bar = '#' * count
        print(f'    {short[dk]:<15} {count:>2}  {bar}')

assigned_count = sum(eje_duality_count.values())
print(f'\n  Assigned: {assigned_count}/{len(ejes)} ejes')
if unassigned_ejes:
    print(f'  Unassigned: {unassigned_ejes}')
print()

# ######################################################################
#  SECTION 6: COUNTERFACTUAL NECESSITY TEST
# ######################################################################

print('=' * 78)
print('  COUNTERFACTUAL NECESSITY TEST — 14 DUALIDADES')
print('  C(14,2) = 91 pairs. If Di->D and Dj->N, does monotonicity collapse?')
print('=' * 78)
print()


def compute_monotonicity(assignment):
    """Fraction of edges where child_state <= parent_state."""
    violations = 0
    for parent, child in dep_pairs:
        pval = STATE_VAL.get(assignment.get(parent, 'A'), 1)
        cval = STATE_VAL.get(assignment.get(child, 'A'), 1)
        if cval > pval:
            violations += 1
    return 1 - violations / len(dep_pairs) if dep_pairs else 1.0


real_monos = [compute_monotonicity(domains[dn]['classes']) for dn in domain_names]
baseline_mono = sum(real_monos) / len(real_monos)
threshold = 0.80

print(f'  Baseline avg monotonicity: {baseline_mono:.3f}')
print(f'  Threshold: {threshold}')
print()

counter_results = []
for i, di in enumerate(ALL_14):
    for j, dj in enumerate(ALL_14):
        if i >= j:
            continue
        synth = {}
        di_anchors = set(get_anchors(di))
        dj_anchors = set(get_anchors(dj))
        for pname in names:
            if pname in dj_anchors:
                synth[pname] = 'D'
            elif pname in di_anchors:
                synth[pname] = 'N'
            else:
                synth[pname] = 'A'
        mono = compute_monotonicity(synth)
        if mono < threshold:
            interp = 'NECESSARY'
        elif mono < baseline_mono - 0.05:
            interp = 'WEAK'
        else:
            interp = 'UNCERTAIN'
        counter_results.append((di, dj, mono, interp))

# Group by interpretation
by_interp = defaultdict(list)
for di, dj, mono, interp in counter_results:
    by_interp[interp].append((di, dj, mono))

for cat in ['NECESSARY', 'WEAK', 'UNCERTAIN']:
    items = by_interp.get(cat, [])
    print(f'  {cat}: {len(items)}/91 pairs')
    if cat == 'NECESSARY' and items:
        for di, dj, mono in sorted(items, key=lambda x: x[2]):
            print(f'    {short[di]}->{short[dj]}: mono={mono:.3f}')
    elif cat == 'WEAK' and items:
        for di, dj, mono in sorted(items, key=lambda x: x[2])[:10]:
            print(f'    {short[di]}->{short[dj]}: mono={mono:.3f}')
        if len(items) > 10:
            print(f'    ... and {len(items) - 10} more')
print()

# ######################################################################
#  SECTION 7: REVERSE DEPENDENCY CHECK
# ######################################################################

print('=' * 78)
print('  REVERSE DEPENDENCY CHECK — 14 DUALIDADES')
print('  Bidirectional dependencies -> lattice structure?')
print('=' * 78)
print()

bidirectional_pairs = []
forward_only = []
reverse_only = []
independent = []

for i, di in enumerate(ALL_14):
    for j, dj in enumerate(ALL_14):
        if i >= j:
            continue
        fwd = dep_matrix[di][dj] or 0.0
        rev = dep_matrix[dj][di] or 0.0
        if fwd > 0 and rev > 0:
            bidirectional_pairs.append((di, dj, fwd, rev))
        elif fwd > 0:
            forward_only.append((di, dj, fwd))
        elif rev > 0:
            reverse_only.append((di, dj, rev))
        else:
            independent.append((di, dj))

print(f'  Forward only:    {len(forward_only)}')
print(f'  Reverse only:    {len(reverse_only)}')
print(f'  Bidirectional:   {len(bidirectional_pairs)}')
print(f'  Independent:     {len(independent)}')
print()

if bidirectional_pairs:
    print('  Bidirectional pairs:')
    for di, dj, fwd, rev in sorted(bidirectional_pairs, key=lambda x: -(x[2]+x[3])):
        print(f'    {short[di]} <-> {short[dj]}: fwd={fwd:.2f}, rev={rev:.2f}')
    print()

if reverse_only:
    print('  Reverse-only pairs (tensions):')
    for di, dj, rev in sorted(reverse_only, key=lambda x: -x[2])[:10]:
        print(f'    {short[dj]}->{short[di]}: {rev:.2f}')
    if len(reverse_only) > 10:
        print(f'    ... and {len(reverse_only) - 10} more')
    print()

# ######################################################################
#  SECTION 8: TREE VERIFICATION (D8-D14)
# ######################################################################

print('=' * 78)
print('  TREE VERIFICATION — SPIRAL D8-D14')
print('  Does the dependency matrix reproduce the expected tree?')
print('=' * 78)
print()

# Expected edges from SPIRAL_TREE
expected_edges = []
for child_dk, parent_list in SPIRAL_TREE.items():
    for parent_dk in parent_list:
        expected_edges.append((parent_dk, child_dk))

print(f'  Expected tree edges: {len(expected_edges)}')
print()

confirmed = 0
print(f'  {"Edge":<35} {"dep_matrix":>10} {"Status":>10}')
print(f'  {"-"*35} {"-"*10} {"-"*10}')

for parent_dk, child_dk in expected_edges:
    v = dep_matrix[parent_dk][child_dk]
    if v is None:
        v = 0.0
    status = 'OK' if v > 0 else 'MISSING'
    if v > 0:
        confirmed += 1
    print(f'  {short[parent_dk] + " -> " + short[child_dk]:<35} {v:>10.2f} {status:>10}')

tree_fidelity = confirmed / len(expected_edges) if expected_edges else 0.0
print()
print(f'  Tree fidelity (edge recall): {confirmed}/{len(expected_edges)} = {tree_fidelity:.3f}')

# Check for unexpected edges within D8-D14 (non-tree edges with dep > 0)
unexpected = []
for di in SPIRAL_ORDER:
    for dj in SPIRAL_ORDER:
        if di == dj:
            continue
        v = dep_matrix[di][dj]
        if v is None or v == 0:
            continue
        if (di, dj) not in expected_edges:
            unexpected.append((di, dj, v))

print(f'  Unexpected non-tree edges (dep > 0): {len(unexpected)}')
if unexpected:
    for di, dj, v in sorted(unexpected, key=lambda x: -x[2]):
        # Check if this is explained by transitivity
        tree_path = (di, dj) not in expected_edges
        print(f'    {short[di]} -> {short[dj]}: {v:.2f}')

# Missing edges: why?
missing_edges = [(p, c) for p, c in expected_edges
                 if (dep_matrix[p][c] or 0.0) == 0.0]
if missing_edges:
    print()
    print('  Analysis of missing edges:')
    for parent_dk, child_dk in missing_edges:
        p_anchors = get_anchors(parent_dk)
        c_anchors = get_anchors(child_dk)
        print(f'    {short[parent_dk]} -> {short[child_dk]}:')
        print(f'      Parent anchors: {p_anchors}')
        print(f'      Child anchors: {c_anchors}')
        for ca in c_anchors:
            anc = ancestors[ca]
            hits = anc & set(p_anchors)
            print(f'      {ca} ancestors contain parent anchors? '
                  f'{"YES: " + str(hits) if hits else "NO"}')

verdict_tree = 'PASS' if tree_fidelity >= 0.80 else 'FAIL'
print(f'\n  Verdict: {verdict_tree} (threshold >= 0.80)')
print()

# ######################################################################
#  SECTION 9: CROSS-SPIRAL ANALYSIS
# ######################################################################

print('=' * 78)
print('  CROSS-SPIRAL ANALYSIS')
print('  Dependencies between circle (D1-D7) and spiral (D8-D14)')
print('=' * 78)
print()

# Identify bridge primitives (appear in both spirals)
circle_prims = set()
for dk in CIRCLE_ORDER:
    circle_prims.update(dualidades[dk]['anclas'])
    circle_prims.update(dualidades[dk]['secundarios'])

spiral_prims = set()
for dk in SPIRAL_ORDER:
    spiral_prims.update(dualidades[dk]['anclas'])
    spiral_prims.update(dualidades[dk]['secundarios'])

bridge = sorted(circle_prims & spiral_prims)
print(f'  Bridge primitives (in both spirals): {len(bridge)}')
for bp in bridge:
    # Find which dualidades this primitive belongs to
    circle_dualities = [dk for dk in CIRCLE_ORDER
                        if bp in dualidades[dk]['anclas'] or bp in dualidades[dk]['secundarios']]
    spiral_dualities = [dk for dk in SPIRAL_ORDER
                        if bp in dualidades[dk]['anclas'] or bp in dualidades[dk]['secundarios']]
    c_str = ', '.join(short[d] for d in circle_dualities)
    s_str = ', '.join(short[d] for d in spiral_dualities)
    role_c = 'A' if any(bp in dualidades[dk]['anclas'] for dk in circle_dualities) else 'S'
    role_s = 'A' if any(bp in dualidades[dk]['anclas'] for dk in spiral_dualities) else 'S'
    print(f'    {bp:<20} circle: {c_str:<20} ({role_c})  '
          f'spiral: {s_str:<20} ({role_s})')
print()

# Cross-dependencies: circle -> spiral
print('  Circle -> Spiral dependencies (top entries):')
cs_deps = []
for di in CIRCLE_ORDER:
    for dj in SPIRAL_ORDER:
        v = dep_matrix[di][dj]
        if v and v > 0:
            cs_deps.append((di, dj, v))
cs_deps.sort(key=lambda x: -x[2])
for di, dj, v in cs_deps[:15]:
    print(f'    {short[di]} -> {short[dj]}: {v:.2f}')
print(f'  Total: {len(cs_deps)} pairs with dep > 0')
print()

# Cross-dependencies: spiral -> circle
print('  Spiral -> Circle dependencies (reverse coupling):')
sc_deps = []
for di in SPIRAL_ORDER:
    for dj in CIRCLE_ORDER:
        v = dep_matrix[di][dj]
        if v and v > 0:
            sc_deps.append((di, dj, v))
sc_deps.sort(key=lambda x: -x[2])
for di, dj, v in sc_deps[:15]:
    # These are "spiral influences circle" — identify mechanism
    di_anchors = set(get_anchors(di))
    dj_anchors = get_anchors(dj)
    shared = di_anchors & circle_prims
    print(f'    {short[di]} -> {short[dj]}: {v:.2f}  '
          f'(via shared: {", ".join(sorted(di_anchors & set(bridge)))})')
print(f'  Total: {len(sc_deps)} pairs with dep > 0')
print()

# ######################################################################
#  SECTION 10: BEFORE/AFTER COMPARISON
# ######################################################################

print('=' * 78)
print('  BEFORE/AFTER: 7x7 vs 14x14')
print('=' * 78)
print()

print(f'  {"Metric":<35} {"7x7 (circle)":>14} {"14x14 (all)":>14}')
print(f'  {"-"*35} {"-"*14} {"-"*14}')
print(f'  {"Triangularity":<35} {tri_cc:>14.3f} {tri_all:>14.3f}')
print(f'  {"Spearman rho (depth)":<35} {rho_depth_c:>14.3f} {rho_depth_a:>14.3f}')
print(f'  {"Spearman rho (D-rate)":<35} {rho_drate_c:>14.3f} {rho_drate_a:>14.3f}')
print(f'  {"p-value (depth)":<35} {p_depth_c:>14.3f} {p_depth_a:>14.3f}')
print(f'  {"p-value (D-rate)":<35} {p_drate_c:>14.3f} {p_drate_a:>14.3f}')

# Counterfactual stats for 7x7 vs 14x14
nec_7 = sum(1 for di, dj, m, interp in counter_results
            if interp == 'NECESSARY' and di in CIRCLE_ORDER and dj in CIRCLE_ORDER)
nec_14 = sum(1 for _, _, _, interp in counter_results if interp == 'NECESSARY')
total_7 = sum(1 for di, dj, _, _ in counter_results
              if di in CIRCLE_ORDER and dj in CIRCLE_ORDER)
total_14 = len(counter_results)
print(f'  {"Necessary pairs":<35} {str(nec_7) + "/" + str(total_7):>14} '
      f'{str(nec_14) + "/" + str(total_14):>14}')
print(f'  {"Bidirectional pairs":<35} '
      f'{sum(1 for di, dj, _, _ in bidirectional_pairs if di in CIRCLE_ORDER and dj in CIRCLE_ORDER):>14} '
      f'{len(bidirectional_pairs):>14}')
print(f'  {"Ejes assigned":<35} '
      f'{sum(eje_duality_count.get(dk, 0) for dk in CIRCLE_ORDER):>14} '
      f'{assigned_count:>14}')
print()

# FDR caveat (added by I1 audit)
print('=' * 78)
print('  FDR CAVEAT (from dualidademergente+reptimeline/internal/i1)')
print('=' * 78)
print()
print('  NONE of the Spearman correlations above survive Benjamini-Hochberg')
print('  FDR correction (alpha=0.05) when tested jointly with all 12 rank')
print('  correlations from Doc 34 + Doc 35. With n=7 and n=14, statistical')
print('  power is 0.14-0.45 — far below the 0.80 convention.')
print('  Triangularity and tree fidelity remain valid structural metrics.')
print()

# ######################################################################
#  SECTION 11: SYNTHESIS
# ######################################################################

print('=' * 78)
print('  SYNTHESIS — 14 DUALIDADES')
print('=' * 78)
print()

# Consolidated table
print(f'  {"Dualidad":<12} {"Pos":>4} {"Depth":>6} {"D-rate":>7} '
      f'{"DepSc":>6} {"Ejes":>5} {"CtrMono":>8} {"Spiral":>7}')
print(f'  {"-"*12} {"-"*4} {"-"*6} {"-"*7} {"-"*6} {"-"*5} {"-"*8} {"-"*7}')

for dk in ALL_14:
    pos = ALL_LABELS[dk]
    depth = avg_depths[dk]
    dr = avg_drate[dk]

    idx = ALL_14.index(dk)
    if idx == 0:
        dep_score = '---'
    else:
        earlier = ALL_14[:idx]
        scores = [dep_matrix[e][dk] for e in earlier
                  if dep_matrix[e][dk] is not None]
        dep_score = f'{sum(scores) / len(scores):.2f}' if scores else '---'

    ej = eje_duality_count.get(dk, 0)

    cmonos = [m for di, dj, m, _ in counter_results if di == dk or dj == dk]
    cmono = f'{sum(cmonos) / len(cmonos):.3f}' if cmonos else '---'

    spiral_marker = 'C' if dk in CIRCLE_ORDER else 'S'
    print(f'  {short[dk]:<12} {pos:>4} {depth:>6.2f} {dr:>7.3f} '
          f'{dep_score:>6} {ej:>5} {cmono:>8} {spiral_marker:>7}')

print()

# Correlations summary
print('  Correlations:')
print(f'    {"":>25} {"rho":>8} {"p":>8}')
print(f'    {"-"*25} {"-"*8} {"-"*8}')
for label, rho, p in [
    ('Depth (circle D1-D7)', rho_depth_c, p_depth_c),
    ('Depth (spiral D8-D14)', rho_depth_s, p_depth_s),
    ('Depth (combined D1-D14)', rho_depth_a, p_depth_a),
    ('D-rate (circle D1-D7)', rho_drate_c, p_drate_c),
    ('D-rate (spiral D8-D14)', rho_drate_s, p_drate_s),
    ('D-rate (combined D1-D14)', rho_drate_a, p_drate_a),
]:
    sig = '*' if p < 0.05 else (' ' if p < 0.10 else '')
    print(f'    {label:<25} {rho:>+8.3f} {p:>7.3f}{sig}')
print()

# D1 row check: everything should depend on D1
d1_deps = [(dj, dep_matrix['D1_existir'][dj])
           for dj in ALL_14 if dj != 'D1_existir']
d1_all_positive = all(v is not None and v > 0 for _, v in d1_deps)
d1_zeros = [(dj, v) for dj, v in d1_deps if v is not None and v == 0]
print(f'  D1 row check (all depend on Existir): '
      f'{"PASS" if d1_all_positive else "FAIL"}')
if d1_zeros:
    print(f'    Zero dependencies: {[short[dj] for dj, _ in d1_zeros]}')
print()

# Verdicts
print('  ' + '=' * 60)
print('  VERDICTS')
print('  ' + '=' * 60)
print()


def judge_verdict(tri, rho_d, rho_dr, p_d, p_dr, label):
    if tri >= 0.9 and rho_d > 0.7 and rho_dr > 0.7:
        v = 'SUPPORTED'
    elif tri >= 0.7 or (rho_d > 0.5 and rho_dr > 0.5):
        v = 'PARTIALLY SUPPORTED'
    else:
        v = 'CONTRADICTED'
    print(f'  {label}:')
    print(f'    Triangularity = {tri:.3f}, rho_depth = {rho_d:+.3f}, '
          f'rho_D-rate = {rho_dr:+.3f}')
    print(f'    -> {v}')
    return v


v_circle = judge_verdict(tri_cc, rho_depth_c, rho_drate_c,
                         p_depth_c, p_drate_c, 'Circle (D1-D7)')
print()
v_spiral = judge_verdict(tri_ss, rho_depth_s, rho_drate_s,
                         p_depth_s, p_drate_s, 'Spiral (D8-D14)')
print()
v_combined = judge_verdict(tri_all, rho_depth_a, rho_drate_a,
                           p_depth_a, p_drate_a, 'Combined (D1-D14)')
print()

# Tree verdict
print(f'  Tree fidelity: {tree_fidelity:.3f} '
      f'({"PASS" if tree_fidelity >= 0.80 else "FAIL"}, threshold 0.80)')
print()

# Structure type
if len(bidirectional_pairs) > 5:
    struct = 'LATTICE (many bidirectional links)'
elif bidirectional_pairs:
    struct = 'PARTIAL LATTICE (some bidirectional links)'
else:
    struct = 'STRICT CHAIN'
print(f'  Structure: {struct}')

# Cross-spiral
cs_strength = dep_cs_total / (7 * 7) if dep_cs_total else 0
sc_strength = dep_sc_total / (7 * 7) if dep_sc_total else 0
print(f'  Cross-spiral coupling: circle->spiral={cs_strength:.3f}, '
      f'spiral->circle={sc_strength:.3f}')
print(f'  Bridge primitives: {len(bridge)}/65')
print()

print('  ' + '=' * 60)
