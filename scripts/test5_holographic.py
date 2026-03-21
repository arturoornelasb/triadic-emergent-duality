"""Test 5: Holographic principle — do identical peripheral profiles determine identical interior profiles?"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
from collections import defaultdict

DATA_DIR = r'C:\Github\triadic-microgpt\playground\danza_data'

with open(f'{DATA_DIR}/primitivos.json', 'r', encoding='utf-8') as f:
    prim_data = json.load(f)
with open(f'{DATA_DIR}/anclas_v2.json', 'r', encoding='utf-8') as f:
    anclas = json.load(f)

prims = prim_data['primitivos']
ejes = prim_data['ejes_duales']

# Identify peripheral primitives (dual poles from ejes_duales)
peripheral = set()
for pair in ejes:
    for p in pair:
        peripheral.add(p)

# Interior = everything else
all_names = {p['nombre'] for p in prims}
interior = all_names - peripheral

print(f'Dual axes: {len(ejes)} pairs')
print(f'Peripheral primitives (dual poles): {len(peripheral)}')
print(f'  {sorted(peripheral)}')
print(f'Interior primitives (non-dual): {len(interior)}')
print(f'  {sorted(interior)[:20]}...')
print()

# Filter anchors
meta_keys = {'_descripcion', '_formato', '_total_v1', '_total_v2'}
anchor_data = {}
for k, v in anclas.items():
    if k.startswith('_') or k in meta_keys:
        continue
    if isinstance(v, dict) and 'bits' in v:
        anchor_data[k] = set(v['bits'])

print(f'Total anchors: {len(anchor_data)}')
print()

# ========== TEST ==========
print('=' * 70)
print('TEST 5: HOLOGRAPHIC DETERMINATION')
print('Does the peripheral profile determine the interior profile?')
print('=' * 70)
print()

# For each anchor, extract peripheral and interior profiles
profiles = {}
for name, bits in anchor_data.items():
    periph_profile = frozenset(bits & peripheral)
    inter_profile = frozenset(bits & interior)
    profiles[name] = (periph_profile, inter_profile)

# Group by peripheral profile
periph_groups = defaultdict(list)
for name, (pp, ip) in profiles.items():
    periph_groups[pp].append((name, ip))

# Check: for each group with >1 anchor, are interior profiles identical?
groups_with_multiple = {pp: members for pp, members in periph_groups.items() if len(members) > 1}

print(f'Distinct peripheral profiles: {len(periph_groups)}')
print(f'Profiles with multiple anchors: {len(groups_with_multiple)}')
print()

total_pairs = 0
consistent_pairs = 0
inconsistent_pairs = 0
inconsistent_details = []

for pp, members in groups_with_multiple.items():
    interior_profiles = [ip for _, ip in members]
    names = [n for n, _ in members]
    # Check all pairs
    for i in range(len(members)):
        for j in range(i+1, len(members)):
            total_pairs += 1
            if interior_profiles[i] == interior_profiles[j]:
                consistent_pairs += 1
            else:
                inconsistent_pairs += 1
                diff = interior_profiles[i].symmetric_difference(interior_profiles[j])
                inconsistent_details.append((names[i], names[j], pp, diff))

if total_pairs > 0:
    rate = consistent_pairs / total_pairs * 100
    print(f'Total pairs with same peripheral profile: {total_pairs}')
    print(f'Pairs with IDENTICAL interior: {consistent_pairs} ({rate:.1f}%)')
    print(f'Pairs with DIFFERENT interior: {inconsistent_pairs} ({100-rate:.1f}%)')
else:
    print('No pairs share peripheral profiles — holographic test is TRIVIALLY TRUE')
    print('(Every anchor has a unique peripheral profile)')
    rate = 100.0

print()

# Show the groups
print('PERIPHERAL PROFILE GROUPS:')
for pp, members in sorted(periph_groups.items(), key=lambda x: -len(x[1])):
    if len(members) > 1:
        names = [n for n, _ in members]
        print(f'\n  Profile: {sorted(pp)}')
        for name, ip in members:
            print(f'    {name}: interior = {sorted(ip)}')

if inconsistent_details:
    print()
    print('INCONSISTENCIES:')
    for n1, n2, pp, diff in inconsistent_details:
        print(f'  {n1} vs {n2}')
        print(f'    Shared peripheral: {sorted(pp)}')
        print(f'    Interior difference: {sorted(diff)}')

# ========== RELAXED TEST ==========
print()
print('=' * 70)
print('RELAXED HOLOGRAPHIC TEST')
print('(Using similarity instead of exact match)')
print('=' * 70)
print()

# For pairs with same peripheral profile, compute Jaccard similarity of interior
if total_pairs > 0:
    similarities = []
    for pp, members in groups_with_multiple.items():
        interior_profiles = [ip for _, ip in members]
        for i in range(len(members)):
            for j in range(i+1, len(members)):
                union = interior_profiles[i] | interior_profiles[j]
                intersection = interior_profiles[i] & interior_profiles[j]
                if len(union) > 0:
                    jaccard = len(intersection) / len(union)
                else:
                    jaccard = 1.0
                similarities.append(jaccard)

    avg_sim = sum(similarities) / len(similarities)
    print(f'Average Jaccard similarity of interior profiles (same peripheral): {avg_sim:.3f}')

# Compare with baseline: random pairs
import random
random.seed(42)
all_anchors = list(profiles.keys())
baseline_sims = []
for _ in range(min(1000, len(all_anchors) * (len(all_anchors)-1) // 2)):
    a, b = random.sample(all_anchors, 2)
    _, ip_a = profiles[a]
    _, ip_b = profiles[b]
    union = ip_a | ip_b
    intersection = ip_a & ip_b
    if len(union) > 0:
        baseline_sims.append(len(intersection) / len(union))
    else:
        baseline_sims.append(1.0)

avg_baseline = sum(baseline_sims) / len(baseline_sims) if baseline_sims else 0
print(f'Average Jaccard similarity of interior profiles (random pairs): {avg_baseline:.3f}')
if avg_baseline > 0:
    print(f'Ratio (same-peripheral / random): {avg_sim/avg_baseline:.2f}x')
print()

# ========== PERIPHERAL DETERMINATION POWER ==========
print('=' * 70)
print('PERIPHERAL DETERMINATION POWER')
print('=' * 70)
print()

# For each interior primitive, how well does the peripheral profile predict it?
# For each interior bit, compute correlation with peripheral bits

for interior_bit in sorted(interior):
    # Count: how many anchors have this interior bit active?
    has_bit = [n for n, bits in anchor_data.items() if interior_bit in bits]
    if len(has_bit) < 3:
        continue

    # What peripheral bits best predict this interior bit?
    best_predictors = []
    for periph_bit in sorted(peripheral):
        has_both = sum(1 for n in has_bit if periph_bit in anchor_data[n])
        has_periph = sum(1 for n, bits in anchor_data.items() if periph_bit in bits)
        if has_periph > 0:
            precision = has_both / has_periph
            recall = has_both / len(has_bit) if len(has_bit) > 0 else 0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
            if f1 > 0.3:
                best_predictors.append((periph_bit, f1, precision, recall))

    if best_predictors:
        best_predictors.sort(key=lambda x: -x[1])
        top = best_predictors[0]
        print(f'  {interior_bit} (n={len(has_bit)}): best predictor = {top[0]} (F1={top[1]:.2f}, prec={top[2]:.2f}, rec={top[3]:.2f})')
