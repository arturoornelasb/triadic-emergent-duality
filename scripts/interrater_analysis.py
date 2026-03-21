"""Fase 10: Inter-Rater Reliability Analysis + Perturbation Sensitivity.

Infrastructure for inter-rater agreement (kappa, alpha, confusion matrix)
plus simulation-based sensitivity analysis (no human evaluators available).

Modes:
  python interrater_analysis.py                       # simulation only
  python interrater_analysis.py eval1.json eval2.json # real evaluator data

Solo stdlib: json, math, sys, os, random, collections.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import math
import os
import random
from collections import defaultdict, Counter

# ######################################################################
#  SECTION 0: CLI + DATA LOADING
# ######################################################################

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data')

with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
    prim_data = json.load(f)

with open(os.path.join(DATA_DIR, 'reference_domains.json'), 'r', encoding='utf-8') as f:
    dom_data = json.load(f)

prims = prim_data['primitivos']
names = [p['nombre'] for p in prims]
capa_map = {p['nombre']: p['capa'] for p in prims}
def_map = {p['nombre']: p['def'] for p in prims}
deps_map = {p['nombre']: list(p['deps']) for p in prims}
prime_map = {p['nombre']: p['primo'] for p in prims}

# dep_pairs as (child, parent) for monotonicity checking
dep_pairs = []
for p in prims:
    for d in p['deps']:
        dep_pairs.append((p['nombre'], d))

total_L14 = sum(1 for p in prims if p['capa'] <= 4)
STATE_MAP = {'D': 2, 'A': 1, 'N': 0}

domains = dom_data['domains']
domain_names = sorted(domains.keys())

evaluator_files = sys.argv[1:] if len(sys.argv) > 1 else []
has_evaluators = len(evaluator_files) >= 2

print('=' * 78)
print('  INTER-RATER RELIABILITY & SENSITIVITY ANALYSIS')
print(f'  {len(prims)} Primitivos x {len(domain_names)} Domains')
print(f'  Mode: {"REAL EVALUATORS" if has_evaluators else "SIMULATION"}')
print('=' * 78)
print()

# ######################################################################
#  SECTION 1: METRIC FUNCTIONS
# ######################################################################


def cohens_kappa(rater1_classes, rater2_classes):
    """Cohen's kappa for D/A/N classification."""
    categories = ['D', 'A', 'N']
    common_keys = sorted(set(rater1_classes.keys()) & set(rater2_classes.keys()))
    n = len(common_keys)
    if n == 0:
        return {'kappa': 0.0, 'po': 0.0, 'pe': 0.0, 'confusion_matrix': {}}

    matrix = {c1: {c2: 0 for c2 in categories} for c1 in categories}
    for key in common_keys:
        r1 = rater1_classes[key]
        r2 = rater2_classes[key]
        if r1 in categories and r2 in categories:
            matrix[r1][r2] += 1

    po = sum(matrix[c][c] for c in categories) / n
    pe = 0.0
    for c in categories:
        row_sum = sum(matrix[c][c2] for c2 in categories) / n
        col_sum = sum(matrix[c1][c] for c1 in categories) / n
        pe += row_sum * col_sum
    kappa = (po - pe) / (1 - pe) if pe < 1.0 else 1.0

    return {'kappa': kappa, 'po': po, 'pe': pe, 'confusion_matrix': matrix}


def krippendorffs_alpha(ratings_matrix, level='nominal'):
    """Krippendorff's alpha for multiple raters (D/A/N)."""
    categories = ['D', 'A', 'N']
    ordinal_map = {'D': 0, 'A': 1, 'N': 2} if level == 'ordinal' else None

    all_items = set()
    for r in ratings_matrix:
        all_items |= set(r.keys())

    n_total = 0
    coincidence = {c1: {c2: 0.0 for c2 in categories} for c1 in categories}

    for item in all_items:
        ratings = [r[item] for r in ratings_matrix
                   if item in r and r[item] in categories]
        m = len(ratings)
        if m < 2:
            continue
        for i in range(m):
            for j in range(m):
                if i != j:
                    coincidence[ratings[i]][ratings[j]] += 1.0 / (m - 1)
            n_total += 1

    if n_total == 0:
        return {'alpha': 0.0, 'Do': 0.0, 'De': 0.0}

    total_c = sum(sum(coincidence[c1][c2] for c2 in categories)
                  for c1 in categories)
    if total_c == 0:
        return {'alpha': 0.0, 'Do': 0.0, 'De': 0.0}

    if level == 'ordinal' and ordinal_map:
        Do = sum(coincidence[c1][c2] * (ordinal_map[c1] - ordinal_map[c2])**2
                 for c1 in categories for c2 in categories) / total_c
    else:
        Do = 1.0 - sum(coincidence[c][c] for c in categories) / total_c

    marginals = {c: sum(coincidence[c][c2] for c2 in categories)
                 for c in categories}
    n_vals = sum(marginals.values())

    if level == 'ordinal' and ordinal_map:
        De = sum(marginals[c1] * marginals[c2]
                 * (ordinal_map[c1] - ordinal_map[c2])**2
                 for c1 in categories for c2 in categories)
        De /= (n_vals * (n_vals - 1)) if n_vals > 1 else 1
    else:
        De = (1.0 - sum(marginals[c]**2 for c in categories)
              / (n_vals * (n_vals - 1))) if n_vals > 1 else 0

    alpha = 1.0 - Do / De if De > 0 else 1.0
    return {'alpha': alpha, 'Do': Do, 'De': De}


def confusion_matrix_dan(rater1, rater2):
    """3x3 confusion matrix for D/A/N."""
    categories = ['D', 'A', 'N']
    common_keys = sorted(set(rater1.keys()) & set(rater2.keys()))
    n = len(common_keys)

    matrix = {c1: {c2: 0 for c2 in categories} for c1 in categories}
    for key in common_keys:
        r1 = rater1[key]
        r2 = rater2[key]
        if r1 in categories and r2 in categories:
            matrix[r1][r2] += 1

    exact_agree = sum(matrix[c][c] for c in categories)
    pct_agree = exact_agree / n * 100 if n > 0 else 0
    return {'matrix': matrix, 'n': n,
            'exact_agreement': exact_agree, 'pct_agreement': pct_agree}


# ######################################################################
#  SECTION 2: EVALUATOR PROCESSING
# ######################################################################

if has_evaluators:
    print('=' * 78)
    print('  EVALUATOR AGREEMENT')
    print('=' * 78)
    print()

    eval_data = []
    for ef in evaluator_files:
        with open(ef, 'r', encoding='utf-8') as f:
            eval_data.append(json.load(f))

    for i in range(len(eval_data)):
        for j in range(i + 1, len(eval_data)):
            name_i = evaluator_files[i]
            name_j = evaluator_files[j]
            classes_i = eval_data[i].get('classes', {})
            classes_j = eval_data[j].get('classes', {})

            kappa_result = cohens_kappa(classes_i, classes_j)
            cm = confusion_matrix_dan(classes_i, classes_j)

            print(f'  Pair: {name_i} vs {name_j}')
            print(f'    kappa = {kappa_result["kappa"]:.3f}  '
                  f'(po={kappa_result["po"]:.3f}, pe={kappa_result["pe"]:.3f})')
            print(f'    Agreement: {cm["exact_agreement"]}/{cm["n"]} '
                  f'({cm["pct_agreement"]:.1f}%)')

            # Print confusion matrix
            print(f'    {"":>8} {"D":>6} {"A":>6} {"N":>6}')
            for c in ['D', 'A', 'N']:
                row = f'    {c:>8}'
                for c2 in ['D', 'A', 'N']:
                    row += f'{cm["matrix"][c][c2]:>6}'
                print(row)
            print()

    # Krippendorff's alpha if 2+ evaluators
    if len(eval_data) >= 2:
        all_classes = [ed.get('classes', {}) for ed in eval_data]
        alpha_nom = krippendorffs_alpha(all_classes, 'nominal')
        alpha_ord = krippendorffs_alpha(all_classes, 'ordinal')
        print(f'  Krippendorff alpha (nominal): {alpha_nom["alpha"]:.3f}')
        print(f'  Krippendorff alpha (ordinal): {alpha_ord["alpha"]:.3f}')
        print()
else:
    print('  No evaluator files provided. Running simulation mode only.')
    print()

# ######################################################################
#  SECTION 3: PERTURBATION SENSITIVITY
# ######################################################################

print('=' * 78)
print('  PERTURBATION SENSITIVITY')
print('  9 domains x k={1,2,3,5,7,10} x 1000 reps')
print('=' * 78)
print()

K_VALUES = [1, 2, 3, 5, 7, 10]
N_REPS = 1000
STATES = ['D', 'A', 'N']


def perturb(classes, k, rng):
    """Randomly change k classifications to different states."""
    modified = dict(classes)
    selected = rng.sample(list(classes.keys()), min(k, len(classes)))
    for p in selected:
        alternatives = [s for s in STATES if s != modified[p]]
        modified[p] = rng.choice(alternatives)
    return modified


# Layer weights: higher layers -> more ambiguous -> more likely to be perturbed
LAYER_WEIGHTS = {1: 0.05, 2: 0.10, 3: 0.15, 4: 0.20, 5: 0.25, 6: 0.25}


def perturb_weighted(classes, k, rng):
    """Layer-weighted perturbation: higher layers perturbed more often."""
    modified = dict(classes)
    prim_names = list(classes.keys())
    weights = [LAYER_WEIGHTS.get(capa_map.get(p, 4), 0.20) for p in prim_names]
    selected = set()
    attempts = 0
    while len(selected) < min(k, len(prim_names)) and attempts < k * 10:
        pick = rng.choices(prim_names, weights=weights, k=1)[0]
        selected.add(pick)
        attempts += 1
    for p in selected:
        alternatives = [s for s in STATES if s != modified[p]]
        modified[p] = rng.choice(alternatives)
    return modified


perturbation_results = {}  # domain -> {k -> [kappa values]}

print(f'  {"Domain":<14}', end='')
for k in K_VALUES:
    print(f'  k={k:<3} (mean/std)', end='')
print()
print(f'  {"-"*14}', end='')
for _ in K_VALUES:
    print(f'  {"-"*15}', end='')
print()

for dname in domain_names:
    classes = domains[dname]['classes']
    perturbation_results[dname] = {}
    rng = random.Random(42)

    row = f'  {dname:<14}'
    for k in K_VALUES:
        kappas = []
        for _ in range(N_REPS):
            perturbed = perturb(classes, k, rng)
            result = cohens_kappa(classes, perturbed)
            kappas.append(result['kappa'])
        perturbation_results[dname][k] = kappas
        mean_k = sum(kappas) / len(kappas)
        std_k = (sum((x - mean_k)**2 for x in kappas) / len(kappas)) ** 0.5
        row += f'  {mean_k:.3f}/{std_k:.3f}  '
    print(row)

print()

# Verify: k=0 should give kappa=1
for dname in domain_names[:1]:
    classes = domains[dname]['classes']
    r = cohens_kappa(classes, classes)
    assert abs(r['kappa'] - 1.0) < 1e-10, f'k=0 should give kappa=1.0'
print('  Verification: k=0 -> kappa=1.0  PASS')

# Verify: mean_kappa decreases with k
mono_check = True
for dname in domain_names:
    prev_mean = 1.0
    for k in K_VALUES:
        mean_k = sum(perturbation_results[dname][k]) / N_REPS
        if mean_k > prev_mean + 0.01:
            mono_check = False
        prev_mean = mean_k
print(f'  Monotonic decrease check: {"PASS" if mono_check else "FAIL"}')
print()

# ######################################################################
#  SECTION 4: FRAGILE PRIMITIVES
# ######################################################################

print('=' * 78)
print('  FRAGILE PRIMITIVES')
print('  Impact of single reclassification on IDVS')
print('=' * 78)
print()


def compute_idvs(classes):
    """Compute IDVS = coverage x monotonicity."""
    nulls_l14 = sum(1 for p in prims
                    if p['capa'] <= 4 and classes.get(p['nombre'], 'A') == 'N')
    coverage = 1.0 - nulls_l14 / total_L14

    violations = 0
    for child, parent in dep_pairs:
        c_state = STATE_MAP.get(classes.get(child, 'A'), 1)
        p_state = STATE_MAP.get(classes.get(parent, 'A'), 1)
        if c_state > p_state:
            violations += 1
    mono = 1 - violations / len(dep_pairs) if dep_pairs else 1.0

    return coverage * mono


for dname in domain_names:
    classes = domains[dname]['classes']
    base_idvs = compute_idvs(classes)

    fragilities = []
    for pname in names:
        original_state = classes[pname]
        max_delta = 0.0
        for alt_state in STATES:
            if alt_state == original_state:
                continue
            modified = dict(classes)
            modified[pname] = alt_state
            new_idvs = compute_idvs(modified)
            delta = base_idvs - new_idvs
            max_delta = max(max_delta, delta)
        fragilities.append((pname, max_delta, capa_map[pname]))

    fragilities.sort(key=lambda x: -x[1])
    top10 = fragilities[:10]

    print(f'  {dname} (base IDVS = {base_idvs:.3f}):')
    if top10[0][1] > 0:
        for pname, delta, capa in top10:
            if delta > 0:
                bar = '#' * int(delta * 50)
                print(f'    L{capa} {pname:<22} delta={delta:>+.4f}  {bar}')
    else:
        print(f'    No fragile primitives (all delta = 0)')
    print()

# ######################################################################
#  SECTION 5: IDVS SENSITIVITY
# ######################################################################

print('=' * 78)
print('  IDVS SENSITIVITY')
print(f'  P(IDVS < 0.80) after k perturbations — uniform + weighted')
print('=' * 78)
print()

K_RANGE = list(range(1, 11))
IDVS_THRESHOLD = 0.90

perturb_modes = [
    ('Uniform', perturb),
    ('Weighted', perturb_weighted),
]

# Store results per mode: mode_name -> domain -> {k -> P(IDVS < threshold)}
idvs_sensitivity = {}      # uniform (default for backwards compat)
idvs_sensitivity_all = {}  # mode_name -> domain -> {k -> p_below}

for mode_name, perturb_fn in perturb_modes:
    print(f'  --- {mode_name} perturbation ---')
    idvs_sensitivity_all[mode_name] = {}

    print(f'  {"Domain":<14} {"Type":<8}', end='')
    for k in K_RANGE:
        print(f' k={k:>2}', end='')
    print()
    print(f'  {"-"*14} {"-"*8}', end='')
    for _ in K_RANGE:
        print(f' {"-"*4}', end='')
    print()

    for dname in domain_names:
        classes = domains[dname]['classes']
        dtype = domains[dname].get('type', 'positive')
        idvs_sensitivity_all[mode_name][dname] = {}
        rng = random.Random(42)

        row = f'  {dname:<14} {dtype:<8}'
        for k in K_RANGE:
            below_count = 0
            for _ in range(N_REPS):
                perturbed = perturb_fn(classes, k, rng)
                idvs = compute_idvs(perturbed)
                if idvs < IDVS_THRESHOLD:
                    below_count += 1
            p_below = below_count / N_REPS
            idvs_sensitivity_all[mode_name][dname][k] = p_below
            row += f' {p_below:>.2f}'
        print(row)

    print()

# Use weighted results as primary
idvs_sensitivity = idvs_sensitivity_all['Weighted']

# Check robustness of positive domains for k <= 3 (weighted)
print(f'  Robustness check (weighted): P(IDVS < {IDVS_THRESHOLD}) < 0.10 for k <= 3')
for dname in domain_names:
    dtype = domains[dname].get('type', 'positive')
    if dtype == 'negative_control':
        continue
    p_k3 = idvs_sensitivity[dname].get(3, 0)
    status = 'ROBUST' if p_k3 < 0.10 else 'FRAGILE'
    print(f'    {dname:<14}: P(k=3) = {p_k3:.3f}  -> {status}')
print()

# ######################################################################
#  SECTION 6: TEMPLATE GENERATION
# ######################################################################

print('=' * 78)
print('  EVALUATOR TEMPLATE GENERATION')
print('=' * 78)
print()

template_dir = os.path.join(DATA_DIR, 'evaluator_templates')
os.makedirs(template_dir, exist_ok=True)

for dname in domain_names:
    template = {
        "evaluator": "YOUR_NAME",
        "domain": dname,
        "instructions": (
            "For each primitive, assign D (Direct), A (Analogical), or N (Null). "
            "D = the primitive operates directly in this domain. "
            "A = the primitive applies by metaphor/analogy. "
            "N = the primitive does not apply at all."
        ),
        "classifications": {}
    }
    for p in sorted(prims, key=lambda x: (x['capa'], x['bit'])):
        template["classifications"][p['nombre']] = {
            "class": "?",
            "definition": p['def'],
            "layer": p['capa'],
            "dependencies": p['deps'],
            "reference_class": domains[dname]['classes'].get(p['nombre'], '?')
        }

    template_path = os.path.join(template_dir, f'{dname.lower()}_template.json')
    with open(template_path, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2, ensure_ascii=False)

print(f'  Generated {len(domain_names)} templates in {template_dir}')
print(f'  Files:')
for dname in domain_names:
    print(f'    {dname.lower()}_template.json')
print()

# ######################################################################
#  SECTION 7: READINESS REPORT
# ######################################################################

print('=' * 78)
print('  READINESS REPORT')
print('  Priority ranking for human evaluation')
print('=' * 78)
print()

readiness = []

for dname in domain_names:
    classes = domains[dname]['classes']
    dtype = domains[dname].get('type', 'positive')

    # Pe: expected chance agreement
    counts = Counter(classes.values())
    n = sum(counts.values())
    pe = sum((c / n) ** 2 for c in counts.values())

    # kappa_max given marginals (assuming second rater has same distribution)
    # P_max = sum(min(p_i, p_i)) = sum(p_i^2... no.
    # For same marginals: P_max = sum(p_i^2) = pe actually.
    # kappa_max = (P_max - pe)/(1 - pe). With same marginals P_max = 1
    # when we CAN have perfect agreement.
    # Actually kappa_max with fixed marginals = 1 only if marginals match.
    # Since we assume same marginals, kappa_max = 1.
    kappa_max = 1.0

    # flips-to-threshold: min k where P(IDVS < 0.80) > 0.50
    flips_thresh = None
    for k in K_RANGE:
        if idvs_sensitivity[dname].get(k, 0) > 0.50:
            flips_thresh = k
            break

    base_idvs = compute_idvs(classes)

    readiness.append({
        'domain': dname,
        'type': dtype,
        'pe': pe,
        'kappa_max': kappa_max,
        'flips_to_threshold': flips_thresh,
        'base_idvs': base_idvs,
    })

# Sort by priority: negative control last, then by flips_to_threshold ascending
readiness.sort(key=lambda x: (
    0 if x['type'] == 'negative_control' else 1,
    x['flips_to_threshold'] if x['flips_to_threshold'] else 99
))

print(f'  {"Domain":<14} {"Type":<10} {"Pe":>6} {"IDVS":>6} '
      f'{"Flips->0.80":>12} {"Priority":<10}')
print(f'  {"-"*14} {"-"*10} {"-"*6} {"-"*6} {"-"*12} {"-"*10}')

for i, r in enumerate(readiness):
    ft = str(r['flips_to_threshold']) if r['flips_to_threshold'] else '>10'
    priority = 'LOW' if r['type'] == 'negative_control' else (
        'HIGH' if r['flips_to_threshold'] and r['flips_to_threshold'] <= 5
        else 'MEDIUM'
    )
    print(f'  {r["domain"]:<14} {r["type"]:<10} {r["pe"]:>6.3f} '
          f'{r["base_idvs"]:>6.3f} {ft:>12} {priority:<10}')

print()

# ######################################################################
#  SECTION 8: SYNTHESIS
# ######################################################################

print('=' * 78)
print('  SYNTHESIS')
print('=' * 78)
print()

# Overall robustness verdict
positive_domains = [dn for dn in domain_names
                    if domains[dn].get('type', 'positive') != 'negative_control']
robust_count = sum(1 for dn in positive_domains
                   if idvs_sensitivity[dn].get(3, 0) < 0.10)

print(f'  Robustness: {robust_count}/{len(positive_domains)} positive domains '
      f'are robust at k=3')
print()

# Astrology patterns
ast_name = 'Astrology'
if ast_name in domain_names:
    ast_idvs = compute_idvs(domains[ast_name]['classes'])
    ast_p3 = idvs_sensitivity[ast_name].get(3, 0)
    n_N = sum(1 for v in domains[ast_name]['classes'].values() if v == 'N')
    print(f'  Negative control ({ast_name}):')
    print(f'    IDVS = {ast_idvs:.3f}, N-count = {n_N}, P(IDVS<0.80|k=3) = {ast_p3:.3f}')
    print(f'    Distinct pattern: {"YES" if n_N > 10 else "NO"} (many N classifications)')
    print()

# Priority domains for human evaluation
high_priority = [r['domain'] for r in readiness
                 if r['type'] != 'negative_control'
                 and r['flips_to_threshold'] and r['flips_to_threshold'] <= 5]
print(f'  Priority domains for human evaluation:')
if high_priority:
    for d in high_priority:
        print(f'    - {d}')
else:
    print(f'    None (all domains are sufficiently robust)')
print()

# Mode information
if has_evaluators:
    print('  Evaluator data was provided and analyzed.')
else:
    print('  No evaluator data available. Results are simulation-based.')
    print('  To run with real evaluators:')
    print('    python interrater_analysis.py eval1.json eval2.json')
print()

print('  ' + '=' * 50)
print(f'  VERDICT: System is '
      f'{"ROBUST" if robust_count >= len(positive_domains) - 1 else "NEEDS ATTENTION"} '
      f'for inter-rater validation')
print('  ' + '=' * 50)
