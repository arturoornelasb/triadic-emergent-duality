"""Test 6: Abstraction-zeros correlation.
Do abstract concepts have more zeros (inactive bits) than concrete concepts?"""
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

prims = prim_data['primitivos']
capa_map = {p['nombre']: p['capa'] for p in prims}
total_bits = 63

meta_keys = {'_descripcion', '_formato', '_total_v1', '_total_v2'}
anchor_data = {}
for k, v in anclas.items():
    if k.startswith('_') or k in meta_keys:
        continue
    if isinstance(v, dict) and 'bits' in v:
        anchor_data[k] = v

print(f'Total anchors: {len(anchor_data)}')
print(f'Total bits: {total_bits}')
print()

# ========== COMPUTE ABSTRACTION LEVEL ==========
print('=' * 70)
print('TEST 6: ABSTRACTION-ZEROS CORRELATION')
print('=' * 70)
print()

# Method 1: Average layer of active bits as proxy for abstraction
# Higher average layer = more abstract (uses higher-order primitives)
# Method 2: Manual classification into concrete/abstract

# Method 1: Average layer
anchor_metrics = []
for name, data in anchor_data.items():
    bits = data['bits']
    n_active = len(bits)
    n_zeros = total_bits - n_active  # bits NOT active
    pct_zeros = n_zeros / total_bits * 100

    # Average layer of active bits
    layers = []
    for b in bits:
        if b in capa_map:
            layers.append(capa_map[b])
    avg_layer = sum(layers) / len(layers) if layers else 0

    # Max layer
    max_layer = max(layers) if layers else 0

    anchor_metrics.append({
        'name': name,
        'en': data.get('en', name),
        'n_active': n_active,
        'n_zeros': n_zeros,
        'pct_zeros': pct_zeros,
        'avg_layer': avg_layer,
        'max_layer': max_layer,
    })

# Sort by abstraction (avg_layer)
anchor_metrics.sort(key=lambda x: x['avg_layer'])

print('PART A: All anchors sorted by average layer of active bits')
print(f'{"Concept":<22} {"EN":<18} {"Active":<8} {"%Zeros":<8} {"AvgLyr":<8} {"MaxLyr"}')
print('-' * 75)
for m in anchor_metrics:
    print(f'{m["name"]:<22} {m["en"]:<18} {m["n_active"]:<8} {m["pct_zeros"]:5.1f}%  {m["avg_layer"]:5.2f}   {m["max_layer"]}')

# ========== CORRELATION ==========
print()
print('PART B: Correlation analysis')
print()

avg_layers = [m['avg_layer'] for m in anchor_metrics]
pct_zeros = [m['pct_zeros'] for m in anchor_metrics]
n_active = [m['n_active'] for m in anchor_metrics]

# Pearson correlation
def pearson(x, y):
    n = len(x)
    if n < 2:
        return 0
    mx = sum(x) / n
    my = sum(y) / n
    sx = (sum((xi - mx)**2 for xi in x) / (n-1)) ** 0.5
    sy = (sum((yi - my)**2 for yi in y) / (n-1)) ** 0.5
    if sx == 0 or sy == 0:
        return 0
    cov = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / (n-1)
    return cov / (sx * sy)

r_layer_zeros = pearson(avg_layers, pct_zeros)
r_layer_active = pearson(avg_layers, n_active)

print(f'Pearson correlation (avg_layer vs %zeros): r = {r_layer_zeros:+.4f}')
print(f'Pearson correlation (avg_layer vs n_active): r = {r_layer_active:+.4f}')
print()

# Interpretation
if r_layer_zeros > 0.1:
    print(f'RESULT: POSITIVE correlation ({r_layer_zeros:+.3f})')
    print('  Higher-layer concepts have MORE zeros (fewer active bits)')
    print('  This SUPPORTS the prediction: abstract concepts have more zeros')
elif r_layer_zeros < -0.1:
    print(f'RESULT: NEGATIVE correlation ({r_layer_zeros:+.3f})')
    print('  Higher-layer concepts have FEWER zeros (more active bits)')
    print('  This CONTRADICTS the prediction')
else:
    print(f'RESULT: NEGLIGIBLE correlation ({r_layer_zeros:+.3f})')
    print('  No relationship between abstraction level and zeros')

print()

# ========== GROUP ANALYSIS ==========
print('PART C: Grouped analysis')
print()

# Method 2: Manual classification
concrete = ['piedra', 'agua_concepto', 'hierro', 'carbono', 'oxígeno',
            'nitrógeno', 'hidrógeno', 'gravedad', 'velocidad', 'masa',
            'distancia', 'luz', 'fuego']
abstract = ['socialismo', 'capitalismo', 'democracia', 'libertad_concepto',
            'conocimiento', 'esperanza', 'desesperación', 'tolerancia',
            'confianza', 'desconfianza', 'aceptación']
emotional = ['ira', 'calma', 'miedo', 'sorpresa', 'asco', 'vergüenza',
             'culpa', 'ansiedad', 'pasión', 'felicidad']
roles = ['maestro', 'estudiante', 'doctor', 'paciente', 'líder',
         'seguidor', 'empleador', 'empleado', 'depredador', 'presa']

categories = [
    ('Concrete/Physical', concrete),
    ('Abstract/Political', abstract),
    ('Emotional', emotional),
    ('Social Roles', roles),
]

for cat_name, cat_members in categories:
    cat_metrics = [m for m in anchor_metrics if m['name'] in cat_members]
    if not cat_metrics:
        continue
    avg_active = sum(m['n_active'] for m in cat_metrics) / len(cat_metrics)
    avg_zeros_pct = sum(m['pct_zeros'] for m in cat_metrics) / len(cat_metrics)
    avg_lyr = sum(m['avg_layer'] for m in cat_metrics) / len(cat_metrics)
    print(f'{cat_name} (n={len(cat_metrics)}):')
    print(f'  Avg active bits: {avg_active:.1f}')
    print(f'  Avg %zeros: {avg_zeros_pct:.1f}%')
    print(f'  Avg layer: {avg_lyr:.2f}')
    print()

# ========== ~42% TEST ==========
print('PART D: Overall zero percentage')
print()
all_zeros = [m['pct_zeros'] for m in anchor_metrics]
overall_avg = sum(all_zeros) / len(all_zeros)
print(f'Average %zeros across all 104 anchors: {overall_avg:.1f}%')
print(f'Predicted by framework: ~42% (from BitNet convergence)')
print(f'Actual in anchor data: {overall_avg:.1f}%')
print()

# Note: anchors encode SALIENT bits, not exhaustive bits,
# so the zero percentage measures something different from
# the training-time convergence (~42% of weights to zero)
active_counts = [m['n_active'] for m in anchor_metrics]
avg_active_bits = sum(active_counts) / len(active_counts)
print(f'Average active bits per anchor: {avg_active_bits:.1f} / {total_bits}')
print(f'Average active percentage: {avg_active_bits/total_bits*100:.1f}%')
print(f'Average inactive percentage: {(1-avg_active_bits/total_bits)*100:.1f}%')

# Distribution of active bit counts
from collections import Counter
count_dist = Counter(m['n_active'] for m in anchor_metrics)
print()
print('Distribution of active bit counts:')
for n_bits in sorted(count_dist.keys()):
    bar = '#' * count_dist[n_bits]
    print(f'  {n_bits} bits: {count_dist[n_bits]:>3} {bar}')
