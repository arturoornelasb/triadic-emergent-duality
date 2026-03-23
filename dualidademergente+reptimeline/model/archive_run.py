"""
Archive a training run: copy results + checkpoints reference to runs/{version}/.

General-purpose replacement for audit_v2.py. Works for any version.

Usage:
    python archive_run.py v3
    python archive_run.py v3 --force   # overwrite existing archive

Creates:
    runs/{version}/
        manifest.json       — full metadata + metrics
        run_config.json     — copy from checkpoints
        results.json        — copy from checkpoints
        training_log.csv    — copy from checkpoints
        gold_*.json         — copy of gold targets used
        exploration.json    — from neural/results/ if exists
        deep_analysis.json  — from neural/results/ if exists
        audit_targets.json  — from neural/results/ if exists
        audit_learned_vs_target.json — from neural/results/ if exists
        checkpoints_path.txt — pointer to .pt files (no copy of GBs)
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json
import shutil
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'neural', 'results'))
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
    parser = argparse.ArgumentParser(description='Archive a training run')
    parser.add_argument('version', help='Run version (e.g. v3, v4)')
    parser.add_argument('--force', action='store_true', help='Overwrite existing archive')
    args = parser.parse_args()

    version = args.version
    run_name = f'gpt2_triadic_65_{version}'
    ckpt_dir = os.path.join(SCRIPT_DIR, 'checkpoints', run_name)
    run_dir = os.path.join(RUNS_DIR, version)

    if not os.path.exists(ckpt_dir):
        print(f'ERROR: Checkpoint dir not found: {ckpt_dir}')
        print(f'  Available: {os.listdir(os.path.join(SCRIPT_DIR, "checkpoints"))}')
        sys.exit(1)

    if os.path.exists(run_dir) and not args.force:
        print(f'ERROR: Archive already exists: {run_dir}')
        print(f'  Use --force to overwrite')
        sys.exit(1)

    os.makedirs(run_dir, exist_ok=True)

    print('=' * 70)
    print(f'  ARCHIVING RUN: {version} ({run_name})')
    print('=' * 70)

    # ---- Load data ----
    results = load_json(os.path.join(ckpt_dir, 'results.json'))
    run_config = load_json(os.path.join(ckpt_dir, 'run_config.json'))
    exploration = load_json(os.path.join(RESULTS_DIR, 'exploration.json'))
    audit_targets = load_json(os.path.join(RESULTS_DIR, 'audit_targets.json'))
    audit_learned = load_json(os.path.join(RESULTS_DIR, 'audit_learned_vs_target.json'))
    deep = load_json(os.path.join(RESULTS_DIR, 'deep_analysis.json'))
    prim_targets = load_json(os.path.join(RESULTS_DIR, 'audit_primitivos_targets.json'))
    last_row = load_csv_last_row(os.path.join(ckpt_dir, 'training_log.csv'))

    # ---- Build manifest ----
    manifest = {
        'run_id': version,
        'run_name': run_name,
        'date': results.get('date', 'unknown') if results else 'unknown',

        # Config
        'model': results.get('model', 'gpt2-medium') if results else 'gpt2-medium',
        'params': '355M',
        'bits': results.get('bits', 65) if results else 65,
        'head_mode': results.get('head_mode', 'simple') if results else 'simple',
        'activation': results.get('activation', 'ifsq') if results else 'ifsq',
        'steps': results.get('steps', 0) if results else 0,
        'batch_size': results.get('batch_size', 4) if results else 4,
        'accum_steps': results.get('accum_steps', 2) if results else 2,
        'effective_batch': results.get('effective_batch', 8) if results else 8,
        'lr': results.get('lr', 0) if results else 0,
        'alpha': results.get('alpha', 0) if results else 0,
        'gold_file': results.get('gold_file', 'unknown') if results else 'unknown',
        'n_concepts': results.get('n_concepts', 0) if results else 0,
        'gpu': 'RTX 4060 Ti 16GB',
        'training_time_s': results.get('elapsed_s', 0) if results else 0,
        'training_time_h': results.get('elapsed_h', 0) if results else 0,
        'grad_checkpoint': True,

        # Metrics
        'metrics': {
            'best_bit_accuracy_test': results.get('best_bit_accuracy_test', 0) if results else 0,
            'final_loss': results.get('final_loss', 0) if results else 0,
            'final_bit_acc_test': float(last_row.get('bit_acc_test', 0)) if last_row else 0,
            'final_sub_test': float(last_row.get('sub_test', 0)) if last_row else 0,
            'dead_bits': int(last_row.get('dead_bits', 0)) if last_row else 0,
            'entropy': float(last_row.get('entropy', 0)) if last_row else 0,
        },

        # Target analysis (from audit_primitivos_targets or audit_targets)
        'target_analysis': {},

        # Learned analysis
        'learned_analysis': {},

        # Learned vs target
        'learned_vs_target': {},

        # Dual coherence
        'dual_coherence': {},

        # Regla de tres
        'regla_de_tres': results.get('regla_de_tres', []) if results else [],

        # Diagnosis (filled by user or subsequent audit)
        'diagnosis': {},

        # Files in archive
        'files': {},
    }

    # Fill target analysis
    if prim_targets:
        manifest['target_analysis'] = {
            'unique_targets': prim_targets.get('n_unique', 0),
            'unique_pct': prim_targets.get('unique_pct', 0),
            'discriminative_bits': prim_targets.get('n_discriminative', 0),
            'bits_always_on': prim_targets.get('n_always_on', 0),
            'jaccard_median': prim_targets.get('jaccard_median', 0),
        }
    elif audit_targets:
        manifest['target_analysis'] = {
            'unique_targets': audit_targets.get('n_unique_targets', 0),
            'unique_pct': audit_targets.get('unique_pct', 0),
            'discriminative_bits': audit_targets.get('n_discriminative_bits', 0),
            'bits_always_on': len(audit_targets.get('bits_always_on', [])),
            'jaccard_median': audit_targets.get('jaccard_stats', {}).get('median', 0),
        }

    # Fill learned analysis
    if exploration:
        manifest['learned_analysis'] = {
            'unique_learned': exploration.get('signature_uniqueness', {}).get('unique', 0),
            'unique_pct': exploration.get('signature_uniqueness', {}).get('unique_pct', 0),
            'active_bits': exploration.get('active_bits', 0),
            'n_duals': exploration.get('discovery', {}).get('n_duals', 0),
            'n_deps': exploration.get('discovery', {}).get('n_deps', 0),
            'n_triadic': exploration.get('discovery', {}).get('n_triadic', 0),
            'n_clusters_090': len(deep.get('clusters_090', [])) if deep else 0,
        }

    # Fill learned vs target
    if audit_learned:
        manifest['learned_vs_target'] = {
            'overall_accuracy': audit_learned.get('overall_accuracy', 0),
            'unique_targets_asked': audit_learned.get('unique_targets', 0),
            'unique_learned_created': audit_learned.get('unique_learned', 0),
            'per_capa': audit_learned.get('per_capa', audit_learned.get('per_domain', {})),
        }

    # Fill dual coherence
    if exploration and 'dual_coherence' in exploration:
        for dc in exploration['dual_coherence']:
            manifest['dual_coherence'][dc['a'] + '/' + dc['b']] = dc['score']

    # ---- Copy files ----
    files_to_copy = [
        (os.path.join(ckpt_dir, 'results.json'), 'results.json'),
        (os.path.join(ckpt_dir, 'run_config.json'), 'run_config.json'),
        (os.path.join(ckpt_dir, 'training_log.csv'), 'training_log.csv'),
        (os.path.join(RESULTS_DIR, 'exploration.json'), 'exploration.json'),
        (os.path.join(RESULTS_DIR, 'deep_analysis.json'), 'deep_analysis.json'),
        (os.path.join(RESULTS_DIR, 'audit_targets.json'), 'audit_targets.json'),
        (os.path.join(RESULTS_DIR, 'audit_learned_vs_target.json'), 'audit_learned_vs_target.json'),
        (os.path.join(RESULTS_DIR, 'audit_primitivos_targets.json'), 'audit_primitivos_targets.json'),
    ]

    # Also copy gold file from checkpoint dir
    gold_in_ckpt = os.path.join(ckpt_dir, results.get('gold_file', '')) if results else None
    if gold_in_ckpt and os.path.exists(gold_in_ckpt):
        files_to_copy.append((gold_in_ckpt, os.path.basename(gold_in_ckpt)))

    copied = []
    for src, name in files_to_copy:
        if os.path.exists(src):
            dst = os.path.join(run_dir, name)
            shutil.copy2(src, dst)
            copied.append(name)
            print(f'  Copied: {name}')

    manifest['files'] = {name: name for name in copied}

    # Checkpoint reference (don't copy GBs of .pt files)
    ckpt_ref = os.path.join(run_dir, 'checkpoints_path.txt')
    with open(ckpt_ref, 'w') as f:
        f.write(os.path.abspath(ckpt_dir) + '\n')
    print(f'  Checkpoint reference: {ckpt_ref}')

    # List .pt files for documentation
    pt_files = sorted([f for f in os.listdir(ckpt_dir) if f.endswith('.pt')])
    manifest['checkpoint_files'] = pt_files
    print(f'  Checkpoint .pt files: {len(pt_files)}')

    # ---- Write manifest ----
    manifest_path = os.path.join(run_dir, 'manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f'  Manifest: {manifest_path}')

    # ---- Summary ----
    print()
    print('-' * 70)
    m = manifest['metrics']
    print(f'  Run:           {version} ({run_name})')
    print(f'  Date:          {manifest["date"]}')
    print(f'  Model:         {manifest["model"]} ({manifest["params"]})')
    print(f'  Steps:         {manifest["steps"]}')
    print(f'  Gold file:     {manifest["gold_file"]} ({manifest["n_concepts"]} concepts)')
    print(f'  Best accuracy: {m["best_bit_accuracy_test"]:.4f}')
    print(f'  Final loss:    {m["final_loss"]:.4f}')
    print(f'  Dead bits:     {m["dead_bits"]}')
    print(f'  Time:          {manifest["training_time_h"]}h')
    print(f'  Checkpoints:   {len(pt_files)} files in {ckpt_dir}')
    print(f'  Archive:       {run_dir}/')
    print(f'  Files:         {len(copied)} copied')
    print()
    print(f'  Compare with previous: python compare_runs.py v2 {version}')
    print('=' * 70)


if __name__ == '__main__':
    main()
