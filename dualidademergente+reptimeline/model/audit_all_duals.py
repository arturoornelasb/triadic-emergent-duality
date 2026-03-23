"""
Audit ALL dual pairs — not just the 11 with explicit 'dual' field.

Analyzes:
  1. All 14 ejes_duales from primitivos.json
  2. Other structural pairs (más/menos, puede/debe, etc.)
  3. Discovery: find best anti-correlated pairs the model learned

Coherence = exclusive / (both_active + exclusive)
  1.0 = perfect anti-correlation (never both ON)
  0.0 = always both ON together
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'neural', 'results'))
RUNS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'runs'))


def load_signatures(run_name=None):
    """Load learned signatures from exploration.json."""
    if run_name:
        path = os.path.join(RUNS_DIR, run_name, 'exploration.json')
    else:
        path = os.path.join(RESULTS_DIR, 'exploration.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['signatures']


def load_primitivos():
    """Load primitivos.json for names and structure."""
    path = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data', 'primitivos.json'))
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def coherence(bits_a, bits_b):
    """Compute dual coherence between two bit signatures."""
    both = 0
    exclusive = 0
    agree_off = 0
    for a, b in zip(bits_a, bits_b):
        if a == 1 and b == 1:
            both += 1
        elif a == 1 or b == 1:
            exclusive += 1
        else:
            agree_off += 1
    total = both + exclusive
    if total == 0:
        return 0.0, both, exclusive, agree_off
    return exclusive / total, both, exclusive, agree_off


def jaccard(bits_a, bits_b):
    """Jaccard similarity = intersection / union of ON bits."""
    inter = sum(a == 1 and b == 1 for a, b in zip(bits_a, bits_b))
    union = sum(a == 1 or b == 1 for a, b in zip(bits_a, bits_b))
    if union == 0:
        return 0.0
    return inter / union


def hamming_distance(bits_a, bits_b):
    """Number of bits that differ."""
    return sum(a != b for a, b in zip(bits_a, bits_b))


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Audit all dual pairs')
    parser.add_argument('--run', default=None, help='Run name (default: current)')
    parser.add_argument('--compare', default=None, help='Compare with another run')
    parser.add_argument('--top-discovered', type=int, default=20,
                        help='How many discovered anti-correlated pairs to show')
    args = parser.parse_args()

    prim_data = load_primitivos()
    sigs = load_signatures(args.run)
    sigs_compare = load_signatures(args.compare) if args.compare else None

    # Build name mapping: nombre → english
    nombre_to_english = {}
    english_to_nombre = {}
    for p in prim_data['primitivos']:
        # Find english name by matching in sigs
        for eng_name in sigs:
            if sigs[eng_name].get('nombre', eng_name) == p['nombre'] or eng_name == p['nombre']:
                nombre_to_english[p['nombre']] = eng_name
                english_to_nombre[eng_name] = p['nombre']
                break

    # If mapping incomplete, try direct match
    for p in prim_data['primitivos']:
        if p['nombre'] not in nombre_to_english:
            # Try finding by matching concept names
            for eng_name in sigs:
                sig_data = sigs[eng_name]
                if isinstance(sig_data, dict) and sig_data.get('bit') == p['bit']:
                    nombre_to_english[p['nombre']] = eng_name
                    english_to_nombre[eng_name] = p['nombre']
                    break

    # All concepts available
    all_concepts = list(sigs.keys())

    print('=' * 78)
    print('  AUDIT: ALL DUAL PAIRS — COMPREHENSIVE COHERENCE ANALYSIS')
    if args.run:
        print('  Run: %s' % args.run)
    if args.compare:
        print('  Comparing with: %s' % args.compare)
    print('=' * 78)

    # ================================================================
    # [1] All 14 ejes_duales
    # ================================================================
    print()
    print('  [1] EJES DUALES (14 pairs from primitivos.json)')
    print('  ' + '-' * 74)

    ejes = prim_data['ejes_duales']

    # Map Spanish names to English names in signatures
    # The signatures use English names, ejes_duales uses Spanish names
    es_to_en = {
        'bien': 'good', 'mal': 'evil', 'orden': 'order', 'caos': 'chaos',
        'creación': 'creation', 'destrucción': 'destruction',
        'unión': 'union', 'separación': 'separation',
        'verdad': 'truth', 'mentira': 'lie',
        'libertad': 'freedom', 'control': 'control',
        'vida': 'life', 'muerte': 'death',
        'placer': 'pleasure', 'dolor': 'pain',
        'consciente': 'conscious', 'ausente': 'absent',
        'temporal_obs': 'mortal_observer', 'eterno_obs': 'eternal_observer',
        'individual': 'individual', 'colectivo': 'collective',
        'receptivo': 'receptive', 'creador_obs': 'creator_observer',
        'mover': 'move', 'quietud': 'stillness',
        'atracción': 'attraction', 'aversión': 'aversion',
    }

    eje_results = []
    eje_compare = []

    if args.compare:
        print('  %-22s %-22s  %6s %6s %5s  │ %6s %6s %5s' % (
            'Concept A', 'Concept B', 'Coher', 'Jaccd', 'Hamm',
            'Coher', 'Jaccd', 'Hamm'))
        print('  %-22s %-22s  %6s %6s %5s  │ %6s %6s %5s' % (
            '', '', args.run or 'current', '', '',
            args.compare, '', ''))
    else:
        print('  %-22s %-22s  %8s %8s %6s  %5s %5s' % (
            'Concept A', 'Concept B', 'Coherenc', 'Jaccard', 'Hamming',
            'Both', 'Excl'))
    print('  ' + '-' * 74)

    for pair in ejes:
        es_a, es_b = pair
        en_a = es_to_en.get(es_a, es_a)
        en_b = es_to_en.get(es_b, es_b)

        if en_a not in sigs or en_b not in sigs:
            print('  %-22s %-22s  MISSING (en_a=%s en_b=%s)' % (es_a, es_b, en_a, en_b))
            continue

        bits_a = sigs[en_a]['bits']
        bits_b = sigs[en_b]['bits']
        coh, both, excl, off = coherence(bits_a, bits_b)
        jac = jaccard(bits_a, bits_b)
        ham = hamming_distance(bits_a, bits_b)

        eje_results.append({
            'a_es': es_a, 'b_es': es_b, 'a_en': en_a, 'b_en': en_b,
            'coherence': coh, 'jaccard': jac, 'hamming': ham,
            'both': both, 'exclusive': excl,
        })

        if sigs_compare and en_a in sigs_compare and en_b in sigs_compare:
            bits_a2 = sigs_compare[en_a]['bits']
            bits_b2 = sigs_compare[en_b]['bits']
            coh2, both2, excl2, off2 = coherence(bits_a2, bits_b2)
            jac2 = jaccard(bits_a2, bits_b2)
            ham2 = hamming_distance(bits_a2, bits_b2)
            eje_compare.append({
                'a_es': es_a, 'b_es': es_b,
                'coherence': coh2, 'jaccard': jac2, 'hamming': ham2,
            })
            delta_c = coh - coh2
            print('  %-22s %-22s  %6.3f %6.3f %5d  │ %6.3f %6.3f %5d  Δ%+.3f' % (
                es_a, es_b, coh, jac, ham, coh2, jac2, ham2, delta_c))
        else:
            print('  %-22s %-22s  %8.3f %8.3f %6d  %5d %5d' % (
                es_a, es_b, coh, jac, ham, both, excl))

    # Summary
    if eje_results:
        mean_coh = sum(r['coherence'] for r in eje_results) / len(eje_results)
        mean_jac = sum(r['jaccard'] for r in eje_results) / len(eje_results)
        print('  ' + '-' * 74)
        print('  %-22s %-22s  %8.3f %8.3f' % ('MEAN', '', mean_coh, mean_jac))
        if eje_compare:
            mean_coh2 = sum(r['coherence'] for r in eje_compare) / len(eje_compare)
            print('  %-22s %-22s  %8.3f (compare)' % ('MEAN', '', mean_coh2))

    # ================================================================
    # [2] Additional structural pairs
    # ================================================================
    print()
    print('  [2] ADDITIONAL STRUCTURAL PAIRS')
    print('  ' + '-' * 74)

    extra_pairs = [
        # Capa 2 opposites
        ('más', 'menos', 'more', 'less', 'Quantity poles'),
        ('unión', 'separación', 'union', 'separation', 'Connection poles'),
        # Capa 3 opposites
        ('orden', 'caos', 'order', 'chaos', 'Structure poles'),
        ('creación', 'destrucción', 'creation', 'destruction', 'Making poles'),
        ('mover', 'quietud', 'move', 'stillness', 'Motion poles'),
        # Capa 4 modal
        ('puede', 'debe', 'can', 'must', 'Modal poles'),
        ('tal_vez', 'debe', 'maybe', 'must', 'Certainty poles'),
        # Capa 4 quantity
        ('uno', 'muchos', 'one', 'many', 'Quantity scale'),
        ('algunos', 'todo', 'some', 'all', 'Scope scale'),
        # Capa 1 fundamental
        ('vacío', 'información', 'void', 'information', 'Existence poles'),
        ('vacío', 'uno', 'void', 'one', 'Nothing/Something'),
        # Capa 5 elements
        ('fuego', 'agua', 'fire', 'water', 'Classical elements'),
        ('tierra', 'aire', 'earth', 'air', 'Classical elements'),
        # Capa 5 cognition
        ('saber', 'querer', 'know', 'want', 'Cognition/Volition'),
        ('pensar', 'decir', 'think', 'say', 'Inner/Outer'),
        # Cross-capa interesting
        ('atracción', 'decaimiento', 'attraction', 'decay', 'Build/Erode'),
        ('cooperación', 'aversión', 'cooperation', 'aversion', 'Social poles'),
        ('atención', 'intención', 'attention', 'intention', 'Passive/Active focus'),
        ('parte_de', 'contención', 'part_of', 'containment', 'In/Contains'),
        # New v4 primitives
        ('pérdida', 'atracción', 'loss', 'attraction', 'Lose/Gain'),
        ('cooperación', 'pérdida', 'cooperation', 'loss', 'Together/Lost'),
        ('intención', 'decaimiento', 'intention', 'decay', 'Purpose/Entropy'),
    ]

    print('  %-22s %-22s  %8s %8s %6s  %s' % (
        'Concept A', 'Concept B', 'Coherenc', 'Jaccard', 'Hamming', 'Category'))
    print('  ' + '-' * 74)

    extra_results = []
    for es_a, es_b, en_a, en_b, category in extra_pairs:
        if en_a not in sigs or en_b not in sigs:
            print('  %-22s %-22s  MISSING' % (es_a, es_b))
            continue

        bits_a = sigs[en_a]['bits']
        bits_b = sigs[en_b]['bits']
        coh, both, excl, off = coherence(bits_a, bits_b)
        jac = jaccard(bits_a, bits_b)
        ham = hamming_distance(bits_a, bits_b)

        extra_results.append({
            'a_es': es_a, 'b_es': es_b, 'a_en': en_a, 'b_en': en_b,
            'coherence': coh, 'jaccard': jac, 'hamming': ham, 'category': category,
        })

        # Flag if surprisingly high or low
        flag = ''
        if coh > 0.85:
            flag = ' ★'
        elif coh < 0.4:
            flag = ' ⚠'

        print('  %-22s %-22s  %8.3f %8.3f %6d  %s%s' % (
            es_a, es_b, coh, jac, ham, category, flag))

    # ================================================================
    # [3] Discovery: best anti-correlated pairs in learned signatures
    # ================================================================
    print()
    print('  [3] DISCOVERED ANTI-CORRELATED PAIRS (model-learned)')
    print('      Top %d pairs by coherence (excluding known ejes_duales)' % args.top_discovered)
    print('  ' + '-' * 74)

    # Build set of known eje pairs for exclusion
    known_pairs = set()
    for pair in ejes:
        en_a = es_to_en.get(pair[0], pair[0])
        en_b = es_to_en.get(pair[1], pair[1])
        known_pairs.add((en_a, en_b))
        known_pairs.add((en_b, en_a))

    # Compute all pairwise coherences
    all_pairs = []
    concepts = list(sigs.keys())
    for i in range(len(concepts)):
        for j in range(i + 1, len(concepts)):
            c_a, c_b = concepts[i], concepts[j]
            if (c_a, c_b) in known_pairs:
                continue
            bits_a = sigs[c_a]['bits']
            bits_b = sigs[c_b]['bits']
            coh, both, excl, off = coherence(bits_a, bits_b)
            jac = jaccard(bits_a, bits_b)
            all_pairs.append({
                'a': c_a, 'b': c_b,
                'coherence': coh, 'jaccard': jac,
                'both': both, 'exclusive': excl,
            })

    # Sort by highest coherence (most anti-correlated)
    all_pairs.sort(key=lambda x: -x['coherence'])

    # Get capa info
    capa_map = {}
    for p in prim_data['primitivos']:
        en = es_to_en.get(p['nombre'], p['nombre'])
        if en not in sigs:
            # Try direct
            for c in sigs:
                if sigs[c].get('bit') == p['bit']:
                    en = c
                    break
        capa_map[en] = p['capa']

    print('  %-20s %2s  %-20s %2s  %6s %6s  %s' % (
        'Concept A', 'C', 'Concept B', 'C', 'Coher', 'Jaccd', 'Note'))
    print('  ' + '-' * 74)

    for pair in all_pairs[:args.top_discovered]:
        ca = capa_map.get(pair['a'], '?')
        cb = capa_map.get(pair['b'], '?')
        note = ''
        if pair['coherence'] > 0.95:
            note = 'NEAR-PERFECT DUAL'
        elif pair['coherence'] > 0.85:
            note = 'strong anti-corr'
        print('  %-20s %2s  %-20s %2s  %6.3f %6.3f  %s' % (
            pair['a'], ca, pair['b'], cb,
            pair['coherence'], pair['jaccard'], note))

    # ================================================================
    # [4] Most correlated pairs (potential collapses)
    # ================================================================
    print()
    print('  [4] MOST CORRELATED PAIRS (potential collapses / near-synonyms)')
    print('  ' + '-' * 74)

    # Sort by lowest coherence (most correlated = most similar)
    all_pairs.sort(key=lambda x: x['coherence'])

    print('  %-20s %2s  %-20s %2s  %6s %6s  %s' % (
        'Concept A', 'C', 'Concept B', 'C', 'Coher', 'Jaccd', 'Note'))
    print('  ' + '-' * 74)

    for pair in all_pairs[:20]:
        ca = capa_map.get(pair['a'], '?')
        cb = capa_map.get(pair['b'], '?')
        note = ''
        if pair['jaccard'] > 0.90:
            note = 'NEAR-COLLAPSE'
        elif pair['jaccard'] > 0.80:
            note = 'very similar'
        elif pair['jaccard'] > 0.70:
            note = 'similar'
        print('  %-20s %2s  %-20s %2s  %6.3f %6.3f  %s' % (
            pair['a'], ca, pair['b'], cb,
            pair['coherence'], pair['jaccard'], note))

    # ================================================================
    # [5] Summary statistics
    # ================================================================
    print()
    print('  [5] SUMMARY')
    print('  ' + '-' * 74)

    if eje_results:
        cohs = [r['coherence'] for r in eje_results]
        jacs = [r['jaccard'] for r in eje_results]
        print('  Ejes duales (14 pairs):')
        print('    Mean coherence: %.3f' % (sum(cohs) / len(cohs)))
        print('    Mean Jaccard:   %.3f' % (sum(jacs) / len(jacs)))
        print('    Perfect (>0.95): %d/%d' % (sum(1 for c in cohs if c > 0.95), len(cohs)))
        print('    Good (>0.80):    %d/%d' % (sum(1 for c in cohs if c > 0.80), len(cohs)))
        print('    Weak (<0.60):    %d/%d' % (sum(1 for c in cohs if c < 0.60), len(cohs)))
        print()
        print('    Worst:  %s/%s = %.3f' % (
            min(eje_results, key=lambda r: r['coherence'])['a_es'],
            min(eje_results, key=lambda r: r['coherence'])['b_es'],
            min(cohs)))
        print('    Best:   %s/%s = %.3f' % (
            max(eje_results, key=lambda r: r['coherence'])['a_es'],
            max(eje_results, key=lambda r: r['coherence'])['b_es'],
            max(cohs)))

    # ================================================================
    # Save
    # ================================================================
    os.makedirs(RESULTS_DIR, exist_ok=True)
    out = {
        'run': args.run or 'current',
        'ejes_duales': eje_results,
        'extra_pairs': extra_results,
        'top_anti_correlated': all_pairs[:args.top_discovered] if all_pairs else [],
        'top_correlated': sorted(all_pairs, key=lambda x: x['coherence'])[:20] if all_pairs else [],
    }
    out_path = os.path.join(RESULTS_DIR, 'audit_all_duals.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print()
    print('=' * 78)
    print('  Saved: %s' % out_path)
    print('=' * 78)


if __name__ == '__main__':
    main()
