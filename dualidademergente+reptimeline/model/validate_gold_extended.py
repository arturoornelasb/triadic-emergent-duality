"""
Validate gold_extended_v6.json before training.

Checks:
  1. Original 72 primitivos have unchanged signatures
  2. Unique signature percentage > 80%
  3. No bit activated in >95% or <2% of all entries (warning only)
  4. Mean Jaccard distance within each domain > 0.05
  5. Cross-domain signature means differ
  6. All entries have required fields
  7. No empty signatures (all zeros)
"""

import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def jaccard_distance(a, b):
    """Jaccard distance between two binary lists."""
    intersection = sum(x and y for x, y in zip(a, b))
    union = sum(x or y for x, y in zip(a, b))
    if union == 0:
        return 1.0
    return 1.0 - intersection / union


def main():
    print('=' * 70)
    print('  VALIDATING gold_extended_v6.json')
    print('=' * 70)

    # Load extended gold
    ext_path = os.path.join(SCRIPT_DIR, 'gold_extended_v6.json')
    with open(ext_path, 'r', encoding='utf-8') as f:
        extended = json.load(f)

    # Load original gold
    orig_path = os.path.join(SCRIPT_DIR, 'gold_primitivos_72.json')
    with open(orig_path, 'r', encoding='utf-8') as f:
        original = json.load(f)

    passed = 0
    failed = 0
    warnings = 0

    # --- Check 1: Original signatures unchanged ---
    print('\n  [1] Original primitivo signatures unchanged')
    mismatches = []
    for key, orig_entry in original.items():
        if key not in extended:
            mismatches.append(f'    MISSING: {key}')
            continue
        ext_sig = extended[key]['binary_signature']
        orig_sig = orig_entry['binary_signature']
        if ext_sig != orig_sig:
            mismatches.append(f'    CHANGED: {key}')

    if mismatches:
        print(f'    FAIL: {len(mismatches)} mismatches')
        for m in mismatches[:5]:
            print(m)
        failed += 1
    else:
        print(f'    PASS: all {len(original)} primitivos match exactly')
        passed += 1

    # --- Check 2: Unique signatures > 80% ---
    print('\n  [2] Unique signature percentage > 80%')
    sigs = [tuple(v['binary_signature']) for v in extended.values()]
    unique_pct = 100 * len(set(sigs)) / len(sigs)
    if unique_pct >= 80:
        print(f'    PASS: {unique_pct:.1f}% unique ({len(set(sigs))}/{len(sigs)})')
        passed += 1
    else:
        print(f'    FAIL: {unique_pct:.1f}% unique ({len(set(sigs))}/{len(sigs)})')
        failed += 1

    # --- Check 3: Bit activation range ---
    print('\n  [3] Bit activation distribution')
    n_bits = 72
    bit_counts = [0] * n_bits
    for v in extended.values():
        for i, b in enumerate(v['binary_signature']):
            bit_counts[i] += b
    n_entries = len(extended)

    always_on = []
    dead = []
    for i, c in enumerate(bit_counts):
        rate = c / n_entries
        if rate >= 0.95:
            always_on.append((i, rate))
        elif rate <= 0.02:
            dead.append((i, rate))

    if always_on:
        print(f'    WARN: {len(always_on)} always-ON bits (>=95%):')
        for bit, rate in always_on:
            print(f'      bit {bit}: {rate:.3f}')
        warnings += 1
    else:
        print('    PASS: no always-ON bits')
        passed += 1

    if dead:
        print(f'    WARN: {len(dead)} dead bits (<=2%):')
        for bit, rate in dead:
            print(f'      bit {bit}: {rate:.3f}')
        warnings += 1
    else:
        print('    PASS: no dead bits')
        passed += 1

    # --- Check 4: Intra-domain Jaccard diversity ---
    print('\n  [4] Intra-domain Jaccard distance > 0.05')
    domains = {}
    for v in extended.values():
        d = v.get('source_domain', 'primitivo')
        if d not in domains:
            domains[d] = []
        domains[d].append(v['binary_signature'])

    low_diversity = []
    for d in sorted(domains.keys()):
        sigs_d = domains[d]
        if len(sigs_d) < 2:
            continue
        # Sample pairwise distances (max 500 pairs)
        import random
        random.seed(42)
        n = len(sigs_d)
        pairs = min(500, n * (n - 1) // 2)
        total_dist = 0
        for _ in range(pairs):
            i, j = random.sample(range(n), 2)
            total_dist += jaccard_distance(sigs_d[i], sigs_d[j])
        mean_dist = total_dist / pairs
        status = 'OK' if mean_dist > 0.05 else 'LOW'
        if status == 'LOW':
            low_diversity.append(d)
        print(f'    {d}: mean Jaccard = {mean_dist:.3f} [{status}]')

    if low_diversity:
        print(f'    FAIL: {len(low_diversity)} domains with low diversity')
        failed += 1
    else:
        print('    PASS: all domains have sufficient diversity')
        passed += 1

    # --- Check 5: Cross-domain separation ---
    print('\n  [5] Cross-domain mean signatures differ')
    domain_means = {}
    for d, sigs_d in domains.items():
        if d == 'primitivo':
            continue
        mean_sig = [sum(s[i] for s in sigs_d) / len(sigs_d) for i in range(n_bits)]
        domain_means[d] = mean_sig

    if len(domain_means) >= 2:
        domain_names = sorted(domain_means.keys())
        cross_dists = []
        for i, d1 in enumerate(domain_names):
            for d2 in domain_names[i+1:]:
                dist = sum(abs(a - b) for a, b in zip(domain_means[d1], domain_means[d2])) / n_bits
                cross_dists.append(dist)
        mean_cross = sum(cross_dists) / len(cross_dists)
        min_cross = min(cross_dists)
        print(f'    Mean L1 distance between domain means: {mean_cross:.3f}')
        print(f'    Min L1 distance: {min_cross:.3f}')
        if min_cross > 0.01:
            print('    PASS: domains are distinguishable')
            passed += 1
        else:
            print('    FAIL: some domains are indistinguishable')
            failed += 1
    else:
        print('    SKIP: not enough domains')

    # --- Check 6: Required fields ---
    print('\n  [6] Required fields present')
    required = ['binary_signature', 'text', 'n_active']
    missing_fields = 0
    for key, v in extended.items():
        for field in required:
            if field not in v:
                missing_fields += 1
                if missing_fields <= 3:
                    print(f'    {key} missing {field}')
    if missing_fields:
        print(f'    FAIL: {missing_fields} missing fields')
        failed += 1
    else:
        print(f'    PASS: all {len(extended)} entries have required fields')
        passed += 1

    # --- Check 7: No empty signatures ---
    print('\n  [7] No all-zero signatures')
    empty = [k for k, v in extended.items() if sum(v['binary_signature']) == 0]
    if empty:
        print(f'    FAIL: {len(empty)} entries with all-zero signatures')
        for e in empty[:5]:
            print(f'      {e}')
        failed += 1
    else:
        print(f'    PASS: no empty signatures')
        passed += 1

    # --- Summary ---
    print(f'\n{"=" * 70}')
    print(f'  RESULT: {passed} passed, {failed} failed, {warnings} warnings')
    if failed == 0:
        print('  STATUS: READY FOR TRAINING')
    else:
        print('  STATUS: FIX ISSUES BEFORE TRAINING')
    print('=' * 70)

    return failed == 0


if __name__ == '__main__':
    ok = main()
    sys.exit(0 if ok else 1)
