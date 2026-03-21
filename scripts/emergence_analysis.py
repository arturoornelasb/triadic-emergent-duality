"""Fase 7: Formalización Computable de la Secuencia de Emergencia.

Analiza computacionalmente si la secuencia del círculo de dualidades
(Existir→Espacio→Tiempo→Posibilidad→Identidad→Movimiento→Orden)
emerge de la estructura del DAG y de los datos empíricos de 9 dominios.

5 análisis: dependency matrix, DAG rank, D-rate, ejes, counterfactual.
Solo stdlib: json, math, sys, os, collections.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import math
import os
from collections import defaultdict, deque

# ######################################################################
#  SECTION 0: CLI + DATA LOADING
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

# Duality data
CIRCLE_ORDER = ['D1_existir', 'D2_espacio', 'D3_tiempo',
                'D4_posibilidad', 'D5_identidad', 'D6_movimiento', 'D7_orden']
CIRCLE_LABELS = {k: i + 1 for i, k in enumerate(CIRCLE_ORDER)}
dualidades = dual_data['dualidades']

# State ordering for monotonicity: D=2, A=1, N=0
STATE_VAL = {'D': 2, 'A': 1, 'N': 0}

print('=' * 78)
print('  EMERGENCE SEQUENCE ANALYSIS')
print(f'  7 Dualidades × {len(prims)} Primitivos × {total_edges} Edges × '
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

# Verification
roots = [n for n in names if not parents.get(n)]
for r in roots:
    assert len(ancestors[r]) == 0, f'Root {r} should have no ancestors'

print(f'Transitive closure computed for {len(names)} primitives.')
print(f'  Roots ({len(roots)}): {", ".join(roots)}')

# Sample verification: show ancestor counts for L6
l6 = [n for n in names if capa_map[n] == 6]
avg_l6 = sum(len(ancestors[n]) for n in l6) / len(l6) if l6 else 0
print(f'  L6 avg ancestors: {avg_l6:.1f} (nodes: {", ".join(l6)})')
print()

# ######################################################################
#  SECTION 2: DEPENDENCY MATRIX 7×7
# ######################################################################

print('=' * 78)
print('  DEPENDENCY MATRIX')
print('  Fraction of Dj anchors depending transitively on Di anchors')
print('=' * 78)
print()

def get_anchors(dkey):
    return dualidades[dkey]['anclas']

# Forward matrix: dep_matrix[i][j] = fraction of Dj anchors that
# have at least one Di anchor as transitive ancestor
dep_matrix = {}
for di in CIRCLE_ORDER:
    dep_matrix[di] = {}
    di_anchors = set(get_anchors(di))
    for dj in CIRCLE_ORDER:
        if di == dj:
            dep_matrix[di][dj] = None
            continue
        dj_anchors = get_anchors(dj)
        if not dj_anchors:
            dep_matrix[di][dj] = 0.0
            continue
        count = 0
        for a in dj_anchors:
            anc_a = ancestors[a]
            if anc_a & di_anchors:
                count += 1
        dep_matrix[di][dj] = count / len(dj_anchors)

# Print matrix
short = {k: k.split('_')[0] + '_' + k.split('_')[1][:4] for k in CIRCLE_ORDER}
header = '              ' + '  '.join(f'{short[k]:>6}' for k in CIRCLE_ORDER)
print(header)
for di in CIRCLE_ORDER:
    row = f'  {short[di]:<12}'
    for dj in CIRCLE_ORDER:
        v = dep_matrix[di][dj]
        if v is None:
            row += f'{"—":>8}'
        else:
            row += f'{v:>8.2f}'
    print(row)
print()

# Identify above/below diagonal
above_diag = []
below_diag = []
for i, di in enumerate(CIRCLE_ORDER):
    for j, dj in enumerate(CIRCLE_ORDER):
        if i == j:
            continue
        v = dep_matrix[di][dj]
        if v is not None and v > 0:
            if i < j:
                above_diag.append((di, dj, v))
            else:
                below_diag.append((di, dj, v))

print(f'  Above-diagonal (forward, expected): {len(above_diag)} pairs with deps > 0')
print(f'  Below-diagonal (reverse, tensions): {len(below_diag)} pairs with deps > 0')
print()

if below_diag:
    print('  BELOW-DIAGONAL (reverse dependencies — potential tensions):')
    for di, dj, v in sorted(below_diag, key=lambda x: -x[2]):
        di_a = get_anchors(di)
        dj_a = get_anchors(dj)
        # Find the specific anchors causing the reverse dependency
        details = []
        for a in get_anchors(dj):
            anc_a = ancestors[a]
            hits = anc_a & set(get_anchors(di))
            if hits:
                details.append(f'{a} depends on {", ".join(sorted(hits))}')
        label = ' ← TENSION' if CIRCLE_LABELS[di] > CIRCLE_LABELS[dj] else ''
        print(f'    {short[di]}→{short[dj]}: {v:.2f}  ({"; ".join(details)}){label}')
    print()

# ######################################################################
#  SECTION 3: DAG EMERGENCE RANK
# ######################################################################

print('=' * 78)
print('  DAG EMERGENCE RANK')
print('  Avg depth of anchors per duality vs circle position')
print('=' * 78)
print()

# Depth = minimum distance from any root (BFS from roots)
depth_map = {}
queue = deque()
for r in roots:
    depth_map[r] = 0
    queue.append(r)

while queue:
    node = queue.popleft()
    for ch in children.get(node, set()):
        # depth = min depth via any parent + 1
        candidate = depth_map[node] + 1
        if ch not in depth_map or candidate < depth_map[ch]:
            depth_map[ch] = candidate
            queue.append(ch)

# Avg depth per duality
avg_depths = {}
for dk in CIRCLE_ORDER:
    anchors = get_anchors(dk)
    depths = [depth_map.get(a, 0) for a in anchors]
    avg_depths[dk] = sum(depths) / len(depths) if depths else 0.0

# Rank by depth (lower depth = earlier rank)
sorted_by_depth = sorted(CIRCLE_ORDER, key=lambda k: avg_depths[k])
depth_rank = {k: i + 1 for i, k in enumerate(sorted_by_depth)}

print(f'  {"Dualidad":<20} {"Avg.Depth":>10} {"Rank":>6} {"Circle":>8} {"Δ":>4}')
print(f'  {"-"*20} {"-"*10} {"-"*6} {"-"*8} {"-"*4}')
for dk in CIRCLE_ORDER:
    circle_pos = CIRCLE_LABELS[dk]
    rank = depth_rank[dk]
    delta = rank - circle_pos
    flag = ' ← mismatch' if abs(delta) >= 3 else ''
    print(f'  {short[dk]:<20} {avg_depths[dk]:>10.2f} {rank:>6} {circle_pos:>8} {delta:>+4d}{flag}')

# Spearman correlation
def spearman(ranks_x, ranks_y):
    """Spearman rank correlation. Both are lists of ranks (1..n)."""
    n = len(ranks_x)
    if n < 3:
        return 0.0
    d_sq = sum((rx - ry) ** 2 for rx, ry in zip(ranks_x, ranks_y))
    rho = 1 - 6 * d_sq / (n * (n * n - 1))
    return rho

circle_ranks = [CIRCLE_LABELS[dk] for dk in CIRCLE_ORDER]
depth_ranks = [depth_rank[dk] for dk in CIRCLE_ORDER]
rho_depth = spearman(circle_ranks, depth_ranks)

# Approximate p-value for Spearman (t-test approximation)
def spearman_pvalue(rho, n):
    if n < 4 or abs(rho) >= 1.0:
        return 0.0
    t = rho * math.sqrt((n - 2) / (1 - rho * rho))
    # Approximate two-tailed p-value using t-distribution with n-2 df
    # For small n, use a rough approximation
    df = n - 2
    x = df / (df + t * t)
    # Regularized incomplete beta function approximation
    # For our purposes (n=7), hardcode critical values
    # t critical at p=0.05 for df=5: 2.571, p=0.10: 2.015
    abs_t = abs(t)
    if abs_t > 4.0:
        return 0.005
    elif abs_t > 3.0:
        return 0.02
    elif abs_t > 2.571:
        return 0.05
    elif abs_t > 2.015:
        return 0.10
    elif abs_t > 1.5:
        return 0.19
    elif abs_t > 1.0:
        return 0.36
    else:
        return 0.50

p_depth = spearman_pvalue(rho_depth, 7)
print()
print(f'  Spearman ρ(depth, circle) = {rho_depth:.3f}  (approx p ≈ {p_depth:.3f})')
print()

# ######################################################################
#  SECTION 4: EMPIRICAL UNIVERSALITY (D-rate across 9 domains)
# ######################################################################

print('=' * 78)
print('  EMPIRICAL UNIVERSALITY')
print('  Avg D-rate of anchors per duality across 9 domains')
print('=' * 78)
print()

# Compute D-rate per primitive: fraction of domains where class = D
domains = dom_data['domains']
domain_names = sorted(domains.keys())
n_domains = len(domain_names)

d_rate = {}
for pname in names:
    d_count = 0
    for dname in domain_names:
        cls = domains[dname]['classes'].get(pname, 'N')
        if cls == 'D':
            d_count += 1
    d_rate[pname] = d_count / n_domains

# Avg D-rate per duality
avg_drate = {}
for dk in CIRCLE_ORDER:
    anchors = get_anchors(dk)
    rates = [d_rate[a] for a in anchors]
    avg_drate[dk] = sum(rates) / len(rates) if rates else 0.0

# Rank by D-rate (higher = earlier rank)
sorted_by_drate = sorted(CIRCLE_ORDER, key=lambda k: -avg_drate[k])
drate_rank = {k: i + 1 for i, k in enumerate(sorted_by_drate)}

print(f'  {"Dualidad":<20} {"Avg.D-rate":>10} {"Rank":>6} {"Circle":>8} {"Δ":>4}')
print(f'  {"-"*20} {"-"*10} {"-"*6} {"-"*8} {"-"*4}')
for dk in CIRCLE_ORDER:
    circle_pos = CIRCLE_LABELS[dk]
    rank = drate_rank[dk]
    delta = rank - circle_pos
    flag = ' ← mismatch' if abs(delta) >= 3 else ''
    print(f'  {short[dk]:<20} {avg_drate[dk]:>10.3f} {rank:>6} {circle_pos:>8} {delta:>+4d}{flag}')

drate_ranks = [drate_rank[dk] for dk in CIRCLE_ORDER]
rho_drate = spearman(circle_ranks, drate_ranks)
p_drate = spearman_pvalue(rho_drate, 7)
print()
print(f'  Spearman ρ(D-rate, circle) = {rho_drate:.3f}  (approx p ≈ {p_drate:.3f})')
print()

# ######################################################################
#  SECTION 5: EJE-TO-DUALITY MAPPING
# ######################################################################

print('=' * 78)
print('  EJE-TO-DUALITY MAPPING')
print('  Which duality owns each of the 12 dual axes?')
print('=' * 78)
print()

ejes = prim_data['ejes_duales']

# Build lookup: primitive → duality (anchor or secondary)
prim_to_dual = {}
prim_to_role = {}
for dk in CIRCLE_ORDER:
    for a in dualidades[dk]['anclas']:
        prim_to_dual[a] = dk
        prim_to_role[a] = 'anchor'
    for s in dualidades[dk]['secundarios']:
        if s not in prim_to_dual:  # anchors take priority
            prim_to_dual[s] = dk
            prim_to_role[s] = 'secondary'

print(f'  {"Eje":<30} {"Capa":>5} {"Polo+":<15} {"Polo-":<15} {"Dualidad":<15}')
print(f'  {"-"*30} {"-"*5} {"-"*15} {"-"*15} {"-"*15}')

eje_duality_count = defaultdict(int)
unassigned_ejes = []

for polo_a, polo_b in ejes:
    capa_a = capa_map.get(polo_a, '?')
    capa_b = capa_map.get(polo_b, '?')
    capa = f'{capa_a}'

    dual_a = prim_to_dual.get(polo_a)
    dual_b = prim_to_dual.get(polo_b)

    # Assign eje to duality: prefer the one where both poles belong, else either
    if dual_a and dual_b and dual_a == dual_b:
        assigned = dual_a
    elif dual_a:
        assigned = dual_a
    elif dual_b:
        assigned = dual_b
    else:
        assigned = '—'
        unassigned_ejes.append((polo_a, polo_b))

    if assigned != '—':
        eje_duality_count[assigned] += 1

    print(f'  {polo_a + "/" + polo_b:<30} {capa:>5} {polo_a:<15} {polo_b:<15} {short.get(assigned, assigned):<15}')

print()
print('  Ejes per duality:')
for dk in CIRCLE_ORDER:
    count = eje_duality_count.get(dk, 0)
    bar = '█' * count
    print(f'    {short[dk]:<15} {count:>2}  {bar}')

if unassigned_ejes:
    print(f'\n  Unassigned ejes: {unassigned_ejes}')
print()

# ######################################################################
#  SECTION 6: COUNTERFACTUAL NECESSITY TEST
# ######################################################################

print('=' * 78)
print('  COUNTERFACTUAL NECESSITY TEST')
print('  If we swap Di→D and Dj→N, does monotonicity collapse?')
print('=' * 78)
print()

# Compute monotonicity for a synthetic domain assignment
def compute_monotonicity(assignment):
    """Fraction of DAG edges where child_state <= parent_state.
    assignment: dict {prim_name: 'D'|'A'|'N'}
    """
    violations = 0
    total = 0
    for parent, child in dep_pairs:
        pval = STATE_VAL.get(assignment.get(parent, 'A'), 1)
        cval = STATE_VAL.get(assignment.get(child, 'A'), 1)
        total += 1
        if cval > pval:
            violations += 1
    if total == 0:
        return 1.0
    return 1 - violations / total

# Baseline: use average monotonicity across real domains
real_monos = []
for dname in domain_names:
    real_monos.append(compute_monotonicity(domains[dname]['classes']))
baseline_mono = sum(real_monos) / len(real_monos)

# Threshold: below this, monotonicity is "damaged"
threshold = 0.80

print(f'  Baseline avg monotonicity (real domains): {baseline_mono:.3f}')
print(f'  Threshold for "necessary": mono < {threshold}')
print()

counter_results = []

print(f'  {"Pair":<15} {"Mono(counter)":>14} {"Interpretation":<30}')
print(f'  {"-"*15} {"-"*14} {"-"*30}')

for i, di in enumerate(CIRCLE_ORDER):
    for j, dj in enumerate(CIRCLE_ORDER):
        if i >= j:
            continue
        # Counterfactual: anchors of Dj = D, anchors of Di = N, rest = A
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
            interp = 'NECESSARY (mono drops)'
        elif mono < baseline_mono - 0.05:
            interp = 'WEAK (some damage)'
        else:
            interp = 'UNCERTAIN (mono stays high)'
        counter_results.append((di, dj, mono, interp))
        print(f'  {short[di]+"→"+short[dj]:<15} {mono:>14.3f} {interp:<30}')

print()

# ######################################################################
#  SECTION 7: REVERSE DEPENDENCY CHECK
# ######################################################################

print('=' * 78)
print('  REVERSE DEPENDENCY CHECK')
print('  Bidirectional dependencies → lattice structure?')
print('=' * 78)
print()

print(f'  {"Pair":<15} {"Forward":>8} {"Reverse":>8} {"Relation":<20}')
print(f'  {"-"*15} {"-"*8} {"-"*8} {"-"*20}')

bidirectional_pairs = []

for i, di in enumerate(CIRCLE_ORDER):
    for j, dj in enumerate(CIRCLE_ORDER):
        if i >= j:
            continue
        fwd = dep_matrix[di][dj]
        rev = dep_matrix[dj][di]
        if fwd is None:
            fwd = 0.0
        if rev is None:
            rev = 0.0

        if fwd > 0 and rev > 0:
            relation = 'BIDIRECTIONAL'
            bidirectional_pairs.append((di, dj, fwd, rev))
        elif fwd > 0:
            relation = 'Forward only'
        elif rev > 0:
            relation = 'Reverse only ← TENSION'
        else:
            relation = 'Independent'

        print(f'  {short[di]+"→"+short[dj]:<15} {fwd:>8.2f} {rev:>8.2f} {relation:<20}')

print()
if bidirectional_pairs:
    print(f'  Bidirectional pairs: {len(bidirectional_pairs)}')
    for di, dj, fwd, rev in bidirectional_pairs:
        print(f'    {short[di]} ↔ {short[dj]}: fwd={fwd:.2f}, rev={rev:.2f}')
    print('  → Structure is closer to LATTICE than strict CHAIN')
else:
    print('  No bidirectional pairs → structure is a strict CHAIN')
print()

# ######################################################################
#  SECTION 8: SYNTHESIS
# ######################################################################

print('═' * 78)
print('  SYNTHESIS')
print('═' * 78)
print()

# Consolidated table
print(f'  {"Dualidad":<18} {"Pos.":>5} {"Depth":>7} {"D-rate":>8} '
      f'{"DepScore":>9} {"Ejes":>5} {"CtrMono":>8}')
print(f'  {"-"*18} {"-"*5} {"-"*7} {"-"*8} {"-"*9} {"-"*5} {"-"*8}')

for dk in CIRCLE_ORDER:
    pos = CIRCLE_LABELS[dk]
    depth = avg_depths[dk]
    dr = avg_drate[dk]

    # DepScore: average forward dependency from all earlier dualidades
    idx = CIRCLE_ORDER.index(dk)
    if idx == 0:
        dep_score = '—'
    else:
        earlier = CIRCLE_ORDER[:idx]
        scores = [dep_matrix[e][dk] for e in earlier if dep_matrix[e][dk] is not None]
        dep_score = f'{sum(scores) / len(scores):.2f}' if scores else '—'

    ejes = eje_duality_count.get(dk, 0)

    # CounterMono: avg counterfactual mono for pairs involving this duality
    cmonos = [m for di, dj, m, _ in counter_results if di == dk or dj == dk]
    cmono = f'{sum(cmonos) / len(cmonos):.3f}' if cmonos else '—'

    print(f'  {short[dk]:<18} {pos:>5} {depth:>7.2f} {dr:>8.3f} '
          f'{dep_score:>9} {ejes:>5} {cmono:>8}')

print()

# Correlations
print(f'  Spearman ρ (depth vs circle):  {rho_depth:>+.3f}  (p ≈ {p_depth:.3f})')
print(f'  Spearman ρ (D-rate vs circle): {rho_drate:>+.3f}  (p ≈ {p_drate:.3f})')
print(f'  NOTE: These do not survive BH-FDR correction (0/12). See i1_recalc_pvalues.py.')
print()

# Dependency matrix triangularity
above_sum = sum(v for _, _, v in above_diag)
below_sum = sum(v for _, _, v in below_diag)
above_count = len(above_diag)
below_count = len(below_diag)
total_nonzero = above_count + below_count
triangularity = above_sum / (above_sum + below_sum) if (above_sum + below_sum) > 0 else 0

print(f'  Dependency matrix:')
print(f'    Above-diagonal (forward): {above_count} pairs, total weight = {above_sum:.2f}')
print(f'    Below-diagonal (reverse): {below_count} pairs, total weight = {below_sum:.2f}')
print(f'    Triangularity index: {triangularity:.3f} (1.0 = perfectly triangular)')
print()

# Counterfactual summary
necessary = sum(1 for _, _, _, interp in counter_results if 'NECESSARY' in interp)
weak = sum(1 for _, _, _, interp in counter_results if 'WEAK' in interp)
uncertain = sum(1 for _, _, _, interp in counter_results if 'UNCERTAIN' in interp)
total_pairs = len(counter_results)

print(f'  Counterfactual necessity:')
print(f'    Necessary: {necessary}/{total_pairs}')
print(f'    Weak: {weak}/{total_pairs}')
print(f'    Uncertain: {uncertain}/{total_pairs}')
print()

# Tensions
print(f'  TENSIONS:')
tensions = []
for di, dj, v in below_diag:
    if CIRCLE_LABELS[di] > CIRCLE_LABELS[dj]:
        tensions.append((di, dj, v))

if tensions:
    for di, dj, v in tensions:
        ci = CIRCLE_LABELS[di]
        cj = CIRCLE_LABELS[dj]
        print(f'  • {short[di]}(pos {ci}) → {short[dj]}(pos {cj}): '
              f'circle says {short[dj]} first, DAG shows reverse dependency ({v:.2f})')
else:
    print('  • No tensions detected between circle order and DAG.')

if bidirectional_pairs:
    print()
    for di, dj, fwd, rev in bidirectional_pairs:
        print(f'  • {short[di]} ↔ {short[dj]}: bidirectional (fwd={fwd:.2f}, rev={rev:.2f})')
print()

# Verdict
confirmed_pairs = sum(1 for _, _, v in above_diag if v > 0)
total_ordered = 21  # C(7,2)
pct = confirmed_pairs / total_ordered * 100 if total_ordered > 0 else 0

print('  ════════════════════════════════════════════════════════════════')

if triangularity >= 0.9 and rho_depth > 0.7 and rho_drate > 0.7:
    verdict = 'SUPPORTED'
elif triangularity >= 0.7 or (rho_depth > 0.5 and rho_drate > 0.5):
    verdict = 'PARTIALLY SUPPORTED'
else:
    verdict = 'CONTRADICTED'

print(f'  CONCLUSION: The emergence sequence is {verdict}.')

if len(bidirectional_pairs) > 2:
    print('  The structure is closer to a LATTICE than a strict CHAIN.')
elif bidirectional_pairs:
    print('  The structure has some lattice-like features but is mostly a CHAIN.')
else:
    print('  The structure is consistent with a strict CHAIN.')

print('  ════════════════════════════════════════════════════════════════')
