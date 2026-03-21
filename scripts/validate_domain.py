"""Automatic domain validator for the 7x7 System — IDVS metric.

Usage:
    python validate_domain.py <input.json>       Validate a domain classification
    python validate_domain.py --template [out]   Generate blank template

Input format (flat JSON):
    { "domain": "Economics", "classes": { "vacío": "D", ... } }

Classification key:
    D = Direct    — the primitive operates directly in the domain
    A = Analogical — the primitive applies by metaphor/analogy
    N = Null       — the primitive does not apply at all
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import math
import os

# ######################################################################
#  SECTION 0: CLI PARSING
# ######################################################################

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.normpath(os.path.join(script_dir, '..', 'data'))

if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
    print(__doc__)
    sys.exit(0)

template_mode = sys.argv[1] == '--template'
input_file = None if template_mode else sys.argv[1]

# ######################################################################
#  SECTION 1: DATA LOADING
# ######################################################################

with open(os.path.join(data_dir, 'primitivos.json'), 'r', encoding='utf-8') as f:
    prim_data = json.load(f)

prims = prim_data['primitivos']
names = [p['nombre'] for p in prims]
dep_pairs = []
for p in prims:
    for d in p['deps']:
        dep_pairs.append((p['nombre'], d))
capa_map = {p['nombre']: p['capa'] for p in prims}
prime_map = {p['nombre']: p['primo'] for p in prims}
def_map = {p['nombre']: p['def'] for p in prims}
total_L14 = sum(1 for p in prims if p['capa'] <= 4)

with open(os.path.join(data_dir, 'reference_domains.json'), 'r', encoding='utf-8') as f:
    ref_data = json.load(f)

ref_domains = ref_data['domains']
ref_idvs = ref_data['reference_idvs']

# ######################################################################
#  SECTION 2: TEMPLATE GENERATION
# ######################################################################

if template_mode:
    template = {
        "domain": "YOUR_DOMAIN_NAME",
        "classes": {},
        "_guide": {}
    }
    for p in sorted(prims, key=lambda x: (x['capa'], x['bit'])):
        template["classes"][p['nombre']] = "?"
        template["_guide"][p['nombre']] = {
            "capa": p['capa'],
            "def": p['def'],
            "deps": p['deps']
        }

    output = json.dumps(template, indent=2, ensure_ascii=False)
    if len(sys.argv) > 2:
        with open(sys.argv[2], 'w', encoding='utf-8') as f:
            f.write(output + '\n')
        print(f'Template written to {sys.argv[2]}')
    else:
        print(output)

    print(file=sys.stderr)
    print('# Classification guide:', file=sys.stderr)
    print('#   D = Direct: the primitive operates directly in the domain', file=sys.stderr)
    print('#   A = Analogical: the primitive applies by metaphor/analogy', file=sys.stderr)
    print('#   N = Null: the primitive does not apply at all', file=sys.stderr)
    print(f'# Total primitives: {len(prims)}', file=sys.stderr)
    print(f'# Foundational (layers 1-4): {total_L14}', file=sys.stderr)
    print('# Replace every "?" with D, A, or N, then run:', file=sys.stderr)
    print('#   python validate_domain.py your_domain.json', file=sys.stderr)
    sys.exit(0)

# ######################################################################
#  SECTION 3: INPUT VALIDATION
# ######################################################################

with open(input_file, 'r', encoding='utf-8') as f:
    user_data = json.load(f)

domain_name = user_data.get('domain', 'Unknown')
user_classes = user_data.get('classes', {})

expected = set(names)
provided = set(user_classes.keys())
missing = expected - provided
extra = provided - expected

errors = []
if missing:
    errors.append(f'Missing {len(missing)} primitives: {", ".join(sorted(missing))}')
if extra:
    errors.append(f'Unknown {len(extra)} primitives: {", ".join(sorted(extra))}')

invalid_vals = {k: v for k, v in user_classes.items()
                if v not in ('D', 'A', 'N')}
if invalid_vals:
    errors.append(f'Invalid values (must be D, A, or N): {invalid_vals}')

if errors:
    print('ERROR: Invalid input')
    for e in errors:
        print(f'  • {e}')
    sys.exit(1)

# ######################################################################
#  SECTION 4: UTILITY FUNCTIONS
# ######################################################################

STATE_MAP = {'D': 2, 'A': 1, 'N': 0}


def safe_log2(x):
    return math.log2(x) if x > 0 else 0.0


def build_ternary_vector(cd, order):
    return [STATE_MAP[cd[n]] for n in order]


def hamming_distance(v1, v2):
    return sum(1 for a, b in zip(v1, v2) if a != b)


def weighted_hamming(v1, v2):
    return sum(abs(a - b) for a, b in zip(v1, v2))


def jacobi_eigen(A, tol=1e-10, max_iter=500):
    """Jacobi eigenvalue algorithm for symmetric matrix."""
    n = len(A)
    M = [row[:] for row in A]
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(max_iter):
        max_val = 0.0
        p, q = 0, 1
        for i in range(n):
            for j in range(i + 1, n):
                if abs(M[i][j]) > max_val:
                    max_val = abs(M[i][j])
                    p, q = i, j
        if max_val < tol:
            break
        if abs(M[p][p] - M[q][q]) < 1e-15:
            theta = math.pi / 4
        else:
            theta = 0.5 * math.atan2(2.0 * M[p][q], M[p][p] - M[q][q])
        c = math.cos(theta)
        s = math.sin(theta)
        for i in range(n):
            if i != p and i != q:
                mip = M[i][p]
                miq = M[i][q]
                M[i][p] = c * mip + s * miq
                M[p][i] = M[i][p]
                M[i][q] = -s * mip + c * miq
                M[q][i] = M[i][q]
        mpp, mqq, mpq = M[p][p], M[q][q], M[p][q]
        M[p][p] = c * c * mpp + 2 * s * c * mpq + s * s * mqq
        M[q][q] = s * s * mpp - 2 * s * c * mpq + c * c * mqq
        M[p][q] = 0.0
        M[q][p] = 0.0
        for i in range(n):
            vip = V[i][p]
            viq = V[i][q]
            V[i][p] = c * vip + s * viq
            V[i][q] = -s * vip + c * viq
    return [M[i][i] for i in range(n)], V


# ######################################################################
#  SECTION 5: REPORT HEADER + DISTRIBUTION
# ######################################################################

print('=' * 78)
print(f'  DOMAIN VALIDATION REPORT: {domain_name}')
print('=' * 78)
print()

print('  INPUT VALIDATION')
print(f'  \u2713 {len(user_classes)} primitives classified')
print(f'  \u2713 All values are D, A, or N')

n_D = sum(1 for v in user_classes.values() if v == 'D')
n_A = sum(1 for v in user_classes.values() if v == 'A')
n_N = sum(1 for v in user_classes.values() if v == 'N')
print(f'  Distribution: {n_D} D, {n_A} A, {n_N} N')
print()

print(f'  {"Layer":<10} {"D":>4} {"A":>4} {"N":>4} {"Total":>6}')
print(f'  {"-" * 30}')
for capa in range(1, 7):
    layer_prims = [p for p in prims if p['capa'] == capa]
    ld = sum(1 for p in layer_prims if user_classes[p['nombre']] == 'D')
    la = sum(1 for p in layer_prims if user_classes[p['nombre']] == 'A')
    ln = sum(1 for p in layer_prims if user_classes[p['nombre']] == 'N')
    print(f'  L{capa:<9} {ld:>4} {la:>4} {ln:>4} {len(layer_prims):>6}')
print()

# ######################################################################
#  SECTION 6: COVERAGE L1-4
# ######################################################################

print('  COVERAGE L1-4')
nulls_L14 = []
for p in prims:
    if p['capa'] <= 4 and user_classes[p['nombre']] == 'N':
        nulls_L14.append(p)

coverage = 1.0 - len(nulls_L14) / total_L14
print(f'  Coverage = {coverage:.3f}  ({len(nulls_L14)} NULLs in layers 1-4)')

if nulls_L14:
    print(f'  NULLs in foundational layers:')
    for p in nulls_L14:
        print(f'    L{p["capa"]}: {p["nombre"]} \u2014 {p["def"]}')
print()

# ######################################################################
#  SECTION 7: MONOTONICITY
# ######################################################################

print('  MONOTONICITY')
monotone_count = 0
violations = []

for child, parent in dep_pairs:
    c_state = STATE_MAP[user_classes[child]]
    p_state = STATE_MAP[user_classes[parent]]
    if c_state <= p_state:
        monotone_count += 1
    else:
        violations.append((child, parent, user_classes[child], user_classes[parent]))

mono = monotone_count / len(dep_pairs)
print(f'  Monotonicity = {mono:.3f}  ({monotone_count}/{len(dep_pairs)} monotone, '
      f'{len(violations)} violations)')

if violations:
    print(f'  Violations:')
    vtypes = {}
    for child, parent, cs, ps in violations:
        vtype = f'{cs}\u2190{ps}'
        vtypes.setdefault(vtype, []).append((child, parent, cs, ps))
    for vtype in sorted(vtypes.keys()):
        for child, parent, cs, ps in vtypes[vtype]:
            print(f'    {child}(L{capa_map[child]},{cs}) \u2190 '
                  f'{parent}(L{capa_map[parent]},{ps})')
print()

# ######################################################################
#  SECTION 8: IDVS + VERDICT
# ######################################################################

idvs = coverage * mono

print('  ' + '\u2550' * 52)
print(f'    IDVS = {coverage:.3f} \u00d7 {mono:.3f} = {idvs:.3f}')

if idvs >= 0.90:
    verdict = 'PASS'
    symbol = '\u2713'
    desc = 'Above p95 of null distribution (threshold calibrated by I2 permutation test)'
elif idvs >= 0.50:
    verdict = 'UNCERTAIN'
    symbol = '?'
    desc = 'Between valid and invalid zones'
else:
    verdict = 'FAIL'
    symbol = '\u2717'
    desc = 'Consistent with pseudo-science'

print(f'    VERDICT: {symbol} {verdict} \u2014 {desc}')
print('  ' + '\u2550' * 52)
print()

# ######################################################################
#  SECTION 9: PRIME SIGNATURE
# ######################################################################

print('  PRIME SIGNATURE')
sigma = 1
for p in prims:
    state = STATE_MAP[user_classes[p['nombre']]]
    sigma *= p['primo'] ** state

log2_sigma = math.log2(sigma) if sigma > 0 else 0
print(f'  log\u2082(\u03a3) = {log2_sigma:.2f} bits')

unique = True
match_name = None
for dname, dinfo in ref_domains.items():
    ref_sigma = 1
    for p in prims:
        state = STATE_MAP[dinfo['classes'][p['nombre']]]
        ref_sigma *= p['primo'] ** state
    if ref_sigma == sigma:
        print(f'  \u26a0 IDENTICAL signature to {dname}!')
        unique = False
        match_name = dname
        break

if unique:
    print(f'  Status: UNIQUE')
print()

# ######################################################################
#  SECTION 10: HAMMING COMPARISON
# ######################################################################

print('  COMPARISON WITH REFERENCE DOMAINS')
user_vec = build_ternary_vector(user_classes, names)

comparisons = []
for dname, dinfo in ref_domains.items():
    ref_vec = build_ternary_vector(dinfo['classes'], names)
    h = hamming_distance(user_vec, ref_vec)
    w = weighted_hamming(user_vec, ref_vec)
    ref_score = ref_idvs[dname]
    comparisons.append((dname, ref_score, h, w))

comparisons.sort(key=lambda x: -x[1])

print(f'  {"Domain":<16} {"IDVS":>6} {"Hamming":>8} {"Weighted":>9}')
print(f'  {"-" * 41}')

inserted = False
for dname, ref_score, h, w in comparisons:
    if not inserted and idvs >= ref_score:
        print(f'  \u2192 {domain_name:<13} {idvs:>6.3f} {"\u2014":>8} {"\u2014":>9}')
        inserted = True
    print(f'    {dname:<14} {ref_score:>6.3f} {h:>8} {w:>9}')
if not inserted:
    print(f'  \u2192 {domain_name:<13} {idvs:>6.3f} {"\u2014":>8} {"\u2014":>9}')

by_hamming = sorted(comparisons, key=lambda x: x[2])
print(f'\n  Nearest: {by_hamming[0][0]} (Hamming={by_hamming[0][2]})')
print(f'  Farthest: {by_hamming[-1][0]} (Hamming={by_hamming[-1][2]})')
print()

# ######################################################################
#  SECTION 11: MDS 2D
# ######################################################################

print('  MDS 2D COORDINATES')

all_names_mds = list(ref_domains.keys()) + [domain_name]
all_vecs = []
for dname in list(ref_domains.keys()):
    all_vecs.append(build_ternary_vector(ref_domains[dname]['classes'], names))
all_vecs.append(user_vec)

n_mds = len(all_names_mds)

D_mat = [[0] * n_mds for _ in range(n_mds)]
for i in range(n_mds):
    for j in range(n_mds):
        D_mat[i][j] = hamming_distance(all_vecs[i], all_vecs[j])

D2 = [[D_mat[i][j] ** 2 for j in range(n_mds)] for i in range(n_mds)]
row_means = [sum(D2[i]) / n_mds for i in range(n_mds)]
col_means = [sum(D2[i][j] for i in range(n_mds)) / n_mds for j in range(n_mds)]
grand_mean = sum(sum(r) for r in D2) / (n_mds * n_mds)

B = [[-0.5 * (D2[i][j] - row_means[i] - col_means[j] + grand_mean)
      for j in range(n_mds)] for i in range(n_mds)]

eigenvalues, eigenvectors = jacobi_eigen(B)

idx = sorted(range(n_mds), key=lambda k: -eigenvalues[k])
e1, e2 = eigenvalues[idx[0]], eigenvalues[idx[1]]
total_var = sum(max(0, ev) for ev in eigenvalues)
var_explained = (max(0, e1) + max(0, e2)) / total_var if total_var > 0 else 0

coords = []
for i in range(n_mds):
    x = eigenvectors[i][idx[0]] * math.sqrt(max(0, e1))
    y = eigenvectors[i][idx[1]] * math.sqrt(max(0, e2))
    coords.append((x, y))

print(f'  Variance explained (2D): {var_explained:.1%}')
print(f'  {"Domain":<18} {"x":>8} {"y":>8}')
print(f'  {"-" * 36}')
for i, dname in enumerate(all_names_mds):
    marker = '\u2192 ' if dname == domain_name else '  '
    print(f'  {marker}{dname:<16} {coords[i][0]:>8.3f} {coords[i][1]:>8.3f}')

new_idx = n_mds - 1
min_dist_2d = float('inf')
nearest_2d = ''
for i in range(n_mds - 1):
    dx = coords[new_idx][0] - coords[i][0]
    dy = coords[new_idx][1] - coords[i][1]
    d = math.sqrt(dx * dx + dy * dy)
    if d < min_dist_2d:
        min_dist_2d = d
        nearest_2d = all_names_mds[i]

print(f'\n  Nearest in 2D: {nearest_2d} (dist={min_dist_2d:.3f})')
print()

# ######################################################################
#  SECTION 12: SUMMARY
# ######################################################################

print('=' * 78)
print('  SUMMARY')
print('=' * 78)
print()

print(f'  {"Metric":<24} {"Value":>10}')
print(f'  {"-" * 36}')
print(f'  {"Coverage L1-4":<24} {coverage:>10.3f}')
print(f'  {"Monotonicity":<24} {mono:>10.3f}')
print(f'  {"IDVS":<24} {idvs:>10.3f}')
print(f'  {"NULLs in L1-4":<24} {len(nulls_L14):>10}')
print(f'  {"Violations":<24} {len(violations):>10}')
print(f'  {"Nearest domain":<24} {by_hamming[0][0]:>10}')
print(f'  {"Prime signature":<24} {"UNIQUE" if unique else "= " + str(match_name):>10}')
print()

print(f'  VERDICT: {symbol} {verdict}')
print()

if verdict == 'UNCERTAIN':
    print('  Suggestions:')
    if nulls_L14:
        print('  \u2022 Review NULLs in layers 1-4 \u2014 foundational primitives '
              'should rarely be NULL')
    if len(violations) > 5:
        print('  \u2022 Many monotonicity violations \u2014 check if child '
              'classifications exceed parent states')
    print('  \u2022 Compare with nearest valid domain for guidance')
    print()
elif verdict == 'FAIL':
    print('  Suggestions:')
    if len(nulls_L14) > 5:
        print('  \u2022 Too many NULLs in foundational layers \u2014 genuine '
              'domains engage with basic primitives')
    if mono < 0.85:
        print('  \u2022 Low monotonicity \u2014 classifications do not respect '
              'the dependency hierarchy')
    print('  \u2022 This pattern is consistent with analogical/metaphorical '
          'domains rather than genuine ones')
    print()
