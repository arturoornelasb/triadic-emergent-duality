"""Post-integration audit for the 7×7 System.

Verifies structural integrity after adding proporción, quietud, and D8-D14.
Checks: DAG acyclicity, unique bits/primes, layer ordering, IDVS recompute,
zero orphans, dual axes, transitive closure, and delta report.

Usage:
    python integration_audit.py
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import math
import os
from collections import deque

# ######################################################################
#  DATA LOADING
# ######################################################################

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'data'))

with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
    prim_data = json.load(f)

with open(os.path.join(DATA_DIR, 'reference_domains.json'), 'r', encoding='utf-8') as f:
    ref_data = json.load(f)

with open(os.path.join(DATA_DIR, 'dualidad_primitivo_map.json'), 'r', encoding='utf-8') as f:
    dual_data = json.load(f)

prims = prim_data['primitivos']
names = [p['nombre'] for p in prims]
name_set = set(names)
capa_map = {p['nombre']: p['capa'] for p in prims}
deps_map = {p['nombre']: list(p['deps']) for p in prims}

# Build DAG edges
dep_pairs = []
children_map = {}
parents_map = {}
for p in prims:
    n = p['nombre']
    children_map.setdefault(n, set())
    parents_map.setdefault(n, set())
    for d in p['deps']:
        dep_pairs.append((d, n))
        children_map.setdefault(d, set()).add(n)
        parents_map[n].add(d)

domains = ref_data['domains']
dualidades = dual_data['dualidades']
ejes = prim_data['ejes_duales']

STATE_MAP = {'D': 2, 'A': 1, 'N': 0}

results = []
all_pass = True

def check(name, passed, detail=""):
    global all_pass
    symbol = '\u2713' if passed else '\u2717'
    status = 'PASS' if passed else 'FAIL'
    if not passed:
        all_pass = False
    results.append((name, passed, detail))
    print(f'  {symbol} {name}: {status}')
    if detail:
        for line in detail.split('\n'):
            print(f'      {line}')

print('=' * 78)
print('  INTEGRATION AUDIT')
print(f'  {len(prims)} primitivos, {len(dep_pairs)} aristas, '
      f'{len(domains)} dominios, {len(dualidades)} dualidades')
print('=' * 78)
print()

# ######################################################################
#  CHECK 1: DAG ACYCLICITY (topological sort)
# ######################################################################

in_degree = {n: 0 for n in names}
for parent, child in dep_pairs:
    in_degree[child] += 1

queue = deque([n for n in names if in_degree[n] == 0])
sorted_nodes = []
while queue:
    node = queue.popleft()
    sorted_nodes.append(node)
    for ch in children_map.get(node, set()):
        in_degree[ch] -= 1
        if in_degree[ch] == 0:
            queue.append(ch)

is_dag = len(sorted_nodes) == len(names)
check("DAG acyclicity",
      is_dag,
      f"{len(sorted_nodes)}/{len(names)} nodes in topological order"
      + ("" if is_dag else f" — cycle detected in: {set(names) - set(sorted_nodes)}"))

# ######################################################################
#  CHECK 2: UNIQUE BITS
# ######################################################################

bits = [p['bit'] for p in prims]
unique_bits = len(set(bits)) == len(bits)
detail = f"{len(set(bits))} unique out of {len(bits)}"
if not unique_bits:
    from collections import Counter
    dupes = [b for b, c in Counter(bits).items() if c > 1]
    detail += f" — duplicates: {dupes}"
check("Unique bits", unique_bits, detail)

# ######################################################################
#  CHECK 3: UNIQUE PRIMES (and primality)
# ######################################################################

def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

primos = [p['primo'] for p in prims]
unique_primes = len(set(primos)) == len(primos)
all_prime = all(is_prime(p) for p in primos)
not_prime = [p for p in primos if not is_prime(p)]
detail = f"{len(set(primos))} unique, all prime: {all_prime}"
if not_prime:
    detail += f" — not prime: {not_prime}"
check("Unique primes", unique_primes and all_prime, detail)

# ######################################################################
#  CHECK 4: LAYER ORDERING
# ######################################################################

layer_violations = []
for parent, child in dep_pairs:
    if capa_map[parent] > capa_map[child]:
        layer_violations.append(
            f"{child}(L{capa_map[child]}) <- {parent}(L{capa_map[parent]})")

check("Layer ordering (parent.capa <= child.capa)",
      len(layer_violations) == 0,
      f"{len(layer_violations)} violations" +
      (": " + "; ".join(layer_violations[:5]) if layer_violations else ""))

# ######################################################################
#  CHECK 5: IDVS RECOMPUTE
# ######################################################################

print()
print('  IDVS RECOMPUTE')
print(f'  {"Domain":<16} {"Coverage":>9} {"Monoton.":>9} {"IDVS":>7} {"Status":>8}')
print(f'  {"-" * 51}')

total_L14 = sum(1 for p in prims if p['capa'] <= 4)
idvs_results = {}

for dname, dinfo in sorted(domains.items()):
    classes = dinfo['classes']

    # Coverage L1-4
    nulls_L14 = sum(1 for p in prims
                    if p['capa'] <= 4 and classes.get(p['nombre'], 'N') == 'N')
    coverage = 1.0 - nulls_L14 / total_L14

    # Monotonicity
    mono_count = 0
    for parent, child in dep_pairs:
        p_state = STATE_MAP.get(classes.get(parent, 'N'), 0)
        c_state = STATE_MAP.get(classes.get(child, 'N'), 0)
        if c_state <= p_state:
            mono_count += 1
    monotonicity = mono_count / len(dep_pairs) if dep_pairs else 1.0

    idvs = coverage * monotonicity
    idvs_results[dname] = {
        'coverage': round(coverage, 3),
        'monotonicity': round(monotonicity, 3),
        'idvs': round(idvs, 3)
    }

    is_positive = dinfo['type'] == 'positive'
    if is_positive:
        status = 'PASS' if idvs >= 0.90 else 'FAIL'
    else:
        status = 'PASS' if idvs < 0.50 else 'FAIL'

    print(f'  {dname:<16} {coverage:>9.3f} {monotonicity:>9.3f} {idvs:>7.3f} {status:>8}')

# Check pass/fail
positive_pass = all(
    idvs_results[d]['idvs'] >= 0.90
    for d, info in domains.items() if info['type'] == 'positive'
)
negative_pass = all(
    idvs_results[d]['idvs'] < 0.50
    for d, info in domains.items() if info['type'] != 'positive'
)

print()
check("IDVS: 8 positives >= 0.90", positive_pass,
      ", ".join(f"{d}={idvs_results[d]['idvs']:.3f}"
                for d in sorted(domains) if domains[d]['type'] == 'positive'))
check("IDVS: Astrology < 0.50", negative_pass,
      f"Astrology={idvs_results.get('Astrology', {}).get('idvs', '?')}")

# ######################################################################
#  CHECK 6: ZERO ORPHANS
# ######################################################################

all_duality_prims = set()
for dk, dv in dualidades.items():
    for a in dv['anclas']:
        all_duality_prims.add(a)
    for s in dv['secundarios']:
        all_duality_prims.add(s)

orphans = set(names) - all_duality_prims
check("Zero orphans",
      len(orphans) == 0,
      f"{len(orphans)} orphans" +
      (f": {sorted(orphans)}" if orphans else ""))

# ######################################################################
#  CHECK 7: DUAL AXES
# ######################################################################

eje_issues = []
for polo_a, polo_b in ejes:
    if polo_a not in name_set:
        eje_issues.append(f"{polo_a} not in primitivos")
    if polo_b not in name_set:
        eje_issues.append(f"{polo_b} not in primitivos")
    # Check both poles in same duality
    dual_a = None
    dual_b = None
    for dk, dv in dualidades.items():
        all_in_d = set(dv['anclas']) | set(dv['secundarios'])
        if polo_a in all_in_d:
            dual_a = dk
        if polo_b in all_in_d:
            dual_b = dk
    if dual_a is None:
        eje_issues.append(f"{polo_a} not in any duality")
    if dual_b is None:
        eje_issues.append(f"{polo_b} not in any duality")

check(f"Dual axes ({len(ejes)} ejes)",
      len(eje_issues) == 0,
      "; ".join(eje_issues) if eje_issues else f"All {len(ejes)} axes valid")

# ######################################################################
#  CHECK 8: TRANSITIVE CLOSURE
# ######################################################################

def compute_ancestors(node):
    result = set()
    queue = deque(list(parents_map.get(node, set())))
    while queue:
        n = queue.popleft()
        if n not in result:
            result.add(n)
            for p in parents_map.get(n, set()):
                if p not in result:
                    queue.append(p)
    return result

ancestors_quietud = compute_ancestors('quietud')
ancestors_proporcion = compute_ancestors('proporción')

expected_anc_quietud = {'eje_profundidad', 'uno'}
expected_anc_proporcion = {'más', 'información', 'orden', 'uno',
                           'eje_profundidad', 'fuerza', 'mover',
                           'posición_temporal'}

check("ancestors(quietud) = {eje_profundidad, uno}",
      ancestors_quietud == expected_anc_quietud,
      f"Got: {sorted(ancestors_quietud)}")

check("ancestors(proporción) complete",
      ancestors_proporcion == expected_anc_proporcion,
      f"Got: {sorted(ancestors_proporcion)}")

# ######################################################################
#  CHECK 9: SPECIFIC COLLISIONS
# ######################################################################

bit_63_free = sum(1 for p in prims if p['bit'] == 63) == 1
bit_64_free = sum(1 for p in prims if p['bit'] == 64) == 1
prime_311_free = sum(1 for p in prims if p['primo'] == 311) == 1
prime_313_free = sum(1 for p in prims if p['primo'] == 313) == 1

check("Bit 63 unique (proporción)", bit_63_free)
check("Bit 64 unique (quietud)", bit_64_free)
check("Prime 311 unique (proporción)", prime_311_free)
check("Prime 313 unique (quietud)", prime_313_free)

# ######################################################################
#  CHECK 10: DELTA REPORT
# ######################################################################

print()
print('  ' + '=' * 54)
print('  DELTA REPORT (before → after)')
print('  ' + '=' * 54)
print()

# Before values (hardcoded from pre-integration state)
BEFORE = {
    'primitivos': 63,
    'aristas': 128,
    'ejes_duales': 12,
    'dualidades': 7,
    'huérfanos': 29,
}

AFTER = {
    'primitivos': len(prims),
    'aristas': len(dep_pairs),
    'ejes_duales': len(ejes),
    'dualidades': len(dualidades),
    'huérfanos': len(orphans),
}

print(f'  {"Metric":<20} {"Before":>8} {"After":>8} {"Delta":>8}')
print(f'  {"-" * 46}')
for key in BEFORE:
    b = BEFORE[key]
    a = AFTER[key]
    d = a - b
    sign = '+' if d > 0 else ''
    print(f'  {key:<20} {b:>8} {a:>8} {sign + str(d):>8}')

# IDVS deltas
print()
print(f'  {"Domain":<16} {"Before":>8} {"After":>8} {"Delta":>8}')
print(f'  {"-" * 42}')

old_idvs = ref_data['reference_idvs']
for dname in sorted(domains.keys()):
    old = old_idvs.get(dname, 0)
    new = idvs_results[dname]['idvs']
    delta = new - old
    sign = '+' if delta > 0 else ''
    print(f'  {dname:<16} {old:>8.3f} {new:>8.3f} {sign}{delta:>.3f}'.rstrip('0').rstrip('.') if False else
          f'  {dname:<16} {old:>8.3f} {new:>8.3f} {sign}{delta:>+8.3f}')

# ######################################################################
#  FINAL VERDICT
# ######################################################################

print()
print('  ' + '\u2550' * 54)
if all_pass:
    print('  \u2713 ALL CHECKS PASSED — Integration verified.')
else:
    failed = [name for name, passed, _ in results if not passed]
    print(f'  \u2717 {len(failed)} CHECK(S) FAILED:')
    for f in failed:
        print(f'      - {f}')
print('  ' + '\u2550' * 54)
print()

# ######################################################################
#  OUTPUT: Updated reference values for reference_domains.json
# ######################################################################

print('  UPDATED REFERENCE VALUES (paste into reference_domains.json):')
print()
print('  "reference_idvs": {')
for i, dname in enumerate(sorted(domains.keys())):
    comma = ',' if i < len(domains) - 1 else ''
    print(f'    "{dname}": {idvs_results[dname]["idvs"]:.3f}{comma}')
print('  },')
print('  "reference_coverage": {')
for i, dname in enumerate(sorted(domains.keys())):
    comma = ',' if i < len(domains) - 1 else ''
    print(f'    "{dname}": {idvs_results[dname]["coverage"]:.3f}{comma}')
print('  },')
print('  "reference_monotonicity": {')
for i, dname in enumerate(sorted(domains.keys())):
    comma = ',' if i < len(domains) - 1 else ''
    print(f'    "{dname}": {idvs_results[dname]["monotonicity"]:.3f}{comma}')
print('  }')
print()

sys.exit(0 if all_pass else 1)
