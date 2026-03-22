"""
Audit: Compare what we ASKED the model to learn (gold targets)
vs what the model ACTUALLY learned (exploration signatures).

Per-concept, per-domain, per-bit accuracy.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'neural', 'results'))


def main():
    # Load gold targets
    gold_path = os.path.join(SCRIPT_DIR, 'gold_primes_65.json')
    with open(gold_path, 'r', encoding='utf-8') as f:
        gold = json.load(f)

    # Load learned signatures
    exp_path = os.path.join(RESULTS_DIR, 'exploration.json')
    with open(exp_path, 'r', encoding='utf-8') as f:
        exp = json.load(f)

    learned = exp['signatures']

    # Load primitivo names
    prim_path = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data', 'primitivos.json'))
    prim_names = {}
    if os.path.exists(prim_path):
        with open(prim_path, 'r', encoding='utf-8') as f:
            pdata = json.load(f)
        for p in pdata['primitivos']:
            prim_names[p['bit']] = p['nombre']

    print('=' * 70)
    print('  AUDIT: LEARNED vs TARGET SIGNATURES')
    print('=' * 70)

    concepts = [c for c in gold.keys() if c in learned]
    print('  Concepts with both target and learned: %d' % len(concepts))

    # ---- Per-concept accuracy ----
    per_concept = {}
    for c in concepts:
        target = gold[c]['binary_signature']
        actual = learned[c]['bits']
        n_correct = sum(t == a for t, a in zip(target, actual))
        n_wrong = 65 - n_correct
        wrong_bits = []
        for i in range(65):
            if target[i] != actual[i]:
                wrong_bits.append({
                    'bit': i,
                    'name': prim_names.get(i, '?'),
                    'target': target[i],
                    'actual': actual[i],
                })
        per_concept[c] = {
            'domain': gold[c]['domain'],
            'accuracy': n_correct / 65,
            'n_wrong': n_wrong,
            'wrong_bits': wrong_bits,
        }

    # ---- Per-domain summary ----
    print()
    print('  [1] PER-DOMAIN ACCURACY')
    domains = {}
    for c, info in per_concept.items():
        d = info['domain']
        if d not in domains:
            domains[d] = []
        domains[d].append(info)

    for dom in sorted(domains.keys()):
        infos = domains[dom]
        accs = [i['accuracy'] for i in infos]
        mean_acc = sum(accs) / len(accs)
        min_acc = min(accs)
        max_acc = max(accs)
        perfect = sum(1 for a in accs if a == 1.0)
        print('    %-15s mean=%.3f  min=%.3f  max=%.3f  perfect=%d/%d' % (
            dom, mean_acc, min_acc, max_acc, perfect, len(accs)))

    # ---- Overall stats ----
    all_accs = [info['accuracy'] for info in per_concept.values()]
    all_accs.sort()
    print()
    print('  [2] OVERALL ACCURACY')
    print('    Mean: %.4f' % (sum(all_accs) / len(all_accs)))
    print('    Median: %.4f' % all_accs[len(all_accs) // 2])
    print('    Min: %.4f (%s)' % (all_accs[0],
        [c for c, i in per_concept.items() if i['accuracy'] == all_accs[0]][0]))
    print('    Perfect (100%%): %d / %d' % (
        sum(1 for a in all_accs if a == 1.0), len(all_accs)))
    print('    >= 95%%: %d / %d' % (
        sum(1 for a in all_accs if a >= 0.95), len(all_accs)))
    print('    >= 90%%: %d / %d' % (
        sum(1 for a in all_accs if a >= 0.90), len(all_accs)))

    # ---- Worst concepts ----
    print()
    print('  [3] WORST 20 CONCEPTS')
    worst = sorted(per_concept.items(), key=lambda x: x[1]['accuracy'])
    for c, info in worst[:20]:
        wrong_names = [w['name'] for w in info['wrong_bits'][:5]]
        print('    %-20s (%s) acc=%.3f  wrong=%d  bits: %s' % (
            c, info['domain'][:4], info['accuracy'], info['n_wrong'],
            wrong_names))

    # ---- Per-bit accuracy ----
    print()
    print('  [4] PER-BIT ACCURACY (which primitivos does model get wrong?)')
    bit_correct = [0] * 65
    bit_total = [0] * 65
    bit_false_pos = [0] * 65  # target=0, actual=1
    bit_false_neg = [0] * 65  # target=1, actual=0

    for c in concepts:
        target = gold[c]['binary_signature']
        actual = learned[c]['bits']
        for i in range(65):
            bit_total[i] += 1
            if target[i] == actual[i]:
                bit_correct[i] += 1
            elif target[i] == 0 and actual[i] == 1:
                bit_false_pos[i] += 1
            else:
                bit_false_neg[i] += 1

    bit_accs = [(i, bit_correct[i] / bit_total[i], bit_false_pos[i], bit_false_neg[i])
                for i in range(65)]
    bit_accs.sort(key=lambda x: x[1])

    print('  Worst bits (lowest accuracy):')
    for bit, acc, fp, fn in bit_accs[:20]:
        name = prim_names.get(bit, '?')
        print('    bit %2d %-20s acc=%.3f  false_pos=%d  false_neg=%d' % (
            bit, name, acc, fp, fn))

    print()
    print('  Best bits (perfect or near):')
    for bit, acc, fp, fn in bit_accs[-10:]:
        name = prim_names.get(bit, '?')
        print('    bit %2d %-20s acc=%.3f  false_pos=%d  false_neg=%d' % (
            bit, name, acc, fp, fn))

    # ---- Unique signatures in learned vs target ----
    print()
    print('  [5] UNIQUENESS COMPARISON')
    target_sigs = set()
    learned_sigs = set()
    for c in concepts:
        target_sigs.add(tuple(gold[c]['binary_signature']))
        learned_sigs.add(tuple(learned[c]['bits']))
    print('    Unique target signatures:  %d' % len(target_sigs))
    print('    Unique learned signatures: %d' % len(learned_sigs))
    print('    Model created %d MORE unique signatures than targets asked for' % (
        len(learned_sigs) - len(target_sigs)))

    # ---- Save ----
    os.makedirs(RESULTS_DIR, exist_ok=True)
    results = {
        'n_concepts': len(concepts),
        'overall_accuracy': round(sum(all_accs) / len(all_accs), 4),
        'per_domain': {},
        'per_concept': {},
        'per_bit_accuracy': [round(bit_correct[i] / bit_total[i], 4) for i in range(65)],
        'per_bit_false_pos': bit_false_pos,
        'per_bit_false_neg': bit_false_neg,
        'unique_targets': len(target_sigs),
        'unique_learned': len(learned_sigs),
    }

    for dom in sorted(domains.keys()):
        infos = domains[dom]
        accs = [i['accuracy'] for i in infos]
        results['per_domain'][dom] = {
            'mean_accuracy': round(sum(accs) / len(accs), 4),
            'min_accuracy': round(min(accs), 4),
            'n_perfect': sum(1 for a in accs if a == 1.0),
        }

    for c, info in per_concept.items():
        results['per_concept'][c] = {
            'domain': info['domain'],
            'accuracy': round(info['accuracy'], 4),
            'n_wrong': info['n_wrong'],
            'wrong_bits': [w['bit'] for w in info['wrong_bits']],
        }

    out_path = os.path.join(RESULTS_DIR, 'audit_learned_vs_target.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print()
    print('=' * 70)
    print('  Saved: %s' % out_path)
    print('=' * 70)


if __name__ == '__main__':
    main()
