"""Inter-rater blind classification for D-A-N assignments.

Exports a blank template for a second rater to classify primitives
per domain WITHOUT seeing the original classifications. When both
classifications exist, computes Cohen's kappa per domain.

Solo stdlib: json, os, sys, csv.

Usage:
  python interrater_blind.py export <domain>     Export blank template
  python interrater_blind.py compare <domain>    Compare rater1 vs rater2
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import csv
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data')
RATER_DIR = os.path.join(DATA_DIR, 'interrater')

# ######################################################################
#  SECTION 0: DATA LOADING
# ######################################################################

with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
    prim_data = json.load(f)

with open(os.path.join(DATA_DIR, 'reference_domains.json'), 'r', encoding='utf-8') as f:
    dom_data = json.load(f)

prims = prim_data['primitivos']
prim_names = [p['nombre'] for p in prims]


# ######################################################################
#  SECTION 1: COHEN'S KAPPA
# ######################################################################

def cohens_kappa(labels_a, labels_b, categories=None):
    """Compute Cohen's kappa for inter-rater reliability.

    Args:
        labels_a, labels_b: Lists of category labels (same length).
        categories: List of possible categories. Auto-detected if None.

    Returns:
        dict with kappa, p_observed, p_expected, interpretation.
    """
    n = len(labels_a)
    if n == 0:
        return {'kappa': 0.0, 'p_observed': 0.0, 'p_expected': 0.0,
                'interpretation': 'no_data'}

    if categories is None:
        categories = sorted(set(labels_a) | set(labels_b))

    # Confusion matrix
    matrix = {}
    for c1 in categories:
        matrix[c1] = {}
        for c2 in categories:
            matrix[c1][c2] = 0

    for a, b in zip(labels_a, labels_b):
        matrix[a][b] += 1

    # Observed agreement
    p_o = sum(matrix[c][c] for c in categories) / n

    # Expected agreement by chance
    p_e = 0.0
    for c in categories:
        p_a = sum(matrix[c][c2] for c2 in categories) / n
        p_b = sum(matrix[c1][c] for c1 in categories) / n
        p_e += p_a * p_b

    if abs(1 - p_e) < 1e-10:
        kappa = 1.0 if p_o == 1.0 else 0.0
    else:
        kappa = (p_o - p_e) / (1 - p_e)

    # Interpretation (Landis & Koch 1977)
    if kappa < 0:
        interp = 'poor'
    elif kappa < 0.21:
        interp = 'slight'
    elif kappa < 0.41:
        interp = 'fair'
    elif kappa < 0.61:
        interp = 'moderate'
    elif kappa < 0.81:
        interp = 'substantial'
    else:
        interp = 'almost_perfect'

    return {
        'kappa': round(kappa, 4),
        'p_observed': round(p_o, 4),
        'p_expected': round(p_e, 4),
        'interpretation': interp,
        'n': n,
        'confusion': {c1: dict(matrix[c1]) for c1 in categories},
    }


# ######################################################################
#  SECTION 2: EXPORT BLANK TEMPLATE
# ######################################################################

def export_template(domain_name):
    """Export a CSV template for blind classification."""
    os.makedirs(RATER_DIR, exist_ok=True)

    out_path = os.path.join(RATER_DIR, f'{domain_name}_rater2.csv')

    # Randomize order to avoid ordering bias
    import random
    rng = random.Random(hash(domain_name))
    shuffled = list(prim_names)
    rng.shuffle(shuffled)

    with open(out_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['primitivo', 'capa', 'definicion', 'clasificacion_DAN'])
        for name in shuffled:
            prim = next(p for p in prims if p['nombre'] == name)
            writer.writerow([name, prim['capa'], prim['def'], ''])

    print(f'Exported blank template to: {out_path}')
    print(f'  {len(prim_names)} primitivos in randomized order.')
    print(f'  Fill the clasificacion_DAN column with D, A, or N.')
    print(f'  D = Definitorio (essential to the domain)')
    print(f'  A = Accesorio (present but not essential)')
    print(f'  N = No aplica (not relevant to the domain)')
    print()
    print(f'  Domain: {domain_name}')
    print(f'  IMPORTANT: Do NOT look at the existing classifications before filling.')
    return out_path


# ######################################################################
#  SECTION 3: COMPARE RATERS
# ######################################################################

def compare_raters(domain_name):
    """Compare original classification with rater2."""
    # Rater 1: from reference_domains.json
    dom_info = dom_data['domains'].get(domain_name)
    if dom_info is None:
        print(f'ERROR: Domain "{domain_name}" not found.')
        return None

    rater1 = dom_info.get('classes', dom_info)
    if isinstance(rater1, dict) and 'classes' in rater1:
        rater1 = rater1['classes']

    # Rater 2: from CSV
    csv_path = os.path.join(RATER_DIR, f'{domain_name}_rater2.csv')
    if not os.path.exists(csv_path):
        print(f'ERROR: Rater 2 file not found: {csv_path}')
        print(f'  Run: python interrater_blind.py export {domain_name}')
        return None

    rater2 = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['primitivo']
            cls = row.get('clasificacion_DAN', '').strip().upper()
            if cls in ('D', 'A', 'N'):
                rater2[name] = cls

    if len(rater2) < len(prim_names) * 0.8:
        print(f'WARNING: Only {len(rater2)}/{len(prim_names)} classified by rater 2.')

    # Build parallel arrays
    labels_1 = []
    labels_2 = []
    for name in prim_names:
        if name in rater1 and name in rater2:
            labels_1.append(rater1[name])
            labels_2.append(rater2[name])

    print('=' * 70)
    print(f'Inter-rater comparison: {domain_name}')
    print('=' * 70)
    print(f'\n  Rater 1 (original): {len(rater1)} classifications')
    print(f'  Rater 2 (blind):    {len(rater2)} classifications')
    print(f'  Overlap:            {len(labels_1)} primitivos')

    result = cohens_kappa(labels_1, labels_2, ['D', 'A', 'N'])

    print(f'\n  Cohen\'s kappa: {result["kappa"]:.3f} ({result["interpretation"]})')
    print(f'  Observed agreement: {result["p_observed"]:.3f}')
    print(f'  Expected by chance: {result["p_expected"]:.3f}')

    # Confusion matrix
    print(f'\n  Confusion matrix (Rater1 rows, Rater2 columns):')
    print(f'  {"":>4} {"D":>6} {"A":>6} {"N":>6}')
    for r1_cat in ['D', 'A', 'N']:
        d = result['confusion'].get(r1_cat, {})
        print(f'  {r1_cat:>4} {d.get("D", 0):>6} {d.get("A", 0):>6} {d.get("N", 0):>6}')

    # Disagreements
    print(f'\n  Disagreements:')
    n_shown = 0
    for name in prim_names:
        if name in rater1 and name in rater2:
            if rater1[name] != rater2[name]:
                if n_shown < 20:
                    prim = next(p for p in prims if p['nombre'] == name)
                    print(f'    {name:<20} capa={prim["capa"]} '
                          f'R1={rater1[name]} R2={rater2[name]}')
                n_shown += 1

    total_disagree = sum(1 for n in prim_names
                        if n in rater1 and n in rater2 and rater1[n] != rater2[n])
    if total_disagree > 20:
        print(f'    ... and {total_disagree - 20} more')

    # Verdict
    print(f'\n  --- Verdict ---')
    status = dom_data['domains'][domain_name].get('validation_status', 'unknown')

    if result['kappa'] >= 0.60:
        print(f'  RELIABLE: kappa >= 0.60, classifications are trustworthy.')
        if status == 'candidate':
            print(f'  -> Domain can be upgraded from "candidate" to "validated"')
            print(f'     IF IDVS also exceeds 0.90 after resolving disagreements.')
    elif result['kappa'] >= 0.40:
        print(f'  MODERATE: kappa 0.40-0.60, resolve disagreements before relying.')
    else:
        print(f'  UNRELIABLE: kappa < 0.40, classifications need major revision.')

    # Save
    os.makedirs(RATER_DIR, exist_ok=True)
    out_path = os.path.join(RATER_DIR, f'{domain_name}_kappa.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f'\n  Saved to: {out_path}')

    return result


# ######################################################################
#  SECTION 4: MAIN
# ######################################################################

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage:')
        print('  python interrater_blind.py export <domain>')
        print('  python interrater_blind.py compare <domain>')
        print()
        print('Domains:', ', '.join(dom_data['domains'].keys()))
        sys.exit(1)

    action = sys.argv[1]
    domain = sys.argv[2]

    if action == 'export':
        export_template(domain)
    elif action == 'compare':
        compare_raters(domain)
    else:
        print(f'Unknown action: {action}. Use "export" or "compare".')
        sys.exit(1)
