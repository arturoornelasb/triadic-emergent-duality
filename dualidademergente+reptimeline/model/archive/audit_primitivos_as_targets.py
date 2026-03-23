"""
Analyze: What would the target signatures look like if we train
directly with the 65 primitivos instead of 262 domain anchors?

Each primitivo's target = its own bit ON + all transitive deps ON + rest OFF.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))
RESULTS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'neural', 'results'))


def load_primitivos():
    path = os.path.join(DATA_DIR, 'primitivos.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def build_name_to_bit(prims):
    return {p['nombre']: p['bit'] for p in prims}


def expand_deps_recursive(prim_name, prims_by_name, visited=None):
    """Get all transitive dependencies for a primitivo."""
    if visited is None:
        visited = set()
    if prim_name in visited:
        return set()
    visited.add(prim_name)

    p = prims_by_name.get(prim_name)
    if not p:
        return set()

    result = set()
    for dep_name in p.get('deps', []):
        result.add(dep_name)
        result |= expand_deps_recursive(dep_name, prims_by_name, visited)
    return result


def jaccard(a, b):
    sa, sb = set(a), set(b)
    u = sa | sb
    return len(sa & sb) / len(u) if u else 0.0


def main():
    data = load_primitivos()
    prims = data['primitivos']

    # Build lookup
    prims_by_name = {p['nombre']: p for p in prims}
    name_to_bit = build_name_to_bit(prims)

    print('=' * 70)
    print('  ANALYSIS: 65 PRIMITIVOS AS DIRECT TARGETS')
    print('=' * 70)

    # ---- Compute target signatures ----
    targets = {}
    for p in prims:
        name = p['nombre']
        bit = p['bit']
        capa = p['capa']

        # Own bit + all transitive deps
        all_deps = expand_deps_recursive(name, prims_by_name)
        active_bits = {bit}  # own bit
        for dep_name in all_deps:
            if dep_name in name_to_bit:
                active_bits.add(name_to_bit[dep_name])

        # Build 65-bit signature
        sig = [0] * 65
        for b in active_bits:
            if b < 65:
                sig[b] = 1

        targets[name] = {
            'bit': bit,
            'capa': capa,
            'n_active': sum(sig),
            'active_bits': sorted(active_bits),
            'n_deps': len(all_deps),
            'deps': sorted(all_deps),
            'signature': sig,
            'dual': p.get('dual', None),
        }

    # ---- Uniqueness ----
    sig_tuples = {}
    for name, info in targets.items():
        t = tuple(info['signature'])
        if t not in sig_tuples:
            sig_tuples[t] = []
        sig_tuples[t].append(name)

    n_unique = sum(1 for v in sig_tuples.values() if len(v) == 1)
    collisions = [v for v in sig_tuples.values() if len(v) > 1]

    print()
    print('  [1] UNIQUENESS')
    print('  Unique target signatures: %d / 65 (%.1f%%)' % (n_unique, n_unique / 65 * 100))
    if collisions:
        print('  Collision groups: %d' % len(collisions))
        for group in collisions:
            print('    %s' % group)
    else:
        print('  NO COLLISIONS — every primitivo has a unique target!')

    # ---- Active bits distribution ----
    print()
    print('  [2] ACTIVE BITS PER PRIMITIVO')
    by_capa = {}
    for name, info in targets.items():
        c = info['capa']
        if c not in by_capa:
            by_capa[c] = []
        by_capa[c].append((name, info))

    for capa in sorted(by_capa.keys()):
        items = by_capa[capa]
        counts = [info['n_active'] for _, info in items]
        print()
        print('  Capa %d — %s (%d primitivos, active bits: %d-%d)' % (
            capa, data['capas'][str(capa)]['nombre'], len(items),
            min(counts), max(counts)))
        for name, info in sorted(items, key=lambda x: x[1]['bit']):
            dual = ' (dual: %s)' % info['dual'] if info['dual'] else ''
            deps_str = ', '.join(info['deps'][:5])
            if len(info['deps']) > 5:
                deps_str += '...'
            print('    bit %2d %-20s %2d bits active  deps=[%s]%s' % (
                info['bit'], name, info['n_active'], deps_str, dual))

    # ---- Per-bit activation rate ----
    print()
    print('  [3] PER-BIT ACTIVATION RATE (across 65 targets)')
    bit_rates = []
    for bit in range(65):
        active = sum(1 for info in targets.values() if info['signature'][bit] == 1)
        rate = active / 65
        bit_rates.append(rate)

    always_on = [(i, rate) for i, rate in enumerate(bit_rates) if rate > 0.95]
    always_off = [(i, rate) for i, rate in enumerate(bit_rates) if rate < 0.05]
    discriminative = [(i, rate) for i, rate in enumerate(bit_rates) if 0.05 <= rate <= 0.95]

    print('  Always ON (>95%%):  %d' % len(always_on))
    for bit, rate in always_on:
        name = [p['nombre'] for p in prims if p['bit'] == bit]
        print('    bit %2d %-20s rate=%.3f' % (bit, name[0] if name else '?', rate))
    print('  Always OFF (<5%%): %d' % len(always_off))
    for bit, rate in always_off:
        name = [p['nombre'] for p in prims if p['bit'] == bit]
        print('    bit %2d %-20s rate=%.3f' % (bit, name[0] if name else '?', rate))
    print('  Discriminative (5-95%%): %d / 65' % len(discriminative))

    # ---- Pairwise Jaccard ----
    print()
    print('  [4] PAIRWISE JACCARD DISTRIBUTION')
    all_jaccards = []
    names = list(targets.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            j_sim = jaccard(targets[names[i]]['active_bits'],
                            targets[names[j]]['active_bits'])
            all_jaccards.append(j_sim)

    all_jaccards.sort()
    n_pairs = len(all_jaccards)
    print('  Total pairs: %d' % n_pairs)
    print('  Min=%.3f  P25=%.3f  Median=%.3f  P75=%.3f  Max=%.3f  Mean=%.3f' % (
        all_jaccards[0],
        all_jaccards[n_pairs // 4],
        all_jaccards[n_pairs // 2],
        all_jaccards[3 * n_pairs // 4],
        all_jaccards[-1],
        sum(all_jaccards) / n_pairs))

    for t in [0.90, 0.95, 1.00]:
        count = sum(1 for j in all_jaccards if j >= t)
        print('  Pairs with J >= %.2f: %d (%.1f%%)' % (t, count, count / n_pairs * 100))

    # ---- Dual pair analysis ----
    print()
    print('  [5] DUAL PAIRS — Target Hamming Distance')
    ejes = data['ejes_duales']
    for pair in ejes:
        a_name, b_name = pair[0], pair[1]
        if a_name in targets and b_name in targets:
            a_sig = targets[a_name]['signature']
            b_sig = targets[b_name]['signature']
            hamming = sum(x != y for x, y in zip(a_sig, b_sig))
            j_sim = jaccard(targets[a_name]['active_bits'], targets[b_name]['active_bits'])
            print('    %-20s <-> %-20s hamming=%d  jaccard=%.3f  bits_a=%d  bits_b=%d' % (
                a_name, b_name, hamming, j_sim,
                targets[a_name]['n_active'], targets[b_name]['n_active']))

    # ---- Comparison with v2 targets ----
    print()
    print('  [6] COMPARISON WITH V2 (262 anchors)')
    print('    V2: 10 unique / 262 targets (3.8%%),  21 always-on bits,  31 discriminative')
    print('    V3: %d unique / 65 targets (%.1f%%),  %d always-on bits,  %d discriminative' % (
        n_unique, n_unique / 65 * 100, len(always_on), len(discriminative)))
    print()
    v2_median_j = 0.667  # from audit_targets.json
    v3_median_j = all_jaccards[n_pairs // 2]
    print('    V2 Jaccard median: %.3f' % v2_median_j)
    print('    V3 Jaccard median: %.3f' % v3_median_j)
    print('    Improvement: %+.3f' % (v3_median_j - v2_median_j))

    # ---- Language consideration ----
    print()
    print('  [7] GPT-2 LANGUAGE NOTE')
    print('  The 65 primitivos are Spanish words. GPT-2 was trained on English.')
    print('  Options for v3:')
    print('    A) Use Spanish words directly (GPT-2 has some Spanish)')
    print('    B) Use English translations as context')
    print('    C) Use definitions as multi-word context')
    print('  Recommend: B or C — pass English definitions to GPT-2,')
    print('  map to primitivo targets via the DAG.')

    # ---- Save ----
    os.makedirs(RESULTS_DIR, exist_ok=True)
    results = {
        'n_primitivos': 65,
        'n_unique': n_unique,
        'unique_pct': round(n_unique / 65 * 100, 1),
        'n_collisions': len(collisions),
        'n_always_on': len(always_on),
        'n_discriminative': len(discriminative),
        'jaccard_median': v3_median_j,
        'targets': {
            name: {
                'bit': info['bit'],
                'capa': info['capa'],
                'n_active': info['n_active'],
                'active_bits': info['active_bits'],
                'signature': info['signature'],
                'dual': info['dual'],
            }
            for name, info in targets.items()
        },
        'per_bit_rates': [round(r, 4) for r in bit_rates],
    }

    out_path = os.path.join(RESULTS_DIR, 'audit_primitivos_targets.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print()
    print('=' * 70)
    print('  Saved: %s' % out_path)
    print('=' * 70)


if __name__ == '__main__':
    main()
