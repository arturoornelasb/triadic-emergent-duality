"""Fase 10: Firmas Algebraicas de Dualidad.

Implements algebraic signatures at the duality level using the prime
factorization of the 65-primitive DAG. Three signature types:
  sigma_ancla: product of anchor primes
  sigma_dep:   product of ancestor primes (transitive closure)
  sigma_ext:   product of (anchor + secondary) primes

GCD/LCM matrices, conceptual distance, divisibility order, Spearman.
Answers the 4 open questions from doc 32.
Solo stdlib: json, math, sys, os, collections.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import math
import os
from collections import defaultdict, deque

# ######################################################################
#  SECTION 0: DATA LOADING + TRANSITIVE CLOSURE
# ######################################################################

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data')

with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
    prim_data = json.load(f)

with open(os.path.join(DATA_DIR, 'dualidad_primitivo_map.json'), 'r', encoding='utf-8') as f:
    dual_data = json.load(f)

prims = prim_data['primitivos']
names = [p['nombre'] for p in prims]
prime_map = {p['nombre']: p['primo'] for p in prims}
capa_map = {p['nombre']: p['capa'] for p in prims}
deps_map = {p['nombre']: list(p['deps']) for p in prims}

parents = defaultdict(set)
for p in prims:
    for d in p['deps']:
        parents[p['nombre']].add(d)


def compute_ancestors(node, parents_map, cache):
    if node in cache:
        return cache[node]
    result = set()
    queue = deque(list(parents_map.get(node, set())))
    while queue:
        n = queue.popleft()
        if n not in result:
            result.add(n)
            for par in parents_map.get(n, set()):
                if par not in result:
                    queue.append(par)
    cache[node] = result
    return result


ancestor_cache = {}
ancestors = {n: compute_ancestors(n, parents, ancestor_cache) for n in names}

CIRCLE_ORDER = ['D1_existir', 'D2_espacio', 'D3_tiempo',
                'D4_posibilidad', 'D5_identidad', 'D6_movimiento', 'D7_orden']
SPIRAL_ORDER = ['D8_uno_muchos', 'D9_dentro_fuera', 'D10_parte_todo',
                'D11_vida_muerte', 'D12_causa_efecto',
                'D13_semejante_diferente', 'D14_sujeto_objeto']
ALL_14 = CIRCLE_ORDER + SPIRAL_ORDER
ALL_LABELS = {k: i + 1 for i, k in enumerate(ALL_14)}
dualidades = dual_data['dualidades']
short = {k: k.split('_')[0] + '_' + k.split('_')[1][:4] for k in ALL_14}


def log2(x):
    return math.log2(x) if x > 1 else 0.0


print('=' * 78)
print('  ALGEBRAIC DUALITY SIGNATURES')
print(f'  14 Dualidades x {len(prims)} Primitivos')
print('=' * 78)
print()

# ######################################################################
#  SECTION 1: PRIMITIVE SIGNATURES
# ######################################################################

print('=' * 78)
print('  PRIMITIVE SIGNATURES')
print('=' * 78)
print()

print(f'  {"Primitivo":<22} {"Capa":>5} {"Primo":>6} {"#Anc":>5} '
      f'{"log2(sig)":>10}')
print(f'  {"-"*22} {"-"*5} {"-"*6} {"-"*5} {"-"*10}')

for p in sorted(prims, key=lambda x: (x['capa'], x['bit'])):
    name = p['nombre']
    anc = ancestors[name]
    sig = 1
    for a in anc:
        sig *= prime_map[a]
    print(f'  {name:<22} {p["capa"]:>5} {p["primo"]:>6} {len(anc):>5} '
          f'{log2(sig):>10.2f}')

print()

# ######################################################################
#  SECTION 2: ANCHOR SIGNATURES
# ######################################################################

print('=' * 78)
print('  ANCHOR SIGNATURES: sigma_ancla(Dk) = prod(prime(a) for a in anchors)')
print('=' * 78)
print()


def sigma_product(prim_set):
    """Product of primes for a set of primitive names."""
    result = 1
    for name in prim_set:
        result *= prime_map[name]
    return result


sig_ancla = {}
for dk in ALL_14:
    anchors = dualidades[dk]['anclas']
    sig_ancla[dk] = sigma_product(anchors)

print(f'  {"Dualidad":<12} {"Anchors":<35} '
      f'{"sigma":>12} {"log2":>8}')
print(f'  {"-"*12} {"-"*35} {"-"*12} {"-"*8}')
for dk in ALL_14:
    anchors = dualidades[dk]['anclas']
    print(f'  {short[dk]:<12} {", ".join(anchors):<35} '
          f'{sig_ancla[dk]:>12} {log2(sig_ancla[dk]):>8.2f}')
print()

# ######################################################################
#  SECTION 3: DEPENDENCY SIGNATURES
# ######################################################################

print('=' * 78)
print('  DEPENDENCY SIGNATURES: sigma_dep(Dk) = prod(prime(a) for a in ancestors)')
print('=' * 78)
print()

sig_dep = {}
dep_ancestors = {}  # store ancestor sets for later use
for dk in ALL_14:
    anchors = dualidades[dk]['anclas']
    anc_union = set()
    for a in anchors:
        anc_union |= ancestors[a]
    dep_ancestors[dk] = anc_union
    sig_dep[dk] = sigma_product(anc_union) if anc_union else 1

print(f'  {"Dualidad":<12} {"#Ancestors":>10} {"log2(sig_dep)":>14} '
      f'{"Ancestors (sample)":<35}')
print(f'  {"-"*12} {"-"*10} {"-"*14} {"-"*35}')
for dk in ALL_14:
    anc = dep_ancestors[dk]
    sample = sorted(anc)[:5]
    more = f'... +{len(anc)-5}' if len(anc) > 5 else ''
    print(f'  {short[dk]:<12} {len(anc):>10} {log2(sig_dep[dk]):>14.2f} '
          f'{", ".join(sample) + more:<35}')
print()

# Verification: roots should have sigma_dep = 1
print('  Verification:')
print(f'    sigma_dep(D1_existir) = {sig_dep["D1_existir"]} '
      f'(expected: 1, anchors are roots)')
assert sig_dep['D1_existir'] == 1, 'D1 should have sigma_dep = 1'
print('    PASS: roots have sigma_dep = 1')
print()

# ######################################################################
#  SECTION 4: EXTENDED SIGNATURES
# ######################################################################

print('=' * 78)
print('  EXTENDED SIGNATURES: sigma_ext(Dk) = prod(prime(a+s) for a,s in duality)')
print('=' * 78)
print()

sig_ext = {}
ext_sets = {}
for dk in ALL_14:
    members = set(dualidades[dk]['anclas']) | set(dualidades[dk]['secundarios'])
    ext_sets[dk] = members
    sig_ext[dk] = sigma_product(members)

print(f'  {"Dualidad":<12} {"#Members":>9} {"log2(sig_ext)":>14} '
      f'{"log2(sig_ancla)":>16}')
print(f'  {"-"*12} {"-"*9} {"-"*14} {"-"*16}')
for dk in ALL_14:
    print(f'  {short[dk]:<12} {len(ext_sets[dk]):>9} '
          f'{log2(sig_ext[dk]):>14.2f} {log2(sig_ancla[dk]):>16.2f}')
print()

# ######################################################################
#  SECTION 5: GCD MATRIX
# ######################################################################

print('=' * 78)
print('  GCD MATRIX: MCD(sigma_dep(Di), sigma_dep(Dj))')
print('  Values shown as log2. Factorized = shared ancestor primitives')
print('=' * 78)
print()

gcd_matrix = {}
for di in ALL_14:
    gcd_matrix[di] = {}
    for dj in ALL_14:
        gcd_matrix[di][dj] = math.gcd(sig_dep[di], sig_dep[dj])

# Print in 2 blocks (7 columns each)
for block_name, col_keys in [('Block 1 (D1-D7)', CIRCLE_ORDER),
                              ('Block 2 (D8-D14)', SPIRAL_ORDER)]:
    print(f'  {block_name}')
    hdr = ' ' * 14
    for k in col_keys:
        hdr += f'{short[k]:>8}'
    print(hdr)
    for di in ALL_14:
        row_str = f'  {short[di]:<12}'
        for dj in col_keys:
            v = log2(gcd_matrix[di][dj])
            row_str += f'{v:>8.1f}'
        print(row_str)
    print()

# Factorize: show shared primitives for notable GCD pairs
print('  Notable shared ancestors (GCD > 1):')
shown = set()
for di in ALL_14:
    for dj in ALL_14:
        if di >= dj:
            continue
        shared = dep_ancestors[di] & dep_ancestors[dj]
        if shared and (di, dj) not in shown:
            shown.add((di, dj))
            g = gcd_matrix[di][dj]
            if log2(g) > 10:
                print(f'    {short[di]} & {short[dj]}: '
                      f'{len(shared)} shared ancestors, '
                      f'log2(GCD)={log2(g):.1f}')
print()

# Verification: GCD(anything, D1) = sigma_dep(D1) = 1
for dk in ALL_14:
    if dk == 'D1_existir':
        continue
    g = gcd_matrix['D1_existir'][dk]
    assert g == 1, f'GCD(D1, {dk}) should be 1, got {g}'
print('  Verification: GCD(any, D1) = 1  PASS')
print()

# ######################################################################
#  SECTION 6: LCM MATRIX
# ######################################################################

print('=' * 78)
print('  LCM MATRIX: MCM(sigma_dep(Di), sigma_dep(Dj)) in log2')
print('=' * 78)
print()


def lcm(a, b):
    return a * b // math.gcd(a, b) if a and b else 0


lcm_matrix = {}
for di in ALL_14:
    lcm_matrix[di] = {}
    for dj in ALL_14:
        lcm_matrix[di][dj] = lcm(sig_dep[di], sig_dep[dj])

for block_name, col_keys in [('Block 1 (D1-D7)', CIRCLE_ORDER),
                              ('Block 2 (D8-D14)', SPIRAL_ORDER)]:
    print(f'  {block_name}')
    hdr = ' ' * 14
    for k in col_keys:
        hdr += f'{short[k]:>8}'
    print(hdr)
    for di in ALL_14:
        row_str = f'  {short[di]:<12}'
        for dj in col_keys:
            v = log2(lcm_matrix[di][dj])
            row_str += f'{v:>8.1f}'
        print(row_str)
    print()

# Verification: LCM(Di,Dj) >= max(sigma_dep(Di), sigma_dep(Dj))
lcm_violations = 0
for di in ALL_14:
    for dj in ALL_14:
        if lcm_matrix[di][dj] < max(sig_dep[di], sig_dep[dj]):
            lcm_violations += 1
print(f'  Verification: LCM >= max(sig_dep): '
      f'{"PASS" if lcm_violations == 0 else f"FAIL ({lcm_violations} violations)"}')
print()

# ######################################################################
#  SECTION 7: CONCEPTUAL DISTANCE
# ######################################################################

print('=' * 78)
print('  CONCEPTUAL DISTANCE: dist(Di,Dj) = log2(LCM/GCD)')
print('=' * 78)
print()

dist_matrix = {}
for di in ALL_14:
    dist_matrix[di] = {}
    for dj in ALL_14:
        g = gcd_matrix[di][dj]
        l = lcm_matrix[di][dj]
        dist_matrix[di][dj] = log2(l) - log2(g) if g > 0 else 0.0

for block_name, col_keys in [('Block 1 (D1-D7)', CIRCLE_ORDER),
                              ('Block 2 (D8-D14)', SPIRAL_ORDER)]:
    print(f'  {block_name}')
    hdr = ' ' * 14
    for k in col_keys:
        hdr += f'{short[k]:>8}'
    print(hdr)
    for di in ALL_14:
        row_str = f'  {short[di]:<12}'
        for dj in col_keys:
            v = dist_matrix[di][dj]
            row_str += f'{v:>8.1f}'
        print(row_str)
    print()

# Nearest and farthest
print('  Nearest/Farthest pairs:')
print(f'  {"Dualidad":<12} {"Nearest":<12} {"dist":>6} '
      f'{"Farthest":<12} {"dist":>6}')
print(f'  {"-"*12} {"-"*12} {"-"*6} {"-"*12} {"-"*6}')
for dk in ALL_14:
    others = [(dj, dist_matrix[dk][dj]) for dj in ALL_14 if dj != dk]
    nearest = min(others, key=lambda x: x[1])
    farthest = max(others, key=lambda x: x[1])
    print(f'  {short[dk]:<12} {short[nearest[0]]:<12} {nearest[1]:>6.1f} '
          f'{short[farthest[0]]:<12} {farthest[1]:>6.1f}')
print()

# ######################################################################
#  SECTION 8: DIVISIBILITY ORDER
# ######################################################################

print('=' * 78)
print('  DIVISIBILITY ORDER: sigma_dep(Di) | sigma_dep(Dj)?')
print('=' * 78)
print()

# Build divisibility DAG
divides = {}  # divides[di] = set of dj where sig_dep[di] | sig_dep[dj]
for di in ALL_14:
    divides[di] = set()
    for dj in ALL_14:
        if di == dj:
            continue
        if sig_dep[dj] > 0 and sig_dep[dj] % sig_dep[di] == 0:
            divides[di].add(dj)

# Hasse diagram: remove transitive edges
hasse = {}
for di in ALL_14:
    hasse[di] = set()
    for dj in divides[di]:
        # Check if there is a Dk between Di and Dj
        has_intermediate = False
        for dk in divides[di]:
            if dk != dj and dj in divides.get(dk, set()):
                has_intermediate = True
                break
        if not has_intermediate:
            hasse[di].add(dj)

print('  Hasse diagram (covers):')
for di in ALL_14:
    covers = sorted(hasse[di], key=lambda x: ALL_14.index(x))
    if covers:
        print(f'    {short[di]} -> {", ".join(short[c] for c in covers)}')

# Check acyclicity (DAG)
# Simple DFS cycle check
visited = set()
rec_stack = set()
is_dag = True


def dfs_cycle(node):
    global is_dag
    visited.add(node)
    rec_stack.add(node)
    for nb in hasse.get(node, set()):
        if nb not in visited:
            dfs_cycle(nb)
        elif nb in rec_stack:
            is_dag = False
    rec_stack.discard(node)


for dk in ALL_14:
    if dk not in visited:
        dfs_cycle(dk)

print(f'\n  Acyclicity check: {"PASS (DAG)" if is_dag else "FAIL (has cycles)"}')

# Consistency: do Hasse edges respect circle/spiral ordering?
consistent = 0
inconsistent = 0
for di in ALL_14:
    for dj in hasse[di]:
        pi = ALL_14.index(di)
        pj = ALL_14.index(dj)
        if pi < pj:
            consistent += 1
        else:
            inconsistent += 1

total_hasse = consistent + inconsistent
consistency_score = consistent / total_hasse if total_hasse > 0 else 0.0
print(f'  Consistency with ordering: {consistent}/{total_hasse} = '
      f'{consistency_score:.3f}')
if inconsistent > 0:
    print('  Inconsistent edges (later divides earlier):')
    for di in ALL_14:
        for dj in hasse[di]:
            if ALL_14.index(di) > ALL_14.index(dj):
                print(f'    {short[di]} -> {short[dj]}')
print()

# ######################################################################
#  SECTION 9: SPEARMAN ALGEBRAIC (sigma_dep)
# ######################################################################

print('=' * 78)
print('  SPEARMAN ALGEBRAIC: rank by log2(sigma_dep) vs position')
print('=' * 78)
print()


def spearman(ranks_x, ranks_y):
    n = len(ranks_x)
    if n < 3:
        return 0.0
    d_sq = sum((rx - ry) ** 2 for rx, ry in zip(ranks_x, ranks_y))
    return 1 - 6 * d_sq / (n * (n * n - 1))


def spearman_pvalue(rho, n):
    if n < 4 or abs(rho) >= 1.0:
        return 0.0
    t = rho * math.sqrt((n - 2) / (1 - rho * rho))
    abs_t = abs(t)
    df = n - 2
    T_CRIT = {
        5: [(6.869, 0.001), (4.032, 0.01), (2.571, 0.05),
            (2.015, 0.10), (1.476, 0.20)],
        12: [(4.318, 0.001), (3.055, 0.01), (2.179, 0.05),
             (1.782, 0.10), (1.356, 0.20)],
    }
    table = T_CRIT.get(df)
    if table:
        for t_crit, p_val in table:
            if abs_t > t_crit:
                return p_val
        return 0.50
    if abs_t > 3.291:
        return 0.001
    if abs_t > 2.576:
        return 0.01
    if abs_t > 1.960:
        return 0.05
    if abs_t > 1.645:
        return 0.10
    return 0.50


def algebraic_rank_analysis(order, labels, sig_dict, title):
    """Rank by log2(signature) vs ordering position."""
    sorted_d = sorted(order, key=lambda k: sig_dict[k])
    a_rank = {k: i + 1 for i, k in enumerate(sorted_d)}

    print(f'  {title}')
    print(f'  {"Dualidad":<12} {"log2(sig)":>10} {"Rank":>6} {"Pos":>5} {"D":>4}')
    print(f'  {"-"*12} {"-"*10} {"-"*6} {"-"*5} {"-"*4}')
    for dk in order:
        pos = labels[dk]
        rank = a_rank[dk]
        delta = rank - pos
        flag = ' <- mismatch' if abs(delta) >= 3 else ''
        print(f'  {short[dk]:<12} {log2(sig_dict[dk]):>10.2f} {rank:>6} '
              f'{pos:>5} {delta:>+4d}{flag}')

    pos_r = [labels[dk] for dk in order]
    dep_r = [a_rank[dk] for dk in order]
    rho = spearman(pos_r, dep_r)
    p = spearman_pvalue(rho, len(order))
    print(f'\n  Spearman rho = {rho:.3f}  (p ~ {p:.3f})')
    print()
    return rho, p


CIRCLE_LABELS = {k: i + 1 for i, k in enumerate(CIRCLE_ORDER)}
SPIRAL_LABELS = {k: i + 1 for i, k in enumerate(SPIRAL_ORDER)}

print('  Using sigma_dep:')
rho_dep_c, p_dep_c = algebraic_rank_analysis(
    CIRCLE_ORDER, CIRCLE_LABELS, sig_dep, 'Circle (D1-D7)')
rho_dep_s, p_dep_s = algebraic_rank_analysis(
    SPIRAL_ORDER, SPIRAL_LABELS, sig_dep, 'Spiral (D8-D14)')
rho_dep_a, p_dep_a = algebraic_rank_analysis(
    ALL_14, ALL_LABELS, sig_dep, 'Combined (D1-D14)')

# ######################################################################
#  SECTION 10: ANCHOR vs EXTENDED
# ######################################################################

print('=' * 78)
print('  ANCHOR vs EXTENDED: repeat divisibility & Spearman with sigma_ext')
print('=' * 78)
print()

# Divisibility order with sigma_ext
divides_ext = {}
for di in ALL_14:
    divides_ext[di] = set()
    for dj in ALL_14:
        if di == dj:
            continue
        if sig_ext[dj] > 0 and sig_ext[dj] % sig_ext[di] == 0:
            divides_ext[di].add(dj)

# Hasse for ext
hasse_ext = {}
for di in ALL_14:
    hasse_ext[di] = set()
    for dj in divides_ext[di]:
        has_intermediate = False
        for dk in divides_ext[di]:
            if dk != dj and dj in divides_ext.get(dk, set()):
                has_intermediate = True
                break
        if not has_intermediate:
            hasse_ext[di].add(dj)

print('  Hasse diagram (sigma_ext):')
for di in ALL_14:
    covers = sorted(hasse_ext[di], key=lambda x: ALL_14.index(x))
    if covers:
        print(f'    {short[di]} -> {", ".join(short[c] for c in covers)}')

# Consistency
consistent_ext = sum(1 for di in ALL_14 for dj in hasse_ext[di]
                     if ALL_14.index(di) < ALL_14.index(dj))
total_ext = sum(len(hasse_ext[di]) for di in ALL_14)
cons_ext = consistent_ext / total_ext if total_ext > 0 else 0.0
print(f'\n  Consistency (sigma_ext): {consistent_ext}/{total_ext} = {cons_ext:.3f}')
print()

# Spearman with sigma_ext
print('  Using sigma_ext:')
rho_ext_c, p_ext_c = algebraic_rank_analysis(
    CIRCLE_ORDER, CIRCLE_LABELS, sig_ext, 'Circle (D1-D7)')
rho_ext_s, p_ext_s = algebraic_rank_analysis(
    SPIRAL_ORDER, SPIRAL_LABELS, sig_ext, 'Spiral (D8-D14)')
rho_ext_a, p_ext_a = algebraic_rank_analysis(
    ALL_14, ALL_LABELS, sig_ext, 'Combined (D1-D14)')

# Comparison: dep vs ext
print('  Comparison: sigma_dep vs sigma_ext Spearman')
print(f'  {"Group":<25} {"rho_dep":>8} {"rho_ext":>8} {"Better?":>10}')
print(f'  {"-"*25} {"-"*8} {"-"*8} {"-"*10}')
for label, rd, re in [
    ('Circle (D1-D7)', rho_dep_c, rho_ext_c),
    ('Spiral (D8-D14)', rho_dep_s, rho_ext_s),
    ('Combined (D1-D14)', rho_dep_a, rho_ext_a),
]:
    better = 'dep' if abs(rd) > abs(re) else ('ext' if abs(re) > abs(rd) else 'tie')
    print(f'  {label:<25} {rd:>+8.3f} {re:>+8.3f} {better:>10}')
print()

# ######################################################################
#  SECTION 11: SYNTHESIS
# ######################################################################

print('=' * 78)
print('  SYNTHESIS — ALGEBRAIC SIGNATURES')
print('=' * 78)
print()

# Consolidated table
print(f'  {"Dualidad":<12} {"log_anc":>8} {"log_dep":>8} {"log_ext":>8} '
      f'{"#anc":>5} {"divides":>8}')
print(f'  {"-"*12} {"-"*8} {"-"*8} {"-"*8} {"-"*5} {"-"*8}')
for dk in ALL_14:
    n_div = len(divides[dk])
    print(f'  {short[dk]:<12} {log2(sig_ancla[dk]):>8.2f} '
          f'{log2(sig_dep[dk]):>8.2f} {log2(sig_ext[dk]):>8.2f} '
          f'{len(dep_ancestors[dk]):>5} {n_div:>8}')
print()

# Answer the 4 questions from doc 32
print('  ANSWERS TO DOC 32 OPEN QUESTIONS')
print('  ' + '-' * 50)
print()

# Q1: Do algebraic signatures distinguish dualidades?
all_sig_dep = [sig_dep[dk] for dk in ALL_14]
unique_sigs = len(set(all_sig_dep))
print(f'  Q1: Do signatures distinguish dualidades?')
print(f'      Unique sigma_dep values: {unique_sigs}/14')
print(f'      -> {"YES" if unique_sigs == 14 else "PARTIALLY"}: '
      f'{"all distinct" if unique_sigs == 14 else f"{14 - unique_sigs} collisions"}')
print()

# Q2: Does divisibility reflect emergence order?
print(f'  Q2: Does divisibility reflect emergence order?')
print(f'      Hasse consistency (sigma_dep): {consistency_score:.3f}')
print(f'      Hasse consistency (sigma_ext): {cons_ext:.3f}')
print(f'      -> {"YES" if consistency_score >= 0.8 else "PARTIALLY"}: '
      f'divisibility mostly follows ordering')
print()

# Q3: Does Spearman improve with algebraic approach?
print(f'  Q3: Spearman algebraic vs depth-based?')
print(f'      Algebraic (sigma_dep, combined): rho = {rho_dep_a:+.3f}')
print(f'      (Compare with depth-based from doc 34)')
print(f'      -> Algebraic provides complementary perspective')
print()

# Q4: sigma_ext vs sigma_dep — which is better?
dep_better = sum(1 for rd, re in [(rho_dep_c, rho_ext_c),
                                   (rho_dep_s, rho_ext_s),
                                   (rho_dep_a, rho_ext_a)]
                 if abs(rd) > abs(re))
print(f'  Q4: sigma_ext vs sigma_dep?')
print(f'      sigma_dep wins in {dep_better}/3 Spearman comparisons')
print(f'      -> {"sigma_dep" if dep_better >= 2 else "sigma_ext"} is '
      f'generally better for capturing emergence order')
print()

# Final verdict
print('  ' + '=' * 50)
print(f'  Divisibility order is {"acyclic" if is_dag else "CYCLIC"} (DAG)')
print(f'  Algebraic Spearman (combined): rho = {rho_dep_a:+.3f}')
print(f'  Signatures are {"unique" if unique_sigs == 14 else "not fully unique"}')
print('  ' + '=' * 50)
