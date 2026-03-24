"""Test 1: Dependency consistency and branch independence in anclas_v2.json"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import os
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data')

with open(f'{DATA_DIR}/primitivos.json', 'r', encoding='utf-8') as f:
    prim_data = json.load(f)
with open(f'{DATA_DIR}/anclas_v2.json', 'r', encoding='utf-8') as f:
    anclas = json.load(f)

prims = {p['nombre']: p for p in prim_data['primitivos']}
deps_map = {p['nombre']: set(p['deps']) for p in prim_data['primitivos']}

branch_a = {'contención', 'vida', 'consciente'}
branch_b = {'porque', 'si_entonces'}
branch_c = {'tipo_de'}

meta_keys = {'_descripcion', '_formato', '_total_v1', '_total_v2'}
anchor_names = [k for k in anclas.keys() if k not in meta_keys]

print(f'Total anchors: {len(anchor_names)}')
print()

# ========== TEST 1A: Dependency Consistency ==========
print('=' * 60)
print('TEST 1A: DEPENDENCY CONSISTENCY IN ANCHORS')
print('=' * 60)
print()

dep_checks = [
    ('consciente', 'vida'),
    ('consciente', 'información'),
    ('vida', 'contención'),
    ('vida', 'creación'),
    ('vida', 'flujo_temporal'),
    ('vida', 'orden'),
    ('bien', 'contención'),
    ('mal', 'contención'),
    ('control', 'contención'),
    ('saber', 'consciente'),
    ('pensar', 'consciente'),
    ('querer', 'consciente'),
    ('decir', 'consciente'),
    ('individual', 'contención'),
    ('interocepción', 'vida'),
    ('porque', 'posición_temporal'),
    ('tipo_de', 'información'),
    ('tipo_de', 'orden'),
]

total_checks = 0
violations = 0
violation_details = []

for anchor_name in anchor_names:
    bits = set(anclas[anchor_name]['bits'])
    for child, parent in dep_checks:
        if child in bits:
            total_checks += 1
            if parent not in bits:
                violations += 1
                violation_details.append((anchor_name, child, parent))

print(f'Dependency pairs checked: {len(dep_checks)}')
print(f'Total instances where child was active: {total_checks}')
print(f'Violations (child active, parent missing): {violations}')
if total_checks > 0:
    print(f'Consistency rate: {(total_checks - violations) / total_checks * 100:.1f}%')
print()

if violations > 0:
    print('VIOLATIONS:')
    # Group by dependency pair
    from collections import Counter
    pair_counts = Counter()
    for a, c, p in violation_details:
        pair_counts[(c, p)] += 1

    print(f'\nBy dependency pair:')
    for (c, p), count in pair_counts.most_common():
        # Count how many times child appears total
        child_total = sum(1 for a in anchor_names if c in set(anclas[a]['bits']))
        print(f'  {c} -> {p}: {count} violations / {child_total} occurrences ({count/child_total*100:.0f}% violation rate)')

    print(f'\nDetailed violations:')
    for a, c, p in violation_details[:30]:
        print(f'  {a}: {c} active but {p} MISSING')
    if len(violation_details) > 30:
        print(f'  ... and {len(violation_details) - 30} more')
print()

# ========== TEST 1B: Branch Independence ==========
print('=' * 60)
print('TEST 1B: BRANCH INDEPENDENCE (CO-ACTIVATION)')
print('=' * 60)
print()

branch_a_count = 0
branch_b_count = 0
branch_c_count = 0
ab_co = 0
ac_co = 0
bc_co = 0
abc_co = 0

contencion_count = 0
vida_count = 0
consciente_count = 0
porque_count = 0
tipo_de_count = 0

for anchor_name in anchor_names:
    bits = set(anclas[anchor_name]['bits'])

    has_a = bool(bits & branch_a)
    has_b = bool(bits & branch_b)
    has_c = bool(bits & branch_c)

    if has_a: branch_a_count += 1
    if has_b: branch_b_count += 1
    if has_c: branch_c_count += 1
    if has_a and has_b: ab_co += 1
    if has_a and has_c: ac_co += 1
    if has_b and has_c: bc_co += 1
    if has_a and has_b and has_c: abc_co += 1

    if 'contención' in bits: contencion_count += 1
    if 'vida' in bits: vida_count += 1
    if 'consciente' in bits: consciente_count += 1
    if 'porque' in bits: porque_count += 1
    if 'tipo_de' in bits: tipo_de_count += 1

n = len(anchor_names)
print(f'Branch activation frequencies (of {n} anchors):')
print(f'  Branch A (contención/vida/consciente): {branch_a_count} ({branch_a_count/n*100:.0f}%)')
print(f'  Branch B (porque/si_entonces):         {branch_b_count} ({branch_b_count/n*100:.0f}%)')
print(f'  Branch C (tipo_de):                    {branch_c_count} ({branch_c_count/n*100:.0f}%)')
print()
print(f'Individual primitive frequencies:')
print(f'  contención: {contencion_count} ({contencion_count/n*100:.0f}%)')
print(f'  vida:       {vida_count} ({vida_count/n*100:.0f}%)')
print(f'  consciente: {consciente_count} ({consciente_count/n*100:.0f}%)')
print(f'  porque:     {porque_count} ({porque_count/n*100:.0f}%)')
print(f'  tipo_de:    {tipo_de_count} ({tipo_de_count/n*100:.0f}%)')
print()
print(f'Co-activation:')
exp_ab = branch_a_count * branch_b_count / n if n > 0 else 0
exp_ac = branch_a_count * branch_c_count / n if n > 0 else 0
exp_bc = branch_b_count * branch_c_count / n if n > 0 else 0
print(f'  A+B: {ab_co} (expected if independent: {exp_ab:.1f})')
print(f'  A+C: {ac_co} (expected if independent: {exp_ac:.1f})')
print(f'  B+C: {bc_co} (expected if independent: {exp_bc:.1f})')
print(f'  A+B+C: {abc_co}')
print()

print('Independence ratios (observed/expected, 1.0 = perfectly independent):')
if exp_ab > 0: print(f'  A+B: {ab_co/exp_ab:.2f}')
if exp_ac > 0: print(f'  A+C: {ac_co/exp_ac:.2f}')
if exp_bc > 0: print(f'  B+C: {bc_co/exp_bc:.2f}')
print()

# ========== TEST 1C: Branch-specific anchor profiles ==========
print('=' * 60)
print('TEST 1C: BRANCH-EXCLUSIVE ACTIVATIONS')
print('=' * 60)
print()

a_only = []
b_only = []
c_only = []
none_branches = []

for anchor_name in anchor_names:
    bits = set(anclas[anchor_name]['bits'])
    has_a = bool(bits & branch_a)
    has_b = bool(bits & branch_b)
    has_c = bool(bits & branch_c)

    if has_a and not has_b and not has_c: a_only.append(anchor_name)
    if has_b and not has_a and not has_c: b_only.append(anchor_name)
    if has_c and not has_a and not has_b: c_only.append(anchor_name)
    if not has_a and not has_b and not has_c: none_branches.append(anchor_name)

print(f'Branch A only (no B, no C): {len(a_only)} anchors')
print(f'  Examples: {a_only[:8]}')
print(f'Branch B only (no A, no C): {len(b_only)} anchors')
print(f'  Examples: {b_only[:8]}')
print(f'Branch C only (no A, no B): {len(c_only)} anchors')
print(f'  Examples: {c_only[:8]}')
print(f'No branch active: {len(none_branches)} anchors')
print(f'  Examples: {none_branches[:8]}')
