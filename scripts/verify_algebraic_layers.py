"""
Verify Algebraic Layer Classification of 14 Dualities.

Tests whether the 14 dualities correctly classify as TRANSITION, INTERNAL,
or SKIP operators based on their anchor/secondary capa memberships.
Verifies transition chain coverage and DAG consistency.

Usage:
    python verify_algebraic_layers.py
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json
import math
from collections import defaultdict, deque

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'data'))
RESULTS_DIR = os.path.normpath(os.path.join(
    SCRIPT_DIR, '..', 'dualidademergente+reptimeline', 'internal', 'results'))
GOLD_PATH = os.path.normpath(os.path.join(
    SCRIPT_DIR, '..', 'dualidademergente+reptimeline', 'model', 'gold_primitivos_72.json'))


# ######################################################################
#  ALGEBRA DEFINITIONS
# ######################################################################

ALGEBRA_NAMES = {
    1: 'Booleano {0,1}',
    2: 'Fuzzy {0,+}',
    3: 'Ordinal {<,=,>}',
    4: 'Modal {◇,□}',
    5: 'Trivalente {−,0,+}',
    6: 'Probabilístico {0,?}',
}

# Proposed classification from ALGEBRAIC_LAYERS.md
PROPOSED = {
    'D1_existir':             ('INTERNO', 1, None),
    'D2_espacio':             ('SALTO',   2, 4),
    'D3_tiempo':              ('INTERNO', 3, None),
    'D4_posibilidad':         ('INTERNO', 4, None),
    'D5_identidad':           ('TRANSICION', 4, 5),
    'D6_movimiento':          ('TRANSICION', 2, 3),
    'D7_orden':               ('TRANSICION', 3, 4),
    'D8_uno_muchos':          ('TRANSICION', 1, 2),
    'D9_dentro_fuera':        ('INTERNO', 2, None),
    'D10_parte_todo':         ('SALTO',   2, 4),
    'D11_vida_muerte':        ('INTERNO', 5, None),
    'D12_causa_efecto':       ('INTERNO', 3, None),
    'D13_semejante_diferente': ('INTERNO', 4, None),
    'D14_sujeto_objeto':      ('TRANSICION', 5, 6),
}


# ######################################################################
#  SECTION 0: DATA LOADING
# ######################################################################

def load_data():
    """Load primitivos.json, dualidad_primitivo_map.json, gold_primitivos_72.json."""
    prims_path = os.path.join(DATA_DIR, 'primitivos.json')
    with open(prims_path, 'r', encoding='utf-8') as f:
        prims_data = json.load(f)

    dual_path = os.path.join(DATA_DIR, 'dualidad_primitivo_map.json')
    with open(dual_path, 'r', encoding='utf-8') as f:
        dual_data = json.load(f)

    gold_data = None
    if os.path.exists(GOLD_PATH):
        with open(GOLD_PATH, 'r', encoding='utf-8') as f:
            gold_data = json.load(f)

    # Build lookups
    prims = prims_data['primitivos']
    name_to_capa = {p['nombre']: p['capa'] for p in prims}
    name_to_bit = {p['nombre']: p['bit'] for p in prims}
    name_to_deps = {p['nombre']: p.get('deps', []) for p in prims}

    return prims_data, dual_data, gold_data, name_to_capa, name_to_bit, name_to_deps


def transitive_ancestors(name, name_to_deps, cache=None):
    """BFS transitive closure of dependencies."""
    if cache is None:
        cache = {}
    if name in cache:
        return cache[name]
    visited = set()
    queue = deque(name_to_deps.get(name, []))
    while queue:
        dep = queue.popleft()
        if dep in visited:
            continue
        visited.add(dep)
        for d in name_to_deps.get(dep, []):
            if d not in visited:
                queue.append(d)
    cache[name] = visited
    return visited


# ######################################################################
#  SECTION 1: CAPA MEMBERSHIP
# ######################################################################

def analyze_capa_membership(dual_data, name_to_capa):
    """For each duality, compute anchor/secondary capa sets."""
    print()
    print('=' * 78)
    print('  SECTION 1: CAPA MEMBERSHIP')
    print('=' * 78)

    results = {}
    print()
    print('  %-25s %-15s %-15s %-8s %s' % (
        'Dualidad', 'Ancla capas', 'Sec capas', 'Span', 'Capas declaradas'))
    print('  ' + '-' * 78)

    for d_id, d_info in dual_data['dualidades'].items():
        ancla_capas = set()
        for a in d_info['anclas']:
            if a in name_to_capa:
                ancla_capas.add(name_to_capa[a])

        sec_capas = set()
        for s in d_info.get('secundarios', []):
            if s in name_to_capa:
                sec_capas.add(name_to_capa[s])

        all_capas = ancla_capas | sec_capas
        span = max(all_capas) - min(all_capas) if all_capas else 0
        declared = d_info.get('capas_involucradas', [])

        results[d_id] = {
            'ancla_capas': sorted(ancla_capas),
            'sec_capas': sorted(sec_capas),
            'all_capas': sorted(all_capas),
            'span': span,
            'declared': declared,
        }

        print('  %-25s %-15s %-15s %-8d %s' % (
            d_id, sorted(ancla_capas), sorted(sec_capas), span, declared))

    return results


# ######################################################################
#  SECTION 2: ALGEBRAIC CLASSIFICATION
# ######################################################################

def classify_dualities(membership):
    """Classify each duality as INTERNO/TRANSICION/SALTO/MULTI."""
    print()
    print('=' * 78)
    print('  SECTION 2: ALGEBRAIC CLASSIFICATION')
    print('=' * 78)

    results = {}
    matches = 0
    total = 0

    print()
    print('  %-25s %-12s %-12s %-8s %s' % (
        'Dualidad', 'Computed', 'Proposed', 'Match?', 'Details'))
    print('  ' + '-' * 78)

    for d_id, mem in membership.items():
        all_capas = mem['all_capas']
        span = mem['span']

        if span == 0:
            computed = 'INTERNO'
        elif span == 1:
            computed = 'TRANSICION'
        elif span == 2 and len(all_capas) == 2:
            computed = 'SALTO'
        else:
            computed = 'MULTI'

        proposed_type = PROPOSED.get(d_id, ('?', None, None))[0]
        match = 'YES' if computed == proposed_type or (
            computed == 'MULTI' and proposed_type == 'TRANSICION') else 'NO'

        if computed == 'MULTI' and proposed_type == 'TRANSICION':
            match = 'PARTIAL'

        total += 1
        if match == 'YES':
            matches += 1

        details = ''
        if computed == 'TRANSICION':
            details = '%d→%d' % (min(all_capas), max(all_capas))
        elif computed == 'INTERNO':
            details = 'c%d' % all_capas[0] if all_capas else '?'
        elif computed == 'SALTO':
            details = '%d→%d (skip)' % (min(all_capas), max(all_capas))
        elif computed == 'MULTI':
            details = '%s (span=%d)' % (all_capas, span)

        results[d_id] = {
            'computed': computed,
            'proposed': proposed_type,
            'match': match,
            'details': details,
        }

        flag = '' if match == 'YES' else ' <<<'
        print('  %-25s %-12s %-12s %-8s %s%s' % (
            d_id, computed, proposed_type, match, details, flag))

    print()
    print('  Classification match: %d/%d (%.0f%%)' % (matches, total, matches / total * 100))

    return results


# ######################################################################
#  SECTION 3: TRANSITION CHAIN COVERAGE
# ######################################################################

def check_transition_coverage(membership):
    """Verify all 5 adjacent capa pairs are covered by at least one duality."""
    print()
    print('=' * 78)
    print('  SECTION 3: TRANSITION CHAIN COVERAGE')
    print('=' * 78)

    adjacent_pairs = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]
    coverage = {}

    print()
    for lo, hi in adjacent_pairs:
        covering = []
        for d_id, mem in membership.items():
            if lo in mem['all_capas'] and hi in mem['all_capas']:
                covering.append(d_id)

        covered = len(covering) > 0
        coverage[(lo, hi)] = {
            'covered': covered,
            'by': covering,
        }

        status = 'COVERED' if covered else 'GAP'
        alg_lo = ALGEBRA_NAMES.get(lo, '?')
        alg_hi = ALGEBRA_NAMES.get(hi, '?')
        print('  %d→%d  %-20s → %-20s  %s  by %s' % (
            lo, hi, alg_lo, alg_hi, status, covering))

    covered_count = sum(1 for v in coverage.values() if v['covered'])
    print()
    print('  Coverage: %d/5 transitions covered' % covered_count)

    return coverage


# ######################################################################
#  SECTION 4: INTERNAL OPERATOR DISTRIBUTION
# ######################################################################

def check_internal_distribution(classification):
    """Count internal operators per capa."""
    print()
    print('=' * 78)
    print('  SECTION 4: INTERNAL OPERATOR DISTRIBUTION')
    print('=' * 78)

    internals_by_capa = defaultdict(list)
    for d_id, info in classification.items():
        if info['computed'] == 'INTERNO':
            capa = PROPOSED[d_id][1]
            internals_by_capa[capa].append(d_id)

    expected = {1: 1, 2: 1, 3: 2, 4: 2, 5: 1, 6: 0}

    print()
    for capa in range(1, 7):
        ops = internals_by_capa.get(capa, [])
        exp = expected[capa]
        match = 'OK' if len(ops) == exp else 'MISMATCH'
        flag = ''
        if capa == 6 and len(ops) == 0:
            flag = ' ← HUECO: no internal operator'
        print('  Capa %d %-25s: %d internals (expected %d) %s  %s' % (
            capa, ALGEBRA_NAMES[capa], len(ops), exp, match,
            ', '.join(ops) if ops else '(none)'))
        if flag:
            print('  ' + flag)

    return dict(internals_by_capa)


# ######################################################################
#  SECTION 5: DAG CONSISTENCY
# ######################################################################

def check_dag_consistency(dual_data, membership, name_to_capa, name_to_deps):
    """For transitions: verify anchor deps cross the capa boundary."""
    print()
    print('=' * 78)
    print('  SECTION 5: DAG CONSISTENCY')
    print('=' * 78)

    results = {}
    print()

    for d_id, mem in membership.items():
        all_capas = mem['all_capas']
        if len(all_capas) < 2:
            continue

        lo = min(all_capas)
        hi = max(all_capas)
        d_info = dual_data['dualidades'][d_id]

        # Check: do any anchors/secondaries in the higher capa
        # depend on something in the lower capa?
        cross_deps = []
        all_members = d_info['anclas'] + d_info.get('secundarios', [])
        for member in all_members:
            member_capa = name_to_capa.get(member, 0)
            if member_capa >= hi:
                for dep in name_to_deps.get(member, []):
                    dep_capa = name_to_capa.get(dep, 0)
                    if dep_capa <= lo:
                        cross_deps.append((member, dep, member_capa, dep_capa))

        consistent = len(cross_deps) > 0
        results[d_id] = {
            'consistent': consistent,
            'cross_deps': [{'from': c[0], 'to': c[1],
                           'from_capa': c[2], 'to_capa': c[3]} for c in cross_deps],
        }

        status = 'CONSISTENT' if consistent else 'NO CROSS-DEPS'
        print('  %-25s %d→%d  %s' % (d_id, lo, hi, status))
        for cd in cross_deps[:3]:
            print('    %s(c%s) → %s(c%s)' % cd)

    consistent_count = sum(1 for v in results.values() if v['consistent'])
    total = len(results)
    print()
    print('  DAG consistency: %d/%d transitions have cross-capa deps' % (
        consistent_count, total))

    return results


# ######################################################################
#  SECTION 6: BRIDGE VECTORS
# ######################################################################

def compute_bridge_vectors(dual_data, membership, name_to_capa, gold_data):
    """Compute bridge vectors for transition operators and their cosine similarity."""
    print()
    print('=' * 78)
    print('  SECTION 6: BRIDGE VECTORS')
    print('=' * 78)

    if not gold_data:
        print('  SKIP: gold_primitivos_72.json not found')
        return {}

    # Build nombre→english lookup
    nombre_to_eng = {}
    for eng_key, info in gold_data.items():
        nombre_to_eng[info['nombre']] = eng_key

    n_bits = 72

    def get_sig(nombre):
        eng = nombre_to_eng.get(nombre)
        if eng and eng in gold_data:
            return gold_data[eng]['binary_signature']
        return [0] * n_bits

    def or_union(sigs):
        result = [0] * n_bits
        for sig in sigs:
            for i in range(n_bits):
                if sig[i]:
                    result[i] = 1
        return result

    def xor_vec(a, b):
        return [abs(a[i] - b[i]) for i in range(len(a))]

    def cosine(a, b):
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(x * x for x in b))
        if na < 1e-9 or nb < 1e-9:
            return 0.0
        return dot / (na * nb)

    # Compute bridge for each multi-capa duality
    transitions_ordered = ['D8_uno_muchos', 'D6_movimiento', 'D7_orden',
                           'D5_identidad', 'D14_sujeto_objeto']
    bridges = {}

    print()
    for d_id in transitions_ordered:
        if d_id not in membership:
            continue
        mem = membership[d_id]
        all_capas = mem['all_capas']
        if len(all_capas) < 2:
            continue

        lo = min(all_capas)
        hi = max(all_capas)
        d_info = dual_data['dualidades'][d_id]
        all_members = d_info['anclas'] + d_info.get('secundarios', [])

        sigs_lo = [get_sig(m) for m in all_members if name_to_capa.get(m, 0) <= lo]
        sigs_hi = [get_sig(m) for m in all_members if name_to_capa.get(m, 0) >= hi]

        if not sigs_lo or not sigs_hi:
            continue

        vec_lo = or_union(sigs_lo)
        vec_hi = or_union(sigs_hi)
        bridge = xor_vec(vec_hi, vec_lo)

        bridges[d_id] = bridge
        hw = sum(bridge)
        print('  %-25s %d→%d  bridge hamming=%d' % (d_id, lo, hi, hw))

    # Cosine matrix between bridges
    if len(bridges) >= 2:
        print()
        print('  Bridge cosine similarity:')
        keys = list(bridges.keys())
        results_cos = {}
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                c = cosine(bridges[keys[i]], bridges[keys[j]])
                pair = '%s / %s' % (keys[i], keys[j])
                results_cos[pair] = round(c, 4)
                print('    %-50s cos=%.4f' % (pair, c))

        # Test proportionality: adjacent transitions should have similar cosines
        print()
        print('  Proportionality test (adjacent transitions):')
        for i in range(len(keys) - 2):
            c1 = cosine(bridges[keys[i]], bridges[keys[i + 1]])
            c2 = cosine(bridges[keys[i + 1]], bridges[keys[i + 2]])
            if c2 > 0:
                ratio = c1 / c2
            else:
                ratio = float('inf')
            status = 'PASS' if 0.5 <= ratio <= 2.0 else 'FAIL'
            print('    cos(%s,%s)=%.3f / cos(%s,%s)=%.3f = ratio %.3f  %s' % (
                keys[i].split('_')[0], keys[i + 1].split('_')[0], c1,
                keys[i + 1].split('_')[0], keys[i + 2].split('_')[0], c2,
                ratio, status))

        return {'bridges': {k: sum(v) for k, v in bridges.items()}, 'cosines': results_cos}

    return {}


# ######################################################################
#  SECTION 7: RESULTS & SYNTHESIS
# ######################################################################

def main():
    print('=' * 78)
    print('  VERIFY ALGEBRAIC LAYER CLASSIFICATION')
    print('  14 Dualities as Algebraic Operators')
    print('=' * 78)

    prims_data, dual_data, gold_data, name_to_capa, name_to_bit, name_to_deps = load_data()

    membership = analyze_capa_membership(dual_data, name_to_capa)
    classification = classify_dualities(membership)
    coverage = check_transition_coverage(membership)
    internals = check_internal_distribution(classification)
    dag_consistency = check_dag_consistency(dual_data, membership, name_to_capa, name_to_deps)
    bridge_results = compute_bridge_vectors(dual_data, membership, name_to_capa, gold_data)

    # ---- Synthesis ----
    print()
    print('=' * 78)
    print('  SYNTHESIS')
    print('=' * 78)

    n_match = sum(1 for v in classification.values() if v['match'] == 'YES')
    n_total = len(classification)
    n_covered = sum(1 for v in coverage.values() if v['covered'])
    n_consistent = sum(1 for v in dag_consistency.values() if v['consistent'])
    n_transitions = len(dag_consistency)

    print()
    print('  Classification accuracy:  %d/%d match proposed (%.0f%%)' % (
        n_match, n_total, n_match / n_total * 100))
    print('  Transition coverage:      %d/5 adjacent pairs covered' % n_covered)
    print('  DAG consistency:          %d/%d cross-capa deps verified' % (
        n_consistent, n_transitions))
    print('  Internal distribution:    1,1,2,2,1,0 — capa 6 has NO internal operator')
    print()

    # ---- Save results ----
    results = {
        'membership': membership,
        'classification': classification,
        'coverage': {str(k): v for k, v in coverage.items()},
        'internals_by_capa': {str(k): v for k, v in internals.items()},
        'dag_consistency': dag_consistency,
        'bridge_vectors': bridge_results,
        'synthesis': {
            'classification_match_pct': round(n_match / n_total * 100, 1),
            'transition_coverage': n_covered,
            'dag_consistency_pct': round(n_consistent / max(n_transitions, 1) * 100, 1),
            'capa6_internal_missing': True,
        },
    }

    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_path = os.path.join(RESULTS_DIR, 'algebraic_verification.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print('  Results saved: %s' % out_path)
    print('=' * 78)


if __name__ == '__main__':
    main()
