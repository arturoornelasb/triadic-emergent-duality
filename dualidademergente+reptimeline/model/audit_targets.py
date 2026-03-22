"""
Audit: Are the TARGET signatures in gold_primes_65.json diverse enough?

If targets themselves are too similar, no training will fix it.
This script checks the gold signatures BEFORE any model is involved.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json
import math

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'neural', 'results'))


def jaccard(a, b):
    sa, sb = set(a), set(b)
    u = sa | sb
    return len(sa & sb) / len(u) if u else 0.0


def hamming(sig_a, sig_b):
    return sum(a != b for a, b in zip(sig_a, sig_b))


def main():
    gold_path = os.path.join(SCRIPT_DIR, 'gold_primes_65.json')
    with open(gold_path, 'r', encoding='utf-8') as f:
        gold = json.load(f)

    concepts = list(gold.keys())
    n = len(concepts)

    print('=' * 70)
    print('  AUDIT: TARGET SIGNATURE DIVERSITY')
    print('  Source: gold_primes_65.json (%d concepts)' % n)
    print('=' * 70)

    # ---- Per-concept stats ----
    sigs = {}
    for c in concepts:
        bits = gold[c]['binary_signature']
        active = [i for i, v in enumerate(bits) if v == 1]
        sigs[c] = {
            'bits': bits,
            'active': active,
            'n_active': len(active),
            'domain': gold[c]['domain'],
        }

    # ---- Uniqueness ----
    sig_tuples = {}
    for c in concepts:
        t = tuple(sigs[c]['bits'])
        if t not in sig_tuples:
            sig_tuples[t] = []
        sig_tuples[t].append(c)

    n_unique = sum(1 for v in sig_tuples.values() if len(v) == 1)
    collisions = {k: v for k, v in sig_tuples.items() if len(v) > 1}

    print()
    print('  [1] UNIQUENESS')
    print('  Unique target signatures: %d / %d (%.1f%%)' % (
        n_unique, n, n_unique / n * 100))
    print('  Collision groups: %d' % len(collisions))
    if collisions:
        for group in sorted(collisions.values(), key=lambda x: -len(x)):
            doms = [sigs[c]['domain'] for c in group]
            print('    %s  domains=%s' % (group, list(set(doms))))

    # ---- Active bits distribution ----
    print()
    print('  [2] ACTIVE BITS DISTRIBUTION')
    active_counts = [sigs[c]['n_active'] for c in concepts]
    print('  Min: %d  Max: %d  Mean: %.1f  Median: %d' % (
        min(active_counts), max(active_counts),
        sum(active_counts) / len(active_counts),
        sorted(active_counts)[len(active_counts) // 2]))

    # Per domain
    domains = {}
    for c in concepts:
        d = sigs[c]['domain']
        if d not in domains:
            domains[d] = []
        domains[d].append(c)

    for dom in sorted(domains.keys()):
        cs = domains[dom]
        counts = [sigs[c]['n_active'] for c in cs]
        print('    %s: n=%d  active_bits=[%d-%d] mean=%.1f' % (
            dom, len(cs), min(counts), max(counts),
            sum(counts) / len(counts)))

    # ---- Per-bit activation rate in TARGETS ----
    print()
    print('  [3] PER-BIT ACTIVATION IN TARGETS')
    bit_rates = []
    for bit in range(65):
        active = sum(1 for c in concepts if sigs[c]['bits'][bit] == 1)
        rate = active / n
        bit_rates.append(rate)

    # Load primitivo names
    prim_path = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data', 'primitivos.json'))
    prim_names = {}
    if os.path.exists(prim_path):
        with open(prim_path, 'r', encoding='utf-8') as f:
            pdata = json.load(f)
        for p in pdata['primitivos']:
            prim_names[p['bit']] = p['nombre']

    always_on = []
    always_off = []
    low_var = []
    for bit in range(65):
        name = prim_names.get(bit, '?')
        r = bit_rates[bit]
        if r > 0.95:
            always_on.append((bit, name, r))
        elif r < 0.05:
            always_off.append((bit, name, r))
        elif r > 0.85 or r < 0.15:
            low_var.append((bit, name, r))

    print('  Always ON (>95%%):  %d bits' % len(always_on))
    for bit, name, r in always_on:
        print('    bit %2d %-20s rate=%.3f' % (bit, name, r))
    print('  Always OFF (<5%%): %d bits' % len(always_off))
    for bit, name, r in always_off:
        print('    bit %2d %-20s rate=%.3f' % (bit, name, r))
    print('  Low variance (85-95%% or 5-15%%): %d bits' % len(low_var))
    for bit, name, r in low_var:
        print('    bit %2d %-20s rate=%.3f' % (bit, name, r))

    good = [i for i in range(65) if 0.15 <= bit_rates[i] <= 0.85]
    print('  Discriminative bits (15-85%%): %d / 65' % len(good))

    # ---- Pairwise Jaccard distribution ----
    print()
    print('  [4] PAIRWISE JACCARD (target vs target)')
    all_jaccards = []
    within_jaccards = {}
    between_jaccards = []

    for i in range(n):
        for j in range(i + 1, n):
            c1, c2 = concepts[i], concepts[j]
            j_sim = jaccard(sigs[c1]['active'], sigs[c2]['active'])
            all_jaccards.append(j_sim)
            d1, d2 = sigs[c1]['domain'], sigs[c2]['domain']
            if d1 == d2:
                if d1 not in within_jaccards:
                    within_jaccards[d1] = []
                within_jaccards[d1].append(j_sim)
            else:
                between_jaccards.append(j_sim)

    all_jaccards.sort()
    print('  Total pairs: %d' % len(all_jaccards))
    print('  Jaccard distribution:')
    print('    Min=%.3f  P25=%.3f  Median=%.3f  P75=%.3f  Max=%.3f  Mean=%.3f' % (
        all_jaccards[0],
        all_jaccards[len(all_jaccards) // 4],
        all_jaccards[len(all_jaccards) // 2],
        all_jaccards[3 * len(all_jaccards) // 4],
        all_jaccards[-1],
        sum(all_jaccards) / len(all_jaccards)))

    # Count high-similarity pairs
    thresholds = [0.90, 0.95, 1.00]
    for t in thresholds:
        count = sum(1 for j in all_jaccards if j >= t)
        print('    Pairs with J >= %.2f: %d (%.1f%%)' % (t, count, count / len(all_jaccards) * 100))

    # Within vs between
    print()
    print('  [5] WITHIN-DOMAIN vs BETWEEN-DOMAIN (targets)')
    between_mean = sum(between_jaccards) / len(between_jaccards) if between_jaccards else 0
    print('    Between-domain mean Jaccard: %.3f (n=%d)' % (between_mean, len(between_jaccards)))
    for dom in sorted(within_jaccards.keys()):
        js = within_jaccards[dom]
        wmean = sum(js) / len(js)
        identical = sum(1 for j in js if j >= 1.0)
        near = sum(1 for j in js if j >= 0.95)
        print('    %-15s within=%.3f  sep=%.3f  identical=%d  near_identical(>=.95)=%d' % (
            dom, wmean, wmean / between_mean if between_mean else 0,
            identical, near))

    # ---- Hamming distances ----
    print()
    print('  [6] HAMMING DISTANCES (target vs target)')
    all_hamming = []
    for i in range(n):
        for j in range(i + 1, n):
            h = hamming(sigs[concepts[i]]['bits'], sigs[concepts[j]]['bits'])
            all_hamming.append(h)
    all_hamming.sort()
    print('  Min=%d  Median=%d  Mean=%.1f  Max=%d' % (
        all_hamming[0], all_hamming[len(all_hamming) // 2],
        sum(all_hamming) / len(all_hamming), all_hamming[-1]))
    zero_hamming = sum(1 for h in all_hamming if h == 0)
    one_hamming = sum(1 for h in all_hamming if h <= 1)
    two_hamming = sum(1 for h in all_hamming if h <= 2)
    print('  Hamming=0 (identical): %d pairs' % zero_hamming)
    print('  Hamming<=1: %d pairs' % one_hamming)
    print('  Hamming<=2: %d pairs' % two_hamming)

    # ---- Domain base signature analysis ----
    print()
    print('  [7] DOMAIN BASE SIGNATURES')
    print('  (Bits shared by ALL concepts in a domain)')
    for dom in sorted(domains.keys()):
        cs = domains[dom]
        # Find bits that are 1 in ALL concepts of this domain
        base_bits = []
        for bit in range(65):
            if all(sigs[c]['bits'][bit] == 1 for c in cs):
                base_bits.append(bit)
        # Find bits that are 0 in ALL concepts
        zero_bits = []
        for bit in range(65):
            if all(sigs[c]['bits'][bit] == 0 for c in cs):
                zero_bits.append(bit)
        variable = 65 - len(base_bits) - len(zero_bits)
        base_names = [prim_names.get(b, '?') for b in base_bits[:10]]
        print('    %-15s base=%d bits  zero=%d bits  variable=%d bits' % (
            dom, len(base_bits), len(zero_bits), variable))
        print('      base: %s%s' % (base_names, '...' if len(base_bits) > 10 else ''))

    # ---- Save results ----
    os.makedirs(RESULTS_DIR, exist_ok=True)
    results = {
        'n_concepts': n,
        'n_unique_targets': n_unique,
        'unique_pct': round(n_unique / n * 100, 1),
        'n_collision_groups': len(collisions),
        'collision_groups': [v for v in collisions.values()],
        'bits_always_on': [(b, n) for b, n, r in always_on],
        'bits_always_off': [(b, n) for b, n, r in always_off],
        'n_discriminative_bits': len(good),
        'jaccard_stats': {
            'min': round(all_jaccards[0], 4),
            'p25': round(all_jaccards[len(all_jaccards) // 4], 4),
            'median': round(all_jaccards[len(all_jaccards) // 2], 4),
            'p75': round(all_jaccards[3 * len(all_jaccards) // 4], 4),
            'max': round(all_jaccards[-1], 4),
            'mean': round(sum(all_jaccards) / len(all_jaccards), 4),
        },
        'hamming_stats': {
            'min': all_hamming[0],
            'median': all_hamming[len(all_hamming) // 2],
            'mean': round(sum(all_hamming) / len(all_hamming), 1),
            'max': all_hamming[-1],
            'identical_pairs': zero_hamming,
        },
        'per_bit_rates': [round(r, 4) for r in bit_rates],
        'per_domain': {},
    }
    for dom in sorted(domains.keys()):
        cs = domains[dom]
        js = within_jaccards.get(dom, [])
        results['per_domain'][dom] = {
            'n': len(cs),
            'mean_active_bits': round(sum(sigs[c]['n_active'] for c in cs) / len(cs), 1),
            'within_jaccard': round(sum(js) / len(js), 4) if js else 0,
        }

    out_path = os.path.join(RESULTS_DIR, 'audit_targets.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print()
    print('=' * 70)
    print('  Saved: %s' % out_path)
    print('=' * 70)


if __name__ == '__main__':
    main()
