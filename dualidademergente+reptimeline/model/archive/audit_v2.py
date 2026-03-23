"""
Comprehensive V2 Training Audit.

Consolidates ALL information from this training run into one report.
Reads: training_log.csv, results.json, exploration.json, audit_targets.json,
       audit_learned_vs_target.json, deep_analysis.json
Writes: runs/v2/manifest.json, runs/v2/audit_report.txt
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'neural', 'results'))
CKPT_DIR = os.path.join(SCRIPT_DIR, 'checkpoints', 'gpt2_triadic_65_v2')
RUNS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'runs'))


def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_csv_last_row(path):
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
    if len(lines) < 2:
        return None
    headers = lines[0].split(',')
    values = lines[-1].split(',')
    return dict(zip(headers, values))


def main():
    run_id = 'v2'
    run_dir = os.path.join(RUNS_DIR, run_id)
    os.makedirs(run_dir, exist_ok=True)

    print('=' * 70)
    print('  V2 TRAINING AUDIT — COMPREHENSIVE REPORT')
    print('=' * 70)

    # ---- Collect all data ----
    results = load_json(os.path.join(CKPT_DIR, 'results.json'))
    exploration = load_json(os.path.join(RESULTS_DIR, 'exploration.json'))
    audit_targets = load_json(os.path.join(RESULTS_DIR, 'audit_targets.json'))
    audit_learned = load_json(os.path.join(RESULTS_DIR, 'audit_learned_vs_target.json'))
    deep = load_json(os.path.join(RESULTS_DIR, 'deep_analysis.json'))
    last_row = load_csv_last_row(os.path.join(CKPT_DIR, 'training_log.csv'))

    # ---- Build manifest ----
    manifest = {
        'run_id': run_id,
        'date': '2026-03-22',
        'model': results.get('model', 'gpt2-medium') if results else 'gpt2-medium',
        'params': '355M',
        'bits': 65,
        'head_mode': 'simple',
        'activation': 'ifsq',
        'steps': 50000,
        'batch_size': 4,
        'accum_steps': 2,
        'effective_batch': 8,
        'lr': 1e-4,
        'alpha': 0.05,
        'n_anchors': 262,
        'n_domains': 8,
        'gpu': 'RTX 4060 Ti 16GB',
        'training_time_s': results.get('elapsed_s', 0) if results else 0,
        'training_time_h': round(results.get('elapsed_s', 0) / 3600, 1) if results else 0,
        'grad_checkpoint': True,

        'metrics': {
            'best_bit_accuracy_test': results.get('best_bit_accuracy_test', 0) if results else 0,
            'final_loss': results.get('final_loss', 0) if results else 0,
            'final_bit_acc_test': float(last_row.get('bit_acc_test', 0)) if last_row else 0,
            'final_sub_test': float(last_row.get('sub_test', 0)) if last_row else 0,
            'dead_bits': int(last_row.get('dead_bits', 0)) if last_row else 0,
            'entropy': float(last_row.get('entropy', 0)) if last_row else 0,
        },

        'target_analysis': {
            'unique_targets': audit_targets.get('n_unique_targets', 0) if audit_targets else 0,
            'unique_pct': audit_targets.get('unique_pct', 0) if audit_targets else 0,
            'discriminative_bits': audit_targets.get('n_discriminative_bits', 0) if audit_targets else 0,
            'bits_always_on': len(audit_targets.get('bits_always_on', [])) if audit_targets else 0,
            'jaccard_median': audit_targets.get('jaccard_stats', {}).get('median', 0) if audit_targets else 0,
        },

        'learned_analysis': {
            'unique_learned': exploration.get('signature_uniqueness', {}).get('unique', 0) if exploration else 0,
            'unique_pct': exploration.get('signature_uniqueness', {}).get('unique_pct', 0) if exploration else 0,
            'active_bits': exploration.get('active_bits', 0) if exploration else 0,
            'dead_bits_explore': exploration.get('dead_bits', 0) if exploration else 0,
            'n_duals': exploration.get('discovery', {}).get('n_duals', 0) if exploration else 0,
            'n_deps': exploration.get('discovery', {}).get('n_deps', 0) if exploration else 0,
            'n_triadic': exploration.get('discovery', {}).get('n_triadic', 0) if exploration else 0,
            'n_clusters_090': len(deep.get('clusters_090', [])) if deep else 0,
        },

        'learned_vs_target': {
            'overall_accuracy': audit_learned.get('overall_accuracy', 0) if audit_learned else 0,
            'unique_targets_asked': audit_learned.get('unique_targets', 0) if audit_learned else 0,
            'unique_learned_created': audit_learned.get('unique_learned', 0) if audit_learned else 0,
            'per_domain': audit_learned.get('per_domain', {}) if audit_learned else {},
        },

        'dual_coherence': {},
        'regla_de_tres': results.get('regla_de_tres', []) if results else [],

        'diagnosis': {
            'root_cause': 'Target signatures have only 3.8% uniqueness (10/262). '
                          '21/65 bits are always ON, only 31/65 bits are discriminative. '
                          'Domains share massive base signatures (38-50 bits) with 0-4 variable bits.',
            'model_behavior': 'Model achieved 95.8% bit accuracy against targets, but created '
                              '209 unique signatures from 23 unique targets — it actually '
                              'DIVERSIFIED beyond what was asked, which explains the 70.6% uniqueness.',
            'worst_primitivos': 'fuerza(19.8%), posición_temporal(23.3%), si_entonces(33.6%) — '
                                'model fails to learn always-ON bits and rare bits.',
            'recommendation': 'Fix reference_domains.json to reduce base signature overlap. '
                              'Move most primitivos from D to A for non-core domains. '
                              'Increase concept-specific overrides in anchors.py.',
        },

        'files': {
            'training_log': 'training_log.csv',
            'results': 'results.json',
            'exploration': 'exploration.json',
            'deep_analysis': 'deep_analysis.json',
            'audit_targets': 'audit_targets.json',
            'audit_learned_vs_target': 'audit_learned_vs_target.json',
            'checkpoints': 'checkpoints/',
        },
    }

    # Dual coherence
    if exploration and 'dual_coherence' in exploration:
        for dc in exploration['dual_coherence']:
            manifest['dual_coherence'][dc['a'] + '/' + dc['b']] = dc['score']

    # ---- Write manifest ----
    manifest_path = os.path.join(run_dir, 'manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print('  Manifest: %s' % manifest_path)

    # ---- Copy result files ----
    files_to_copy = [
        (os.path.join(CKPT_DIR, 'results.json'), 'results.json'),
        (os.path.join(CKPT_DIR, 'training_log.csv'), 'training_log.csv'),
        (os.path.join(RESULTS_DIR, 'exploration.json'), 'exploration.json'),
        (os.path.join(RESULTS_DIR, 'deep_analysis.json'), 'deep_analysis.json'),
        (os.path.join(RESULTS_DIR, 'audit_targets.json'), 'audit_targets.json'),
        (os.path.join(RESULTS_DIR, 'audit_learned_vs_target.json'), 'audit_learned_vs_target.json'),
    ]
    for src, name in files_to_copy:
        if os.path.exists(src):
            dst = os.path.join(run_dir, name)
            shutil.copy2(src, dst)
            print('  Copied: %s' % name)

    # ---- Checkpoint symlink (just note the path, don't copy GBs) ----
    ckpt_ref = os.path.join(run_dir, 'checkpoints_path.txt')
    with open(ckpt_ref, 'w') as f:
        f.write(os.path.abspath(CKPT_DIR) + '\n')
    print('  Checkpoint reference: %s' % ckpt_ref)

    # ---- Generate human-readable report ----
    report_lines = []
    report_lines.append('=' * 70)
    report_lines.append('  V2 TRAINING RUN — AUDIT REPORT')
    report_lines.append('  Date: 2026-03-22')
    report_lines.append('=' * 70)
    report_lines.append('')
    report_lines.append('  MODEL: GPT-2 Medium (355M) + 65-bit triadic head (simple, iFSQ)')
    report_lines.append('  STEPS: 50,000  BATCH: 4 x 2 = 8 effective  LR: 1e-4  ALPHA: 0.05')
    report_lines.append('  GPU: RTX 4060 Ti 16GB  TIME: %.1f hours' % manifest['training_time_h'])
    report_lines.append('  ANCHORS: 262 concepts across 8 domains')
    report_lines.append('')
    report_lines.append('--- TRAINING METRICS ---')
    m = manifest['metrics']
    report_lines.append('  Best bit accuracy (test): %.4f' % m['best_bit_accuracy_test'])
    report_lines.append('  Final bit accuracy (test): %.4f' % m['final_bit_acc_test'])
    report_lines.append('  Final subsumption (test):  %.4f' % m['final_sub_test'])
    report_lines.append('  Final loss:                %.4f' % m['final_loss'])
    report_lines.append('  Dead bits (training):      %d' % m['dead_bits'])
    report_lines.append('  Entropy:                   %.4f' % m['entropy'])
    report_lines.append('')
    report_lines.append('--- TARGET SIGNATURE ANALYSIS ---')
    t = manifest['target_analysis']
    report_lines.append('  *** ROOT CAUSE OF LOW UNIQUENESS ***')
    report_lines.append('  Unique target signatures:  %d / 262 (%.1f%%)' % (
        t['unique_targets'], t['unique_pct']))
    report_lines.append('  Bits always ON in targets: %d / 65' % t['bits_always_on'])
    report_lines.append('  Discriminative bits:       %d / 65' % t['discriminative_bits'])
    report_lines.append('  Target Jaccard median:     %.3f' % t['jaccard_median'])
    report_lines.append('')
    report_lines.append('--- LEARNED SIGNATURE ANALYSIS ---')
    l = manifest['learned_analysis']
    report_lines.append('  Unique learned signatures: %d / 262 (%.1f%%)' % (
        l['unique_learned'], l['unique_pct']))
    report_lines.append('  Active bits:               %d / 65 (dead: %d)' % (
        l['active_bits'], l['dead_bits_explore']))
    report_lines.append('  Discovered duals:          %d' % l['n_duals'])
    report_lines.append('  Discovered deps:           %d' % l['n_deps'])
    report_lines.append('  Discovered triadic:        %d' % l['n_triadic'])
    report_lines.append('  Concept clusters (J>=0.9): %d' % l['n_clusters_090'])
    report_lines.append('')
    report_lines.append('--- LEARNED vs TARGET ---')
    lt = manifest['learned_vs_target']
    report_lines.append('  Overall per-bit accuracy:  %.4f' % lt['overall_accuracy'])
    report_lines.append('  Targets asked: %d unique signatures' % lt['unique_targets_asked'])
    report_lines.append('  Model created: %d unique signatures (+%d diversification)' % (
        lt['unique_learned_created'],
        lt['unique_learned_created'] - lt['unique_targets_asked']))
    report_lines.append('')
    report_lines.append('  Per-domain accuracy:')
    for dom, info in sorted(lt['per_domain'].items()):
        report_lines.append('    %-15s mean=%.3f  min=%.3f  perfect=%d' % (
            dom, info['mean_accuracy'], info['min_accuracy'], info['n_perfect']))
    report_lines.append('')
    report_lines.append('--- DUAL COHERENCE ---')
    for pair, score in manifest['dual_coherence'].items():
        status = 'OK' if score > 0.5 else 'LOW'
        report_lines.append('  %-30s %.3f  [%s]' % (pair, score, status))
    report_lines.append('')
    report_lines.append('--- REGLA DE TRES ---')
    for r in manifest['regla_de_tres']:
        report_lines.append('  %s  cos=%.3f  bit_acc=%.2f' % (
            r['quad'], r['cosine'], r['bit_accuracy']))
    report_lines.append('')
    report_lines.append('--- DIAGNOSIS ---')
    d = manifest['diagnosis']
    report_lines.append('  ROOT CAUSE: %s' % d['root_cause'])
    report_lines.append('')
    report_lines.append('  MODEL BEHAVIOR: %s' % d['model_behavior'])
    report_lines.append('')
    report_lines.append('  WORST PRIMITIVOS: %s' % d['worst_primitivos'])
    report_lines.append('')
    report_lines.append('  RECOMMENDATION: %s' % d['recommendation'])
    report_lines.append('')
    report_lines.append('=' * 70)
    report_lines.append('  Files archived in: %s' % run_dir)
    report_lines.append('=' * 70)

    report_text = '\n'.join(report_lines)
    print(report_text)

    report_path = os.path.join(run_dir, 'audit_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    print('\n  Report: %s' % report_path)


if __name__ == '__main__':
    main()
