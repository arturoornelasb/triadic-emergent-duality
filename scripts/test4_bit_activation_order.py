"""Test 4: Bit activation order — THE key falsifiable test.
For each dependency pair (i depends on j) in primitivos.json,
verify that in anclas_v2.json, when bit i is active, bit j is also active."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import os
from collections import defaultdict, Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data')

with open(f'{DATA_DIR}/primitivos.json', 'r', encoding='utf-8') as f:
    prim_data = json.load(f)
with open(f'{DATA_DIR}/anclas_v2.json', 'r', encoding='utf-8') as f:
    anclas = json.load(f)

# Also try to load v1 anchors
try:
    with open(f'{DATA_DIR}/anclas.json', 'r', encoding='utf-8') as f:
        anclas_v1 = json.load(f)
except:
    anclas_v1 = {}

prims = prim_data['primitivos']
deps_map = {p['nombre']: p['deps'] for p in prims}
capa_map = {p['nombre']: p['capa'] for p in prims}
name_set = {p['nombre'] for p in prims}

# Build all dependency pairs (child, parent)
all_dep_pairs = []
for p in prims:
    for d in p['deps']:
        all_dep_pairs.append((p['nombre'], d))

# Filter anchors
meta_keys = {'_descripcion', '_formato', '_total_v1', '_total_v2',
             '_version', '_total', 'version', 'total', 'descripcion'}
anchor_data = {}
for source_name, source in [('v2', anclas), ('v1', anclas_v1)]:
    for k, v in source.items():
        if k.startswith('_') or k in meta_keys:
            continue
        if isinstance(v, dict) and 'bits' in v:
            anchor_data[f'{k}'] = set(v['bits'])

print(f'Total anchors loaded: {len(anchor_data)}')
print(f'Total dependency pairs in primitivos.json: {len(all_dep_pairs)}')
print()

# ========== MAIN TEST ==========
print('=' * 70)
print('TEST 4: BIT ACTIVATION ORDER (KEY FALSIFIABLE TEST)')
print('=' * 70)
print()

# For each dependency pair (child, parent):
# Count: how many anchors have child active?
# Of those, how many also have parent active?
# Consistency = parent_active / child_active

results = []
for child, parent in all_dep_pairs:
    child_active = 0
    both_active = 0
    child_only = []

    for anchor_name, bits in anchor_data.items():
        if child in bits:
            child_active += 1
            if parent in bits:
                both_active += 1
            else:
                child_only.append(anchor_name)

    if child_active > 0:
        consistency = both_active / child_active
    else:
        consistency = None  # child never appears

    results.append({
        'child': child,
        'parent': parent,
        'child_capa': capa_map.get(child, '?'),
        'parent_capa': capa_map.get(parent, '?'),
        'child_active': child_active,
        'both_active': both_active,
        'consistency': consistency,
        'violations': child_only,
    })

# ========== SUMMARY BY CONSISTENCY ==========
print('PART A: Per-dependency-pair results')
print()

# Separate into categories
perfect = [r for r in results if r['consistency'] == 1.0 and r['child_active'] > 0]
high = [r for r in results if r['consistency'] is not None and 0.5 <= r['consistency'] < 1.0]
low = [r for r in results if r['consistency'] is not None and 0 < r['consistency'] < 0.5]
zero = [r for r in results if r['consistency'] == 0.0 and r['child_active'] > 0]
inactive = [r for r in results if r['child_active'] == 0]

print(f'Dependency pairs where child appears in at least 1 anchor: {len(results) - len(inactive)}')
print(f'  Perfect (100%): {len(perfect)}')
print(f'  High (50-99%):  {len(high)}')
print(f'  Low (1-49%):    {len(low)}')
print(f'  Zero (0%):      {len(zero)}')
print(f'  Child never active: {len(inactive)}')
print()

# Overall weighted consistency
total_child = sum(r['child_active'] for r in results if r['consistency'] is not None)
total_both = sum(r['both_active'] for r in results if r['consistency'] is not None)
if total_child > 0:
    overall = total_both / total_child
    print(f'OVERALL WEIGHTED CONSISTENCY: {total_both}/{total_child} = {overall*100:.1f}%')
print()

# ========== DETAIL: High consistency pairs ==========
print('PART B: Perfect consistency pairs (100%)')
print(f'{"Child":<22} {"Parent":<22} {"N":<5} {"Capa_c":<7} {"Capa_p"}')
print('-' * 65)
for r in sorted(perfect, key=lambda x: -x['child_active']):
    print(f'{r["child"]:<22} {r["parent"]:<22} {r["child_active"]:<5} {r["child_capa"]:<7} {r["parent_capa"]}')

print()
print('PART C: Imperfect consistency pairs (<100%)')
print(f'{"Child":<22} {"Parent":<22} {"Rate":<8} {"N":<5} {"Violations"}')
print('-' * 80)
for r in sorted(high + low + zero, key=lambda x: x['consistency']):
    viol_str = ', '.join(r['violations'][:5])
    if len(r['violations']) > 5:
        viol_str += f'... (+{len(r["violations"])-5})'
    print(f'{r["child"]:<22} {r["parent"]:<22} {r["consistency"]*100:5.1f}%  {r["child_active"]:<5} {viol_str}')

# ========== ANALYSIS BY LAYER GAP ==========
print()
print('PART D: Consistency by layer gap (child_capa - parent_capa)')
print()
gap_stats = defaultdict(lambda: {'total': 0, 'consistent': 0})
for r in results:
    if r['consistency'] is not None and r['child_active'] > 0:
        try:
            gap = int(r['child_capa']) - int(r['parent_capa'])
        except:
            continue
        gap_stats[gap]['total'] += r['child_active']
        gap_stats[gap]['consistent'] += r['both_active']

print(f'{"Gap":<5} {"Consistent":<12} {"Total":<8} {"Rate"}')
print('-' * 35)
for gap in sorted(gap_stats.keys()):
    s = gap_stats[gap]
    rate = s['consistent'] / s['total'] * 100 if s['total'] > 0 else 0
    print(f'{gap:<5} {s["consistent"]:<12} {s["total"]:<8} {rate:.1f}%')

# ========== INTERPRETATION ==========
print()
print('=' * 70)
print('INTERPRETATION')
print('=' * 70)
print()

# Key question: do ONTOLOGICAL dependencies show higher consistency
# than expected by chance?

# Compute baseline: for random pairs, what's the co-activation rate?
all_prim_names = [p['nombre'] for p in prims]
prim_freq = Counter()
for anchor_name, bits in anchor_data.items():
    for b in bits:
        if b in name_set:
            prim_freq[b] += 1

n_anchors = len(anchor_data)
print(f'Baseline co-activation (if independent):')
print(f'  Total anchors: {n_anchors}')
print(f'  Average primitive frequency: {sum(prim_freq.values())/len(prim_freq):.1f} / {n_anchors}')
print()

# For dependency pairs with imperfect consistency, check if the
# violation rate is LOWER than the baseline independence prediction
print('DEPENDENCY PAIRS vs RANDOM BASELINE:')
print(f'{"Child":<18} {"Parent":<18} {"Obs.rate":<10} {"Random":<10} {"Ratio":<8} {"Better?"}')
print('-' * 80)
for r in sorted(high + low + zero, key=lambda x: -x['child_active']):
    if r['child_active'] < 2:
        continue
    p_child = prim_freq.get(r['child'], 0) / n_anchors
    p_parent = prim_freq.get(r['parent'], 0) / n_anchors
    random_coact = p_parent  # P(parent | child) under independence = P(parent)
    obs_rate = r['consistency']
    if random_coact > 0:
        ratio = obs_rate / random_coact
        better = 'YES' if obs_rate > random_coact else 'no'
    else:
        ratio = float('inf')
        better = 'N/A'
    print(f'{r["child"]:<18} {r["parent"]:<18} {obs_rate*100:6.1f}%   {random_coact*100:6.1f}%   {ratio:6.2f}   {better}')

print()
print('Ratio > 1.0 means dependency increases co-activation above chance.')
print('This is the core falsifiable prediction of the framework.')
