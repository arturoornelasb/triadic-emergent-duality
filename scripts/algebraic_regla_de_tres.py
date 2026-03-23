"""Algebraic Regla de Tres: operator-level proportionality tests.

Tests whether algebraic operators (transition, internal, skip) exhibit
proportional relationships at the vector level. Three representation
methods, composition verification, and predictions for V4.

Usage:
    python algebraic_regla_de_tres.py
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

# Algebraic classification from verify_algebraic_layers.py results
TRANSITIONS = ['D8_uno_muchos', 'D6_movimiento', 'D7_orden', 'D5_identidad', 'D14_sujeto_objeto']
INTERNALS = ['D1_existir', 'D9_dentro_fuera', 'D3_tiempo', 'D12_causa_efecto',
             'D4_posibilidad', 'D13_semejante_diferente', 'D11_vida_muerte']
SKIPS = ['D2_espacio', 'D10_parte_todo']

# Ordered by the capas they connect
TRANSITION_CHAIN = ['D8_uno_muchos', 'D6_movimiento', 'D7_orden', 'D5_identidad', 'D14_sujeto_objeto']
# Internals ordered by capa
INTERNAL_CHAIN = ['D1_existir', 'D9_dentro_fuera', 'D3_tiempo', 'D12_causa_efecto',
                  'D4_posibilidad', 'D13_semejante_diferente', 'D11_vida_muerte']
INTERNAL_CAPAS = [1, 2, 3, 3, 4, 4, 5]


# ######################################################################
#  SECTION 0: DATA LOADING
# ######################################################################

def load_data():
    with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
        prim_data = json.load(f)
    with open(os.path.join(DATA_DIR, 'dualidad_primitivo_map.json'), 'r', encoding='utf-8') as f:
        dual_data = json.load(f)

    prims = prim_data['primitivos']
    name_to_capa = {p['nombre']: p['capa'] for p in prims}
    name_to_bit = {p['nombre']: p['bit'] for p in prims}
    name_to_primo = {p['nombre']: p['primo'] for p in prims}
    name_to_deps = {p['nombre']: list(p['deps']) for p in prims}
    n_bits = 72

    # Transitive ancestors
    parents = defaultdict(set)
    for p in prims:
        for d in p['deps']:
            parents[p['nombre']].add(d)

    ancestor_cache = {}

    def compute_ancestors(node):
        if node in ancestor_cache:
            return ancestor_cache[node]
        result = set()
        queue = deque(list(parents.get(node, set())))
        while queue:
            n = queue.popleft()
            if n not in result:
                result.add(n)
                for par in parents.get(n, set()):
                    if par not in result:
                        queue.append(par)
        ancestor_cache[node] = result
        return result

    ancestors = {p['nombre']: compute_ancestors(p['nombre']) for p in prims}

    # Load gold signatures (72-bit)
    gold = {}
    if os.path.exists(GOLD_PATH):
        with open(GOLD_PATH, 'r', encoding='utf-8') as f:
            gold = json.load(f)

    # Build nombre→gold_entry map
    nombre_to_gold = {}
    for k, v in gold.items():
        nombre_to_gold[v['nombre']] = v

    return (prim_data, dual_data, prims, name_to_capa, name_to_bit,
            name_to_primo, name_to_deps, ancestors, nombre_to_gold, n_bits)


# ######################################################################
#  SECTION 1: OPERATOR REPRESENTATIONS
# ######################################################################

def cosine(a, b):
    """Cosine similarity between two lists of numbers."""
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def hamming(a, b):
    """Hamming distance between two binary vectors."""
    return sum(1 for x, y in zip(a, b) if x != y)


def build_operator_vectors(dual_data, nombre_to_gold, name_to_primo, n_bits):
    """Build 3 representations for each duality operator."""

    dualidades = dual_data['dualidades']
    operators = {}

    for d_id, d_info in dualidades.items():
        anclas = d_info['anclas']
        secundarios = d_info['secundarios']
        all_members = anclas + secundarios

        # Method A: OR-union of binary signatures of all anchors
        vec_a = [0] * n_bits
        for name in anclas:
            entry = nombre_to_gold.get(name)
            if entry:
                sig = entry['binary_signature']
                for i in range(min(len(sig), n_bits)):
                    vec_a[i] = vec_a[i] | sig[i]

        # Method B: XOR-distinction of dual pairs within the duality
        # For dualities with even number of anchors, XOR first half vs second half
        # For odd, XOR all vs zero
        vec_b = [0] * n_bits
        if len(anclas) >= 2:
            half = len(anclas) // 2
            group1 = anclas[:half]
            group2 = anclas[half:]
            sig1 = [0] * n_bits
            sig2 = [0] * n_bits
            for name in group1:
                entry = nombre_to_gold.get(name)
                if entry:
                    for i in range(min(len(entry['binary_signature']), n_bits)):
                        sig1[i] = sig1[i] | entry['binary_signature'][i]
            for name in group2:
                entry = nombre_to_gold.get(name)
                if entry:
                    for i in range(min(len(entry['binary_signature']), n_bits)):
                        sig2[i] = sig2[i] | entry['binary_signature'][i]
            for i in range(n_bits):
                vec_b[i] = sig1[i] ^ sig2[i]

        # Method C: sigma primos (product of anchor primes, stored as log2)
        sigma = 1
        for name in anclas:
            if name in name_to_primo:
                sigma *= name_to_primo[name]
        log_sigma = math.log2(sigma) if sigma > 1 else 0.0

        # Extended sigma (anchors + secondaries)
        sigma_ext = 1
        for name in all_members:
            if name in name_to_primo:
                sigma_ext *= name_to_primo[name]
        log_sigma_ext = math.log2(sigma_ext) if sigma_ext > 1 else 0.0

        operators[d_id] = {
            'vec_a': vec_a,         # OR-union
            'vec_b': vec_b,         # XOR-distinction
            'sigma': sigma,         # Prime product
            'log_sigma': log_sigma,
            'sigma_ext': sigma_ext,
            'log_sigma_ext': log_sigma_ext,
            'active_a': sum(vec_a),
            'active_b': sum(vec_b),
        }

    return operators


# ######################################################################
#  SECTION 2: TRANSITION CHAIN PROPORTIONALITY
# ######################################################################

def test_transition_proportionality(operators):
    """Test D8:D6 :: D7:D5 :: D5:D14 proportionality."""

    results = {
        'pairwise_cosines_a': {},
        'pairwise_cosines_b': {},
        'ratios': [],
    }

    chain = TRANSITION_CHAIN

    # Pairwise cosines for methods A and B
    for i in range(len(chain)):
        for j in range(i + 1, len(chain)):
            di, dj = chain[i], chain[j]
            key = '%s/%s' % (di, dj)
            cos_a = cosine(operators[di]['vec_a'], operators[dj]['vec_a'])
            cos_b = cosine(operators[di]['vec_b'], operators[dj]['vec_b'])
            results['pairwise_cosines_a'][key] = round(cos_a, 4)
            results['pairwise_cosines_b'][key] = round(cos_b, 4)

    # Adjacent ratios: cos(Di,Di+1) / cos(Di+1,Di+2)
    for method_name, method_key in [('OR-union', 'vec_a'), ('XOR-distinct', 'vec_b')]:
        adj_cosines = []
        for i in range(len(chain) - 1):
            di, dj = chain[i], chain[i + 1]
            c = cosine(operators[di][method_key], operators[dj][method_key])
            adj_cosines.append((di, dj, c))

        for i in range(len(adj_cosines) - 1):
            di, dj, cos1 = adj_cosines[i]
            dk, dl, cos2 = adj_cosines[i + 1]
            ratio = cos1 / cos2 if cos2 != 0 else float('inf')
            passed = 0.5 <= ratio <= 2.0
            results['ratios'].append({
                'method': method_name,
                'pair1': '%s/%s' % (di, dj),
                'pair2': '%s/%s' % (dk, dl),
                'cos1': round(cos1, 4),
                'cos2': round(cos2, 4),
                'ratio': round(ratio, 4) if ratio != float('inf') else 'inf',
                'passed': passed,
            })

    # Sigma-based proportionality
    log_sigmas = [operators[d]['log_sigma'] for d in chain]
    sigma_ratios = []
    for i in range(len(log_sigmas) - 1):
        r = log_sigmas[i] / log_sigmas[i + 1] if log_sigmas[i + 1] != 0 else float('inf')
        sigma_ratios.append(round(r, 4) if r != float('inf') else 'inf')
    results['sigma_chain'] = {
        'log_sigmas': [round(s, 2) for s in log_sigmas],
        'ratios': sigma_ratios,
    }

    return results


# ######################################################################
#  SECTION 3: INTERNAL OPERATOR PROPORTIONALITY
# ######################################################################

def test_internal_proportionality(operators):
    """Test D1:D9 :: D3:D4 :: D11:[?] proportionality among internals."""

    results = {
        'pairwise_cosines': {},
        'predicted_c6_vector': None,
    }

    chain = INTERNAL_CHAIN

    # Pairwise cosines (method A: OR-union)
    for i in range(len(chain)):
        for j in range(i + 1, len(chain)):
            di, dj = chain[i], chain[j]
            key = '%s/%s' % (di, dj)
            cos_a = cosine(operators[di]['vec_a'], operators[dj]['vec_a'])
            results['pairwise_cosines'][key] = round(cos_a, 4)

    # Adjacent cosines within the internal chain
    adj_cosines = []
    for i in range(len(chain) - 1):
        di, dj = chain[i], chain[i + 1]
        c = cosine(operators[di]['vec_a'], operators[dj]['vec_a'])
        adj_cosines.append({
            'pair': '%s/%s' % (di, dj),
            'capas': '%d→%d' % (INTERNAL_CAPAS[i], INTERNAL_CAPAS[i + 1]),
            'cosine': round(c, 4),
        })
    results['adjacent_cosines'] = adj_cosines

    # Predict capa 6 internal operator vector
    # Strategy: average the pattern of consecutive internal operators
    # The "missing" vector should have similar relationship to D11 as D11 has to D4/D13
    # Simple prediction: OR of c6 primitivo sigs (since that's what an internal would look like)
    results['prediction_note'] = (
        'No c6 internal exists — prediction would require c6 anchor+secondary pattern. '
        'Based on internal chain pattern, the c6 operator should have '
        'cosine ~%.3f with D11_vida_muerte (average of last 3 adjacent cosines).' %
        (sum(c['cosine'] for c in adj_cosines[-3:]) / 3 if len(adj_cosines) >= 3 else 0)
    )

    return results


# ######################################################################
#  SECTION 4: SKIP OPERATOR COMPOSITION
# ######################################################################

def test_skip_composition(operators):
    """Test D2 ≈ D6∘D7 and D10 ≈ D6∘D7 (skips as compositions)."""

    results = {}

    # D2 and D10 both skip c2→c4 (bypassing c3)
    # The chain through c3 is D6(2→3) then D7(3→4)
    # Composition: element-wise AND of OR-union vectors

    d6_a = operators['D6_movimiento']['vec_a']
    d7_a = operators['D7_orden']['vec_a']

    # AND composition: bits active in BOTH transition operators
    composed = [a & b for a, b in zip(d6_a, d7_a)]

    for skip_id in SKIPS:
        skip_vec = operators[skip_id]['vec_a']
        cos_direct = cosine(skip_vec, composed)
        cos_d6 = cosine(skip_vec, d6_a)
        cos_d7 = cosine(skip_vec, d7_a)

        # Also try OR composition
        composed_or = [a | b for a, b in zip(d6_a, d7_a)]
        cos_or = cosine(skip_vec, composed_or)

        results[skip_id] = {
            'cos_vs_AND_composition': round(cos_direct, 4),
            'cos_vs_OR_composition': round(cos_or, 4),
            'cos_vs_D6': round(cos_d6, 4),
            'cos_vs_D7': round(cos_d7, 4),
            'active_bits_skip': sum(skip_vec),
            'active_bits_AND': sum(composed),
            'active_bits_OR': sum(composed_or),
            'hamming_vs_AND': hamming(skip_vec, composed),
            'hamming_vs_OR': hamming(skip_vec, composed_or),
        }

    # Sigma composition: D2 sigma vs GCD(D6,D7) and LCM(D6,D7)
    s6 = operators['D6_movimiento']['sigma']
    s7 = operators['D7_orden']['sigma']
    gcd_67 = math.gcd(s6, s7)
    lcm_67 = s6 * s7 // gcd_67 if gcd_67 > 0 else 0

    for skip_id in SKIPS:
        s_skip = operators[skip_id]['sigma']
        results[skip_id]['sigma_skip'] = s_skip
        results[skip_id]['sigma_GCD_D6_D7'] = gcd_67
        results[skip_id]['sigma_LCM_D6_D7'] = lcm_67
        results[skip_id]['sigma_divides_LCM'] = (lcm_67 % s_skip == 0) if s_skip > 0 else False

    return results


# ######################################################################
#  SECTION 5: CROSS-METHOD CONSISTENCY
# ######################################################################

def test_cross_method_consistency(operators):
    """Spearman rank correlation between methods A, B, C for all 14 dualities."""

    all_ids = sorted(operators.keys())

    # Build pairwise distance matrices for each method
    def pairwise_distances(vec_key):
        dists = {}
        for i, di in enumerate(all_ids):
            for j, dj in enumerate(all_ids):
                if i < j:
                    c = cosine(operators[di][vec_key], operators[dj][vec_key])
                    dists[(di, dj)] = 1.0 - c  # distance = 1 - cosine
        return dists

    dist_a = pairwise_distances('vec_a')
    dist_b = pairwise_distances('vec_b')

    # Sigma distances: |log(sigma_i) - log(sigma_j)|
    dist_c = {}
    for i, di in enumerate(all_ids):
        for j, dj in enumerate(all_ids):
            if i < j:
                dist_c[(di, dj)] = abs(
                    operators[di]['log_sigma'] - operators[dj]['log_sigma'])

    # Spearman correlation: rank correlation between distance vectors
    def spearman(d1, d2):
        keys = sorted(d1.keys())
        vals1 = [d1[k] for k in keys]
        vals2 = [d2[k] for k in keys]

        def rank(vals):
            indexed = sorted(range(len(vals)), key=lambda i: vals[i])
            ranks = [0] * len(vals)
            for r, idx in enumerate(indexed):
                ranks[idx] = r + 1
            return ranks

        r1 = rank(vals1)
        r2 = rank(vals2)
        n = len(r1)
        d_sq = sum((a - b) ** 2 for a, b in zip(r1, r2))
        rho = 1 - (6 * d_sq) / (n * (n * n - 1))
        return round(rho, 4)

    results = {
        'spearman_A_B': spearman(dist_a, dist_b),
        'spearman_A_C': spearman(dist_a, dist_c),
        'spearman_B_C': spearman(dist_b, dist_c),
    }

    return results


# ######################################################################
#  SECTION 6: PREDICTIONS FOR V4
# ######################################################################

def make_v4_predictions(operators, nombre_to_gold):
    """Generate predictions for V4 training based on algebraic analysis."""

    predictions = []

    # Prediction 1: Algebraic distance correlates with dual coherence
    # Pairs with greater algebraic span should have higher coherence
    # (because their signatures are more distinct)
    dual_pairs_by_distance = {
        'distance_0': {
            'desc': 'Same-capa dual pairs (internal operators)',
            'examples': ['vida/muerte', 'placer/dolor', 'consciente/ausente'],
            'expected_coherence': 'LOWEST — high Jaccard overlap',
        },
        'distance_1': {
            'desc': 'Adjacent-capa dual pairs (transition operators)',
            'examples': ['individual/colectivo', 'mover/quietud'],
            'expected_coherence': 'MEDIUM — moderate overlap',
        },
        'distance_2': {
            'desc': 'Skip-capa dual pairs (skip operators)',
            'examples': ['atracción/aversión'],
            'expected_coherence': 'HIGHEST — low Jaccard overlap',
        },
    }
    predictions.append({
        'id': 'P1',
        'hypothesis': 'Algebraic distance predicts dual coherence',
        'detail': 'Pairs spanning more capas → more distinct signatures → higher coherence',
        'groups': dual_pairs_by_distance,
        'test': 'Compare mean coherence by algebraic distance group in V4 results',
    })

    # Prediction 2: New primitivos (bits 65-71) improve collapsed pairs
    collapsed_v3 = [
        ('vida', 'muerte', 0.789),
        ('placer', 'dolor', 0.714),
        ('consciente', 'ausente', 0.818),
        ('individual', 'colectivo', 0.800),
        ('receptivo', 'creador_obs', 0.750),
    ]
    v4_jaccards = []
    for a, b, v3_jaccard in collapsed_v3:
        ga = nombre_to_gold.get(a)
        gb = nombre_to_gold.get(b)
        if ga and gb:
            bits_a = set(ga['active_bits'])
            bits_b = set(gb['active_bits'])
            inter = len(bits_a & bits_b)
            union = len(bits_a | bits_b)
            v4_jaccard = inter / union if union else 0
            v4_jaccards.append({
                'pair': '%s/%s' % (a, b),
                'v3_jaccard': v3_jaccard,
                'v4_jaccard': round(v4_jaccard, 4),
                'improved': v4_jaccard < v3_jaccard,
                'delta': round(v3_jaccard - v4_jaccard, 4),
            })

    predictions.append({
        'id': 'P2',
        'hypothesis': '72-bit circle reduces Jaccard of collapsed pairs',
        'detail': 'New primitivos (bits 65-71) add differentiation to high-Jaccard pairs',
        'pairs': v4_jaccards,
        'test': 'All 5 pairs should show Jaccard reduction in V4 vs V3',
    })

    # Prediction 3: Transitions learn better than internals
    predictions.append({
        'id': 'P3',
        'hypothesis': 'Transition operators produce higher per-domain accuracy than internals',
        'detail': 'Transitions connect distinct algebraic domains → clearer gradient signal',
        'transitions': TRANSITION_CHAIN,
        'internals': INTERNAL_CHAIN,
        'test': 'Compare mean per-domain accuracy: transition domains vs internal domains in V4',
    })

    # Prediction 4: Capa 6 coherence is lowest
    predictions.append({
        'id': 'P4',
        'hypothesis': 'Capa 6 dual pairs have lowest coherence due to missing internal operator',
        'detail': 'temporal_obs/eterno_obs and receptivo/creador_obs lack algebraic internal structure',
        'c6_pairs': ['temporal_obs/eterno_obs', 'receptivo/creador_obs'],
        'test': 'C6 coherence < C5 coherence < C4 coherence in V4',
    })

    # Prediction 5: D14 multi-role produces mixed results
    predictions.append({
        'id': 'P5',
        'hypothesis': 'D14_sujeto_objeto domains show high variance due to multi-role spanning capas 4-6',
        'detail': 'D14 serves as transition 4→5, 5→6, AND 4→6 simultaneously — conflicting gradients',
        'test': 'Variance of per-capa accuracy for D14 members > mean variance of other dualidades',
    })

    return predictions


# ######################################################################
#  MAIN
# ######################################################################

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    print('=' * 70)
    print('  ALGEBRAIC REGLA DE TRES')
    print('  Operator-level proportionality + V4 predictions')
    print('=' * 70)

    (prim_data, dual_data, prims, name_to_capa, name_to_bit,
     name_to_primo, name_to_deps, ancestors, nombre_to_gold, n_bits) = load_data()

    # ---- SECTION 1: Operator representations ----
    print()
    print('=' * 70)
    print('  SECTION 1: OPERATOR REPRESENTATIONS')
    print('=' * 70)

    operators = build_operator_vectors(dual_data, nombre_to_gold, name_to_primo, n_bits)

    print()
    print('  %-25s %6s %6s %10s %10s' % (
        'Dualidad', 'Act_A', 'Act_B', 'log2(σ)', 'log2(σ_ext)'))
    print('  ' + '-' * 60)
    for d_id in TRANSITION_CHAIN + INTERNAL_CHAIN + SKIPS:
        op = operators[d_id]
        print('  %-25s %6d %6d %10.2f %10.2f' % (
            d_id, op['active_a'], op['active_b'], op['log_sigma'], op['log_sigma_ext']))

    # ---- SECTION 2: Transition proportionality ----
    print()
    print('=' * 70)
    print('  SECTION 2: TRANSITION CHAIN PROPORTIONALITY')
    print('=' * 70)

    trans_results = test_transition_proportionality(operators)

    print()
    print('  Method A (OR-union) pairwise cosines:')
    for key, val in sorted(trans_results['pairwise_cosines_a'].items()):
        print('    %-50s cos=%.4f' % (key, val))

    print()
    print('  Method B (XOR-distinction) pairwise cosines:')
    for key, val in sorted(trans_results['pairwise_cosines_b'].items()):
        print('    %-50s cos=%.4f' % (key, val))

    print()
    print('  Adjacent ratios (proportionality test):')
    for r in trans_results['ratios']:
        status = 'PASS' if r['passed'] else 'FAIL'
        ratio_str = '%.4f' % r['ratio'] if r['ratio'] != 'inf' else 'inf'
        print('    [%s] %s cos=%.4f / %s cos=%.4f = ratio %s  %s' % (
            r['method'], r['pair1'], r['cos1'], r['pair2'], r['cos2'],
            ratio_str, status))

    print()
    print('  Sigma chain (log2):')
    sc = trans_results['sigma_chain']
    print('    Values: %s' % sc['log_sigmas'])
    print('    Ratios: %s' % sc['ratios'])

    # ---- SECTION 3: Internal proportionality ----
    print()
    print('=' * 70)
    print('  SECTION 3: INTERNAL OPERATOR PROPORTIONALITY')
    print('=' * 70)

    int_results = test_internal_proportionality(operators)

    print()
    print('  Adjacent internal cosines:')
    for ac in int_results['adjacent_cosines']:
        print('    %-45s capas %-6s cos=%.4f' % (ac['pair'], ac['capas'], ac['cosine']))

    print()
    print('  Note: %s' % int_results['prediction_note'])

    # ---- SECTION 4: Skip composition ----
    print()
    print('=' * 70)
    print('  SECTION 4: SKIP OPERATOR COMPOSITION')
    print('  Testing: D2 ≈ D6∘D7 and D10 ≈ D6∘D7')
    print('=' * 70)

    skip_results = test_skip_composition(operators)

    print()
    for skip_id, sr in skip_results.items():
        print('  %s:' % skip_id)
        print('    cos vs AND(D6,D7): %.4f   (active: skip=%d, AND=%d)' % (
            sr['cos_vs_AND_composition'], sr['active_bits_skip'], sr['active_bits_AND']))
        print('    cos vs OR(D6,D7):  %.4f   (active: skip=%d, OR=%d)' % (
            sr['cos_vs_OR_composition'], sr['active_bits_skip'], sr['active_bits_OR']))
        print('    cos vs D6 alone:   %.4f' % sr['cos_vs_D6'])
        print('    cos vs D7 alone:   %.4f' % sr['cos_vs_D7'])
        print('    hamming vs AND:    %d   hamming vs OR: %d' % (
            sr['hamming_vs_AND'], sr['hamming_vs_OR']))
        print('    sigma divides LCM(D6,D7): %s' % sr['sigma_divides_LCM'])
        print()

    # ---- SECTION 5: Cross-method consistency ----
    print()
    print('=' * 70)
    print('  SECTION 5: CROSS-METHOD CONSISTENCY (Spearman)')
    print('=' * 70)

    cross_results = test_cross_method_consistency(operators)

    print()
    print('  Spearman rank correlation of pairwise distances:')
    print('    A(OR-union) vs B(XOR-distinct): ρ=%.4f' % cross_results['spearman_A_B'])
    print('    A(OR-union) vs C(sigma-prime):  ρ=%.4f' % cross_results['spearman_A_C'])
    print('    B(XOR-dist) vs C(sigma-prime):  ρ=%.4f' % cross_results['spearman_B_C'])

    # ---- SECTION 6: V4 Predictions ----
    print()
    print('=' * 70)
    print('  SECTION 6: V4 PREDICTIONS')
    print('=' * 70)

    predictions = make_v4_predictions(operators, nombre_to_gold)

    for pred in predictions:
        print()
        print('  [%s] %s' % (pred['id'], pred['hypothesis']))
        print('    %s' % pred['detail'])
        if 'pairs' in pred:
            for p in pred['pairs']:
                delta_str = '+%.4f' % p['delta'] if p['delta'] > 0 else '%.4f' % p['delta']
                print('      %s: v3=%.3f → v4=%.3f  delta=%s  %s' % (
                    p['pair'], p['v3_jaccard'], p['v4_jaccard'], delta_str,
                    'IMPROVED' if p['improved'] else 'SAME/WORSE'))
        print('    Test: %s' % pred['test'])

    # ---- BUILD RESULTS ----
    all_results = {
        'operator_representations': {
            d_id: {
                'active_a': op['active_a'],
                'active_b': op['active_b'],
                'log_sigma': op['log_sigma'],
                'log_sigma_ext': op['log_sigma_ext'],
            }
            for d_id, op in operators.items()
        },
        'transition_proportionality': trans_results,
        'internal_proportionality': int_results,
        'skip_composition': skip_results,
        'cross_method_consistency': cross_results,
        'v4_predictions': [
            {k: v for k, v in pred.items()}
            for pred in predictions
        ],
    }

    out_path = os.path.join(RESULTS_DIR, 'algebraic_regla_de_tres.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)

    # ---- SYNTHESIS ----
    print()
    print('=' * 70)
    print('  SYNTHESIS')
    print('=' * 70)
    print()

    # Count passes
    pass_count = sum(1 for r in trans_results['ratios'] if r['passed'])
    total_ratios = len(trans_results['ratios'])
    print('  Transition proportionality: %d/%d ratios in [0.5, 2.0]' % (pass_count, total_ratios))

    # Skip composition verdict
    for skip_id, sr in skip_results.items():
        best = max(sr['cos_vs_AND_composition'], sr['cos_vs_OR_composition'])
        print('  %s best composition cos: %.4f (%s)' % (
            skip_id, best,
            'AND' if sr['cos_vs_AND_composition'] > sr['cos_vs_OR_composition'] else 'OR'))

    print('  Cross-method Spearman: A↔B=%.3f  A↔C=%.3f  B↔C=%.3f' % (
        cross_results['spearman_A_B'],
        cross_results['spearman_A_C'],
        cross_results['spearman_B_C']))
    print('  V4 predictions: %d hypotheses registered' % len(predictions))
    print()
    print('  Results saved: %s' % out_path)
    print('=' * 70)


if __name__ == '__main__':
    main()
