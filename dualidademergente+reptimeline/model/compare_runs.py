"""
Compare two training runs side by side.

Usage:
    python compare_runs.py v2 v3
    python compare_runs.py v2 v3 --output comparison_v2_v3.txt
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RUNS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'runs'))


def load_manifest(run_id):
    path = os.path.join(RUNS_DIR, run_id, 'manifest.json')
    if not os.path.exists(path):
        print('ERROR: manifest.json not found for run %s at %s' % (run_id, path))
        sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def delta(a, b, fmt='%.4f', higher_is_better=True):
    if a is None or b is None:
        return '?'
    d = b - a
    sign = '+' if d > 0 else ''
    indicator = ''
    if d != 0:
        if higher_is_better:
            indicator = ' BETTER' if d > 0 else ' WORSE'
        else:
            indicator = ' BETTER' if d < 0 else ' WORSE'
    return (fmt % d).replace('+', sign) + indicator


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('run_a', help='First run ID (baseline)')
    parser.add_argument('run_b', help='Second run ID (new)')
    parser.add_argument('--output', default=None, help='Save comparison to file')
    args = parser.parse_args()

    a = load_manifest(args.run_a)
    b = load_manifest(args.run_b)

    lines = []

    def out(s=''):
        lines.append(s)
        print(s)

    out('=' * 78)
    out('  RUN COMPARISON: %s vs %s' % (args.run_a, args.run_b))
    out('=' * 78)

    # ---- Config diff ----
    out()
    out('--- CONFIGURATION ---')
    config_keys = ['model', 'params', 'bits', 'head_mode', 'activation', 'steps',
                   'batch_size', 'accum_steps', 'effective_batch', 'lr', 'alpha',
                   'n_anchors', 'n_domains', 'gpu', 'grad_checkpoint']
    out('  %-25s %-25s %-25s %s' % ('Parameter', args.run_a, args.run_b, 'Changed?'))
    out('  ' + '-' * 90)
    for k in config_keys:
        va = a.get(k, '?')
        vb = b.get(k, '?')
        changed = ' <<<' if str(va) != str(vb) else ''
        out('  %-25s %-25s %-25s%s' % (k, va, vb, changed))

    out()
    out('  Training time: %s=%.1fh  %s=%.1fh' % (
        args.run_a, a.get('training_time_h', 0),
        args.run_b, b.get('training_time_h', 0)))

    # ---- Metrics ----
    out()
    out('--- TRAINING METRICS ---')
    ma = a.get('metrics', {})
    mb = b.get('metrics', {})
    metrics = [
        ('best_bit_accuracy_test', True),
        ('final_bit_acc_test', True),
        ('final_sub_test', True),
        ('final_loss', False),
        ('dead_bits', False),
        ('entropy', True),
    ]
    out('  %-30s %-12s %-12s %s' % ('Metric', args.run_a, args.run_b, 'Delta'))
    out('  ' + '-' * 70)
    for key, higher_better in metrics:
        va = ma.get(key, None)
        vb = mb.get(key, None)
        d = delta(va, vb, higher_is_better=higher_better)
        fmt_va = '%.4f' % va if va is not None else '?'
        fmt_vb = '%.4f' % vb if vb is not None else '?'
        out('  %-30s %-12s %-12s %s' % (key, fmt_va, fmt_vb, d))

    # ---- Target analysis ----
    out()
    out('--- TARGET ANALYSIS ---')
    ta = a.get('target_analysis', {})
    tb = b.get('target_analysis', {})
    target_keys = [
        ('unique_targets', True), ('unique_pct', True),
        ('discriminative_bits', True), ('bits_always_on', False),
    ]
    for key, hb in target_keys:
        va = ta.get(key, '?')
        vb = tb.get(key, '?')
        changed = ' <<<' if str(va) != str(vb) else ''
        out('  %-30s %-12s %-12s%s' % (key, va, vb, changed))

    # ---- Learned analysis ----
    out()
    out('--- LEARNED ANALYSIS ---')
    la = a.get('learned_analysis', {})
    lb = b.get('learned_analysis', {})
    learned_keys = [
        ('unique_learned', True), ('unique_pct', True),
        ('active_bits', True), ('n_duals', True),
        ('n_deps', True), ('n_triadic', True),
        ('n_clusters_090', False),
    ]
    for key, hb in learned_keys:
        va = la.get(key, '?')
        vb = lb.get(key, '?')
        if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
            d = delta(va, vb, fmt='%+.0f' if isinstance(va, int) else '%+.4f',
                      higher_is_better=hb)
        else:
            d = ''
        out('  %-30s %-12s %-12s %s' % (key, va, vb, d))

    # ---- Per-domain accuracy ----
    out()
    out('--- PER-DOMAIN ACCURACY ---')
    lta = a.get('learned_vs_target', {}).get('per_domain', {})
    ltb = b.get('learned_vs_target', {}).get('per_domain', {})
    all_doms = sorted(set(list(lta.keys()) + list(ltb.keys())))
    out('  %-15s %-12s %-12s %s' % ('Domain', args.run_a, args.run_b, 'Delta'))
    out('  ' + '-' * 50)
    for dom in all_doms:
        va = lta.get(dom, {}).get('mean_accuracy', '?')
        vb = ltb.get(dom, {}).get('mean_accuracy', '?')
        if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
            d = delta(va, vb)
        else:
            d = ''
        out('  %-15s %-12s %-12s %s' % (dom,
            '%.3f' % va if isinstance(va, float) else va,
            '%.3f' % vb if isinstance(vb, float) else vb, d))

    # ---- Dual coherence ----
    out()
    out('--- DUAL COHERENCE ---')
    dca = a.get('dual_coherence', {})
    dcb = b.get('dual_coherence', {})
    all_pairs = sorted(set(list(dca.keys()) + list(dcb.keys())))
    for pair in all_pairs:
        va = dca.get(pair, '?')
        vb = dcb.get(pair, '?')
        if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
            d = delta(va, vb)
        else:
            d = ''
        out('  %-30s %-8s %-8s %s' % (pair,
            '%.3f' % va if isinstance(va, float) else va,
            '%.3f' % vb if isinstance(vb, float) else vb, d))

    # ---- Diagnosis comparison ----
    out()
    out('--- DIAGNOSIS ---')
    out('  %s: %s' % (args.run_a, a.get('diagnosis', {}).get('root_cause', '?')))
    out()
    out('  %s: %s' % (args.run_b, b.get('diagnosis', {}).get('root_cause', '?')))

    out()
    out('=' * 78)

    if args.output:
        out_path = os.path.join(RUNS_DIR, args.output)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print('\nSaved to: %s' % out_path)


if __name__ == '__main__':
    main()
