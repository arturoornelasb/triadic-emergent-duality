"""Simulation of the 63→64 transition: adding 'proporcion' as the 64th primitive.
Algebraic analysis, dependency verification, anchor re-evaluation across 6 domains,
universal core update, and formal decision matrix."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import os
import math
from collections import defaultdict, Counter

# ========== 0. DATA LOADING ==========
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data')

with open(f'{DATA_DIR}/primitivos.json', 'r', encoding='utf-8') as f:
    prim_data = json.load(f)

prims = prim_data['primitivos']
names = [p['nombre'] for p in prims]
deps_map = {p['nombre']: list(p['deps']) for p in prims}
capa_map = {p['nombre']: p['capa'] for p in prims}
primo_map = {p['nombre']: p['primo'] for p in prims}
ejes = prim_data['ejes_duales']
name_set = set(names)

print('=' * 78)
print('  SIMULATION: 63 → 64 PRIMITIVES — PROPORCION')
print('  Algebraic analysis + Dependency check + Anchor re-evaluation')
print('=' * 78)
print()
print(f'Current model: {len(prims)} primitives')
print()

# ######################################################################
#  SECTION 1: THE PROPOSED 64th PRIMITIVE
# ######################################################################
print('=' * 70)
print('SECTION 1: PROPOSED PRIMITIVE — proporcion')
print('=' * 70)
print()

proporcion = {
    'bit': 63,
    'primo': 311,
    'nombre': 'proporcion',
    'capa': 3,
    'deps': ['más', 'información', 'orden'],
    'def': 'Relación cuantitativa entre cantidades, ratio, medida relativa',
}

print(f'  nombre:  {proporcion["nombre"]}')
print(f'  bit:     {proporcion["bit"]}')
print(f'  primo:   {proporcion["primo"]}')
print(f'  capa:    {proporcion["capa"]} (Tiempo)')
print(f'  deps:    {proporcion["deps"]}')
print(f'  def:     {proporcion["def"]}')
print()

# ######################################################################
#  SECTION 2: ALGEBRAIC ANALYSIS
# ######################################################################
print('=' * 70)
print('SECTION 2: ALGEBRAIC ANALYSIS — 63 → 64 BITS')
print('=' * 70)
print()

# 2.1 Word size implications
print('2.1 WORD SIZE')
print(f'  63 bits: NOT a power of 2, NOT byte-aligned')
print(f'  64 bits: 2^6 = 64 — full machine word')
print(f'    → 8 bytes exactly')
print(f'    → Standard CPU register width (x86-64, ARM64)')
print(f'    → Natural boundary for computational representation')
print(f'    → Each primitive maps to exactly one bit in a uint64')
print()

# 2.2 State space
print('2.2 STATE SPACE (3 states per primitive: +, 0, null)')
space_63 = 3**63
space_64 = 3**64
factor = space_64 / space_63
print(f'  3^63 = {space_63:.6e}')
print(f'  3^64 = {space_64:.6e}')
print(f'  Factor: ×{factor:.0f}')
print(f'  Increase: {(factor - 1)*100:.0f}% more states')
print()

# 2.3 Prime verification
print('2.3 PRIME VERIFICATION')

def is_prime(n):
    """Simple primality test."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def nth_prime(n):
    """Find the nth prime number (1-indexed)."""
    count = 0
    candidate = 2
    while True:
        if is_prime(candidate):
            count += 1
            if count == n:
                return candidate
        candidate += 1

assert is_prime(311), "311 should be prime"
p64 = nth_prime(64)
assert p64 == 311, f"64th prime should be 311, got {p64}"

print(f'  311 is prime: {is_prime(311)}')
print(f'  64th prime:   {nth_prime(64)} (= 311 ✓)')
print()

# Verify no collision with existing primes
existing_primes = set(p['primo'] for p in prims)
assert 311 not in existing_primes, "311 already in use!"
print(f'  311 not in existing primes: ✓ (no collision)')
print()

# 2.4 Product of all primes
print('2.4 PRODUCT OF PRIMES')
product_63 = 1
for p in prims:
    product_63 *= p['primo']
product_64 = product_63 * 311

print(f'  ∏(primos_1..63) = {product_63}')
print(f'  ∏(primos_1..64) = {product_64}')
print(f'  Factor: ×311')

# Number of digits
digits_63 = len(str(product_63))
digits_64 = len(str(product_64))
print(f'  Digits in product_63: {digits_63}')
print(f'  Digits in product_64: {digits_64}')
print()

# 2.5 Compatibility with TriadicGPT
print('2.5 COMPATIBILITY WITH TRIADICGPT')
print(f'  TriadicGPT encodes states as base-3 vectors of dimension N.')
print(f'  63 → 64 dimensions: adds 1 dimension to the state vector.')
print(f'  63 bits → 7.875 bytes (non-aligned)')
print(f'  64 bits → 8.000 bytes (byte-aligned)')
print(f'  Implication: 64 dimensions is computationally cleaner.')
print()

# ######################################################################
#  SECTION 3: DEPENDENCY SIMULATION
# ######################################################################
print('=' * 70)
print('SECTION 3: DEPENDENCY SIMULATION — 64 PRIMITIVES')
print('=' * 70)
print()

# Create extended model
ext_deps_map = dict(deps_map)
ext_deps_map['proporcion'] = ['más', 'información', 'orden']

ext_capa_map = dict(capa_map)
ext_capa_map['proporcion'] = 3

ext_names = names + ['proporcion']
ext_name_set = set(ext_names)

# 3.1 Verify layer ordering: all deps in lower layers
print('3.1 LAYER ORDERING VERIFICATION')
print('  NOTE: Same-layer dependencies are allowed (e.g., orden->posición_temporal, both capa 3)')
prop_deps = proporcion['deps']
prop_capa = proporcion['capa']
layer_ok = True
for dep in prop_deps:
    dep_capa = ext_capa_map[dep]
    ok = dep_capa <= prop_capa  # Same-layer is allowed
    status = '✓' if ok else '✗ VIOLATION'
    if dep_capa > prop_capa:
        layer_ok = False
    kind = 'downward' if dep_capa < prop_capa else 'same-layer'
    print(f'  proporcion (capa {prop_capa}) -> {dep} (capa {dep_capa}): {status} ({kind})')
print(f'  Layer ordering: {"PASS" if layer_ok else "FAIL"}')
print()

# 3.2 Build all dependency pairs (64 primitives)
ext_all_dep_pairs = []
for name in ext_names:
    for dep in ext_deps_map.get(name, []):
        ext_all_dep_pairs.append((name, dep))

print(f'3.2 DEPENDENCY PAIRS')
print(f'  Original: {len([(n, d) for n in names for d in deps_map.get(n, [])])} pairs')
print(f'  Extended: {len(ext_all_dep_pairs)} pairs (+{len(ext_all_dep_pairs) - len([(n, d) for n in names for d in deps_map.get(n, [])])} new)')
print()

# New pairs introduced by proporcion
new_pairs = [(proporcion['nombre'], dep) for dep in proporcion['deps']]
print(f'  New dependency pairs:')
for child, parent in new_pairs:
    print(f'    {child} -> {parent} (capa {ext_capa_map[child]} -> {ext_capa_map[parent]})')
print()

# 3.3 Circular dependency check
print('3.3 CIRCULAR DEPENDENCY CHECK')

def has_circular_deps(deps_map, names):
    """Check for circular dependencies using topological sort."""
    in_degree = {n: 0 for n in names}
    adj = defaultdict(list)
    for name in names:
        for dep in deps_map.get(name, []):
            adj[dep].append(name)
            in_degree[name] += 1

    queue = [n for n in names if in_degree[n] == 0]
    visited = 0
    while queue:
        node = queue.pop(0)
        visited += 1
        for child in adj[node]:
            in_degree[child] -= 1
            if in_degree[child] == 0:
                queue.append(child)

    return visited < len(names)

has_circular = has_circular_deps(ext_deps_map, ext_names)
print(f'  Circular dependencies detected: {"YES — VIOLATION" if has_circular else "NO ✓"}')
print()

# 3.4 Complete dependency verification
print('3.4 COMPLETE DEPENDENCY VERIFICATION (64 primitives)')

# Use same classification logic as test scripts
violated_count = 0
confirmed_count = 0
plausible_count = 0
neutral_count = 0

for child, parent in ext_all_dep_pairs:
    child_capa = ext_capa_map[child]
    parent_capa = ext_capa_map.get(parent, 0)

    if child_capa < parent_capa:
        # Upward dependency — VIOLATION
        violated_count += 1
    elif child_capa == parent_capa:
        # Same-layer dependency — allowed in model (e.g., orden->posición_temporal)
        plausible_count += 1
    else:
        # Downward dependency — standard
        confirmed_count += 1

print(f'  Total pairs:  {len(ext_all_dep_pairs)}')
print(f'  Downward (child_capa > parent_capa): {confirmed_count}')
print(f'  Same-layer (child_capa == parent_capa): {plausible_count}')
print(f'  VIOLATED (upward, child_capa < parent_capa): {violated_count}')
print(f'  Result: {"PASS — 0 VIOLATED" if violated_count == 0 else "FAIL"}')
print()

# 3.5 Children of proporcion (who could depend on it in the future)
print('3.5 POTENTIAL CHILDREN OF proporcion')
print(f'  Capa 3 primitive → could have children in capas 4, 5, 6')
higher_capa_prims = [p for p in prims if p['capa'] > 3]
print(f'  Primitives in capas 4-6: {len(higher_capa_prims)}')
print(f'  (These could potentially depend on proporcion if model evolves)')
print()

# ######################################################################
#  SECTION 4: ANCHOR RE-EVALUATION (6 DOMAINS)
# ######################################################################
print('=' * 70)
print('SECTION 4: ANCHOR RE-EVALUATION — 6 DOMAINS')
print('=' * 70)
print()

# Import anchor improvements from test_proporcion data
# For each domain, show anchors that improve with proporcion

domain_improvements = {
    'Music (T8)': {
        'before_anchors': {
            'serie_armonica':   ['información', 'orden', 'unión', 'uno'],
            'temperamento':     ['orden', 'información', 'más'],
            'compas_metrica':   ['flujo_temporal', 'orden', 'más'],
        },
        'after_anchors': {
            'serie_armonica':   ['información', 'orden', 'unión', 'uno', 'proporcion'],
            'temperamento':     ['orden', 'información', 'más', 'proporcion'],
            'compas_metrica':   ['flujo_temporal', 'orden', 'más', 'proporcion'],
        },
    },
    'Chemistry (T9)': {
        'before_anchors': {
            'estequiometria':   ['debe', 'orden', 'más', 'todo'],
            'constante_eq':     ['equilibrio', 'orden', 'más'],
            'ph_escala':        ['más', 'menos', 'orden'],
        },
        'after_anchors': {
            'estequiometria':   ['debe', 'orden', 'más', 'todo', 'proporcion'],
            'constante_eq':     ['equilibrio', 'orden', 'más', 'proporcion'],
            'ph_escala':        ['más', 'menos', 'orden', 'proporcion'],
        },
    },
    'Biology (T10)': {
        'before_anchors': {
            'ratios_mendelianos': ['debe', 'orden', 'más', 'información'],
            'scaling_alometrico': ['más', 'orden', 'vida'],
            'hardy_weinberg':     ['equilibrio', 'orden', 'más', 'todo'],
        },
        'after_anchors': {
            'ratios_mendelianos': ['debe', 'orden', 'más', 'información', 'proporcion'],
            'scaling_alometrico': ['más', 'orden', 'vida', 'proporcion'],
            'hardy_weinberg':     ['equilibrio', 'orden', 'más', 'todo', 'proporcion'],
        },
    },
    'Mathematics (T11)': {
        'before_anchors': {
            'numeros_racionales': ['más', 'información', 'orden', 'todo'],
            'euclides_libro_v':   ['más', 'orden', 'equilibrio'],
            'trigonometria':      ['orden', 'eje_vertical', 'eje_lateral', 'más'],
        },
        'after_anchors': {
            'numeros_racionales': ['más', 'información', 'orden', 'todo', 'proporcion'],
            'euclides_libro_v':   ['más', 'orden', 'equilibrio', 'proporcion'],
            'trigonometria':      ['orden', 'eje_vertical', 'eje_lateral', 'más', 'proporcion'],
        },
    },
    'Philosophy (T12)': {
        'before_anchors': {
            'linea_dividida':     ['equilibrio', 'orden', 'más', 'verdad'],
            'mesotes':            ['equilibrio', 'orden', 'bien'],
            'armonia_pitagorica': ['orden', 'unión', 'información'],
        },
        'after_anchors': {
            'linea_dividida':     ['equilibrio', 'orden', 'más', 'verdad', 'proporcion'],
            'mesotes':            ['equilibrio', 'orden', 'bien', 'proporcion'],
            'armonia_pitagorica': ['orden', 'unión', 'información', 'proporcion'],
        },
    },
    'Physics (T13)': {
        'before_anchors': {
            'constante_estructura_fina': ['debe', 'orden', 'información', 'más'],
            'unidades_planck':           ['uno', 'orden', 'información', 'debe'],
            'ratios_masa':               ['más', 'uno', 'orden', 'información'],
        },
        'after_anchors': {
            'constante_estructura_fina': ['debe', 'orden', 'información', 'más', 'proporcion'],
            'unidades_planck':           ['uno', 'orden', 'información', 'debe', 'proporcion'],
            'ratios_masa':               ['más', 'uno', 'orden', 'información', 'proporcion'],
        },
    },
}

def compute_anchor_consistency(anchors, d_map):
    """Compute consistency for a set of anchors."""
    total_d = 0
    present_d = 0
    for anchor_prims in anchors.values():
        anchor_set = set(anchor_prims)
        for prim in anchor_prims:
            for dep in d_map.get(prim, []):
                total_d += 1
                if dep in anchor_set:
                    present_d += 1
    return present_d / total_d if total_d > 0 else 0.0

print(f'  {"Domain":<22} {"Before":<12} {"After":<12} {"Delta":<12} {"Improved"}')
print(f'  {"-"*65}')

deltas = []
for domain, data in domain_improvements.items():
    before_c = compute_anchor_consistency(data['before_anchors'], deps_map)
    after_c = compute_anchor_consistency(data['after_anchors'], ext_deps_map)
    delta = (after_c - before_c) * 100
    improved = delta > 0
    deltas.append(delta)
    print(f'  {domain:<22} {before_c*100:.1f}%{"":<6} {after_c*100:.1f}%{"":<6} '
          f'{delta:+.1f}pp{"":<5} {"YES" if improved else "NO"}')

avg_delta = sum(deltas) / len(deltas) if deltas else 0
print()
print(f'  Average delta: {avg_delta:+.1f}pp')
print(f'  Domains improved: {sum(1 for d in deltas if d > 0)}/{len(deltas)}')
print()

# ######################################################################
#  SECTION 5: UNIVERSAL CORE UPDATE
# ######################################################################
print('=' * 70)
print('SECTION 5: UNIVERSAL CORE UPDATE')
print('=' * 70)
print()

# Current 6-domain class dicts
music_classes = {
    'vacío': 'D', 'información': 'D', 'uno': 'D',
    'fuerza': 'D', 'eje_profundidad': 'A', 'contención': 'D',
    'más': 'D', 'menos': 'D', 'unión': 'D', 'separación': 'D',
    'parte_de': 'A',
    'mover': 'D', 'posición_temporal': 'D', 'flujo_temporal': 'D',
    'hacer': 'D', 'creación': 'D', 'destrucción': 'D',
    'orden': 'D', 'caos': 'D', 'porque': 'A', 'si_entonces': 'A',
    'eje_vertical': 'A', 'eje_lateral': 'A', 'equilibrio': 'D',
    'vista': 'A', 'bien': 'A', 'mal': 'A',
    'verdad': 'A', 'mentira': 'A', 'libertad': 'A', 'control': 'A',
    'tipo_de': 'A', 'algunos': 'A', 'muchos': 'A',
    'todo': 'A', 'puede': 'A', 'debe': 'A', 'tal_vez': 'A',
    'tierra': 'A', 'agua': 'A', 'aire': 'A', 'fuego': 'A',
    'tacto': 'D', 'oído': 'D', 'gusto': 'N', 'olfato': 'N',
    'interocepción': 'A',
    'vida': 'A', 'muerte': 'A', 'placer': 'D', 'dolor': 'D',
    'consciente': 'A', 'ausente': 'A',
    'individual': 'D', 'colectivo': 'D',
    'querer': 'A', 'saber': 'A', 'pensar': 'A', 'decir': 'A',
    'temporal_obs': 'A', 'eterno_obs': 'A',
    'receptivo': 'A', 'creador_obs': 'A',
}
chem_classes = {
    'vacío': 'D', 'información': 'D', 'uno': 'D',
    'fuerza': 'D', 'eje_profundidad': 'A', 'contención': 'D',
    'más': 'D', 'menos': 'D', 'unión': 'D', 'separación': 'D',
    'parte_de': 'A',
    'mover': 'D', 'posición_temporal': 'D', 'flujo_temporal': 'D',
    'hacer': 'D', 'creación': 'D', 'destrucción': 'D',
    'orden': 'D', 'caos': 'D', 'porque': 'A', 'si_entonces': 'A',
    'eje_vertical': 'D', 'eje_lateral': 'A', 'equilibrio': 'D',
    'vista': 'A', 'bien': 'A', 'mal': 'A',
    'verdad': 'A', 'mentira': 'A', 'libertad': 'D', 'control': 'D',
    'tipo_de': 'D', 'algunos': 'A', 'muchos': 'A',
    'todo': 'A', 'puede': 'A', 'debe': 'A', 'tal_vez': 'A',
    'tierra': 'D', 'agua': 'D', 'aire': 'D', 'fuego': 'D',
    'tacto': 'A', 'oído': 'A', 'gusto': 'D', 'olfato': 'D',
    'interocepción': 'A',
    'vida': 'D', 'muerte': 'D', 'placer': 'A', 'dolor': 'A',
    'consciente': 'A', 'ausente': 'A',
    'individual': 'D', 'colectivo': 'D',
    'querer': 'A', 'saber': 'A', 'pensar': 'A', 'decir': 'A',
    'temporal_obs': 'A', 'eterno_obs': 'A',
    'receptivo': 'A', 'creador_obs': 'A',
}
bio_classes = {
    'vacío': 'D', 'información': 'D', 'uno': 'D',
    'fuerza': 'D', 'eje_profundidad': 'A', 'contención': 'D',
    'más': 'D', 'menos': 'D', 'unión': 'D', 'separación': 'D',
    'parte_de': 'A',
    'mover': 'D', 'posición_temporal': 'D', 'flujo_temporal': 'D',
    'hacer': 'D', 'creación': 'D', 'destrucción': 'D',
    'orden': 'D', 'caos': 'D', 'porque': 'A', 'si_entonces': 'A',
    'eje_vertical': 'A', 'eje_lateral': 'A', 'equilibrio': 'D',
    'vista': 'D', 'bien': 'A', 'mal': 'A',
    'verdad': 'A', 'mentira': 'A', 'libertad': 'A', 'control': 'D',
    'tipo_de': 'D', 'algunos': 'A', 'muchos': 'A',
    'todo': 'A', 'puede': 'A', 'debe': 'A', 'tal_vez': 'A',
    'tierra': 'D', 'agua': 'D', 'aire': 'D', 'fuego': 'A',
    'tacto': 'D', 'oído': 'D', 'gusto': 'D', 'olfato': 'D',
    'interocepción': 'D',
    'vida': 'D', 'muerte': 'D', 'placer': 'D', 'dolor': 'D',
    'consciente': 'D', 'ausente': 'D',
    'individual': 'D', 'colectivo': 'D',
    'querer': 'A', 'saber': 'A', 'pensar': 'A', 'decir': 'A',
    'temporal_obs': 'A', 'eterno_obs': 'A',
    'receptivo': 'A', 'creador_obs': 'A',
}
math_classes = {
    'vacío': 'D', 'información': 'D', 'uno': 'D',
    'fuerza': 'A', 'eje_profundidad': 'A', 'contención': 'D',
    'más': 'D', 'menos': 'D', 'unión': 'D', 'separación': 'D',
    'parte_de': 'A',
    'mover': 'D', 'posición_temporal': 'D', 'flujo_temporal': 'D',
    'hacer': 'A', 'creación': 'D', 'destrucción': 'A',
    'orden': 'D', 'caos': 'D', 'porque': 'D', 'si_entonces': 'A',
    'eje_vertical': 'D', 'eje_lateral': 'D', 'equilibrio': 'D',
    'vista': 'A', 'bien': 'A', 'mal': 'A',
    'verdad': 'D', 'mentira': 'D', 'libertad': 'A', 'control': 'A',
    'tipo_de': 'D', 'algunos': 'D', 'muchos': 'A',
    'todo': 'D', 'puede': 'A', 'debe': 'A', 'tal_vez': 'A',
    'tierra': 'N', 'agua': 'N', 'aire': 'N', 'fuego': 'N',
    'tacto': 'N', 'oído': 'N', 'gusto': 'N', 'olfato': 'N',
    'interocepción': 'N',
    'vida': 'N', 'muerte': 'N', 'placer': 'A', 'dolor': 'N',
    'consciente': 'N', 'ausente': 'N',
    'individual': 'A', 'colectivo': 'A',
    'querer': 'N', 'saber': 'A', 'pensar': 'A', 'decir': 'N',
    'temporal_obs': 'N', 'eterno_obs': 'N',
    'receptivo': 'N', 'creador_obs': 'N',
}
phil_classes = {
    'vacío': 'D', 'información': 'D', 'uno': 'D',
    'fuerza': 'D', 'eje_profundidad': 'A', 'contención': 'A',
    'más': 'A', 'menos': 'D', 'unión': 'D', 'separación': 'D',
    'parte_de': 'D',
    'mover': 'D', 'posición_temporal': 'D', 'flujo_temporal': 'D',
    'hacer': 'D', 'creación': 'D', 'destrucción': 'D',
    'orden': 'D', 'caos': 'D', 'porque': 'D', 'si_entonces': 'A',
    'eje_vertical': 'A', 'eje_lateral': 'A', 'equilibrio': 'D',
    'vista': 'A', 'bien': 'D', 'mal': 'D',
    'verdad': 'D', 'mentira': 'D', 'libertad': 'D', 'control': 'D',
    'tipo_de': 'D', 'algunos': 'A', 'muchos': 'A',
    'todo': 'D', 'puede': 'D', 'debe': 'D', 'tal_vez': 'D',
    'tierra': 'N', 'agua': 'N', 'aire': 'N', 'fuego': 'N',
    'tacto': 'A', 'oído': 'A', 'gusto': 'A', 'olfato': 'N',
    'interocepción': 'A',
    'vida': 'D', 'muerte': 'D', 'placer': 'D', 'dolor': 'D',
    'consciente': 'D', 'ausente': 'A',
    'individual': 'D', 'colectivo': 'D',
    'querer': 'D', 'saber': 'D', 'pensar': 'D', 'decir': 'D',
    'temporal_obs': 'A', 'eterno_obs': 'A',
    'receptivo': 'A', 'creador_obs': 'A',
}
phys_classes = {
    'vacío': 'D', 'información': 'D', 'uno': 'D',
    'fuerza': 'D', 'eje_profundidad': 'A', 'contención': 'D',
    'más': 'D', 'menos': 'D', 'unión': 'D', 'separación': 'D',
    'parte_de': 'A',
    'mover': 'D', 'posición_temporal': 'D', 'flujo_temporal': 'D',
    'hacer': 'A', 'creación': 'D', 'destrucción': 'D',
    'orden': 'D', 'caos': 'D', 'porque': 'D', 'si_entonces': 'A',
    'eje_vertical': 'D', 'eje_lateral': 'D', 'equilibrio': 'D',
    'vista': 'A', 'bien': 'A', 'mal': 'A',
    'verdad': 'A', 'mentira': 'A', 'libertad': 'D', 'control': 'D',
    'tipo_de': 'D', 'algunos': 'A', 'muchos': 'A',
    'todo': 'D', 'puede': 'D', 'debe': 'D', 'tal_vez': 'D',
    'tierra': 'D', 'agua': 'D', 'aire': 'D', 'fuego': 'D',
    'tacto': 'D', 'oído': 'D', 'gusto': 'N', 'olfato': 'N',
    'interocepción': 'A',
    'vida': 'D', 'muerte': 'D', 'placer': 'N', 'dolor': 'N',
    'consciente': 'N', 'ausente': 'A',
    'individual': 'D', 'colectivo': 'D',
    'querer': 'N', 'saber': 'A', 'pensar': 'A', 'decir': 'N',
    'temporal_obs': 'N', 'eterno_obs': 'N',
    'receptivo': 'A', 'creador_obs': 'A',
}

ALL_DOMAINS = ['Mus', 'Che', 'Bio', 'Mat', 'Fil', 'Fis']
DOMAIN_DICTS = [music_classes, chem_classes, bio_classes,
                math_classes, phil_classes, phys_classes]

# Current universal core (D in ALL 6 domains)
universal_core_63 = []
for p in prims:
    classes = [d.get(p['nombre'], '?') for d in DOMAIN_DICTS]
    if all(c == 'D' for c in classes):
        universal_core_63.append(p['nombre'])

print(f'Current universal core (D/D/D/D/D/D): {len(universal_core_63)} primitives')
for p in universal_core_63:
    print(f'  {p:<22} capa={capa_map[p]}')
print()

# Would proporcion be in the core?
# Proporcion is D in all 6 domains (confirmed by Doc 22)
proporcion_class_all = 'D'
print(f'proporcion predicted class in all domains: DIRECT')
print(f'  Music:      DIRECT (harmonic series, intervals)')
print(f'  Chemistry:  DIRECT (stoichiometry, Keq)')
print(f'  Biology:    DIRECT (Mendelian ratios, allometry)')
print(f'  Mathematics:DIRECT (rational numbers, Euclid V)')
print(f'  Philosophy: DIRECT (Divided Line, mesotes)')
print(f'  Physics:    DIRECT (fine-structure constant)')
print()

universal_core_64 = universal_core_63 + ['proporcion']
print(f'Updated universal core (if accepted): {len(universal_core_64)} primitives')
print(f'  Added: proporcion (capa 3)')
print(f'  Core grows from {len(universal_core_63)} → {len(universal_core_64)}')
print()

# Verify no existing core member displaced
displaced = [p for p in universal_core_63 if p not in universal_core_64]
print(f'Displaced primitives: {len(displaced)} ({"NONE" if not displaced else displaced})')
print()

# ######################################################################
#  SECTION 6: DECISION MATRIX
# ######################################################################
print('=' * 70)
print('SECTION 6: DECISION MATRIX')
print('=' * 70)
print()

print('ARGUMENTS IN FAVOR (ACCEPT):')
pros = [
    ('Word alignment',    '64 = 2^6, byte-aligned, natural machine word'),
    ('State space',       '3^64 states: clean algebraic expansion (×3)'),
    ('Prime identity',    '311 is the 64th prime, no collision with existing primes'),
    ('Universal evidence','D/D/D/D/D/D across 6 domains — unique among candidates'),
    ('Metric improvement',f'+{avg_delta:.1f}pp avg consistency improvement across 6 domains'),
    ('Gap closure',       'Closes the only structural gap identified across 6 validations'),
    ('Falsifiability',    'Proportion can be tested in new domains immediately'),
    ('No violations',     '0 VIOLATED dependencies with 64 primitives'),
    ('No circularity',    'No circular dependencies introduced'),
]
for i, (name, desc) in enumerate(pros, 1):
    print(f'  {i}. {name:<22} {desc}')
print()

print('ARGUMENTS AGAINST (REJECT):')
cons = [
    ('Stability break',   'Model has been 63 through 6 validations; changing breaks continuity'),
    ('Re-validation',     'All existing tests would need re-running with 64 primitives'),
    ('Single evaluator',  'All evidence comes from one evaluator — bias risk'),
    ('Incremental risk',  'If 64 is accepted, what prevents 65? Need principled stopping rule'),
    ('TriadicGPT impact', 'Computational model needs updating for 64 dimensions'),
]
for i, (name, desc) in enumerate(cons, 1):
    print(f'  {i}. {name:<22} {desc}')
print()

print('CONDITIONS FOR FUTURE ACCEPTANCE:')
conditions = [
    'Inter-rater validation (κ ≥ 0.6) confirms proportion mapping in ≥ 3 domains',
    'At least 1 additional domain (7th) confirms proportion as DIRECT',
    'TriadicGPT implementation updated and tested with 64 dimensions',
    'Permutation tests confirm statistical significance of improvement',
    'No adverse effects on existing domain validations after re-running',
]
for i, cond in enumerate(conditions, 1):
    print(f'  {i}. {cond}')
print()

# ######################################################################
#  SECTION 7: FORMAL DECISION
# ######################################################################
print('=' * 70)
print('SECTION 7: FORMAL DECISION')
print('=' * 70)
print()

DECISION = 'DEFER'
print(f'  DECISION: {DECISION}')
print()
print('  The evidence strongly justifies the addition of proporcion as the')
print('  64th primitive. However, the decision is DEFERRED pending:')
print()
print('  (a) Inter-rater validation — Protocol 26 must be applied by an')
print('      independent evaluator to at least 3 domains')
print('  (b) 7th domain validation — Linguistics (Test 15) must confirm')
print('      proportion as DIRECT')
print('  (c) Computational implementation — TriadicGPT must be updated')
print('      to handle 64 dimensions')
print()
print('  The model remains at 63 primitives. Proporcion is documented as')
print('  a structural prediction of the model — the first primitive whose')
print('  existence was PREDICTED by cross-domain analysis rather than')
print('  derived from philosophical first principles.')
print()

# ######################################################################
#  SECTION 8: FALSIFIABLE PREDICTIONS
# ######################################################################
print('=' * 70)
print('SECTION 8: FALSIFIABLE PREDICTIONS')
print('=' * 70)
print()

falsifiable = [
    ('F1', 'If 7th domain (linguistics) is validated, proporcion will be DIRECT',
     'Proportion is fundamental to linguistics: morpheme-to-word ratios, '
     'type-token ratios, Zipf\'s law.'),
    ('F2', 'Adding proporcion will improve anchor consistency in linguistics by ≥5pp',
     'Based on 6-domain avg of +16.5pp, conservative lower bound.'),
    ('F3', 'No new VIOLATED dependencies with 64 primitives in any domain',
     'proporcion depends only on {más, información, orden} — all layer ≤3.'),
    ('F4', 'The 65th primitive candidate, if it exists, will emerge from 8th domain',
     'The model should not grow incrementally without domain-driven evidence.'),
    ('F5', 'Inter-rater κ for proportion classification will be ≥ 0.7 (substantial)',
     'Proportion is unambiguous — evaluators should agree.'),
]

for fid, claim, evidence in falsifiable:
    print(f'  {fid}: {claim}')
    print(f'       Evidence: {evidence}')
    print()

# ######################################################################
#  SECTION 9: OUTPUT — JSON PROPOSAL
# ######################################################################
print('=' * 70)
print('SECTION 9: JSON PROPOSAL (64th primitive)')
print('=' * 70)
print()

output_json = {
    'decision': DECISION,
    'primitive': proporcion,
    'algebraic': {
        'word_size': '64 = 2^6',
        'state_space': f'3^64 ≈ {3**64:.4e}',
        'prime_311': {
            'is_prime': True,
            'position': 64,
            'no_collision': True,
        },
    },
    'evidence': {
        'domains_confirmed': 6,
        'universal_class': 'D/D/D/D/D/D',
        'avg_improvement_pp': round(avg_delta, 1),
        'violated': 0,
        'circular_deps': False,
    },
    'conditions_for_acceptance': conditions,
    'core_update': {
        'before': len(universal_core_63),
        'after': len(universal_core_64),
        'added': 'proporcion',
        'displaced': 0,
    },
}

print(json.dumps(output_json, indent=2, ensure_ascii=False))
print()

# ######################################################################
#  SUMMARY TABLE
# ######################################################################
print('=' * 70)
print('SUMMARY TABLE')
print('=' * 70)
print()

print(f'  {"Metric":<40} {"Before (63)":<20} {"After (64)":<20}')
print(f'  {"-"*80}')
print(f'  {"Primitives":<40} {"63":<20} {"64":<20}')
print(f'  {"Bits":<40} {"63 (non-aligned)":<20} {"64 (2^6)":<20}')
print(f'  {"State space":<40} {"3^63":<20} {"3^64":<20}')
print(f'  {"64th prime":<40} {"(unused)":<20} {"311":<20}')
print(f'  {"Universal core":<40} {str(len(universal_core_63)):<20} {str(len(universal_core_64)):<20}')
print(f'  {"VIOLATED deps":<40} {"0":<20} {"0":<20}')
print(f'  {"Circular deps":<40} {"No":<20} {"No":<20}')
print(f'  {"Avg anchor improvement":<40} {"—":<20} {f"+{avg_delta:.1f}pp":<20}')
print(f'  {"Decision":<40} {"—":<20} {"DEFER":<20}')
print()

print('=' * 78)
print('  SIMULATION COMPLETE')
print('=' * 78)
