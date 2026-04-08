"""Extract V9 timeline and generate plots via reptimeline.

Adapted from save_v8_timeline.py for V9 GPT-Neo 125M (50K steps, 10 checkpoints).
This is the SECOND model — addresses N=1 critique (Debilidad #5).
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'neural', 'results'))
sys.path.insert(0, SCRIPT_DIR)

import torch
from triadic_extractor import TriadicExtractor
from reptimeline import TimelineTracker, PrimitiveOverlay
from reptimeline.core import ConceptSnapshot
import glob as globmod


def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f'Device: {device}')

    # Load gold concepts
    gold_path = os.path.join(SCRIPT_DIR, 'gold_extended_v7.json')
    with open(gold_path, 'r', encoding='utf-8') as f:
        gold_data = json.load(f)
    concepts = list(gold_data.keys())
    print(f'Concepts: {len(concepts)}')

    # Find V9 checkpoints
    ckpt_dir = os.path.join(SCRIPT_DIR, 'checkpoints', 'v9_neo_openwebtext')
    step_files = globmod.glob(os.path.join(ckpt_dir, 'step_*.pt'))
    step_files.sort(key=lambda f: int(os.path.basename(f).split('_')[1].split('.')[0]))

    print(f'Checkpoints: {len(step_files)}')
    for sf in step_files:
        print(f'  {os.path.basename(sf)}')

    # Extract snapshots
    extractor = TriadicExtractor(n_bits=72)
    snapshots = []
    t0 = time.time()
    for i, sf in enumerate(step_files):
        snap = extractor.extract(sf, concepts, device=device)
        snapshots.append(snap)
        elapsed = time.time() - t0
        print(f'  {i+1}/{len(step_files)} done (step {snap.step}) [{elapsed:.0f}s]')

    # Analyze
    print('Analyzing timeline...')
    tracker = TimelineTracker(extractor=extractor, stability_window=3)
    timeline = tracker.analyze(snapshots)
    timeline.print_summary()

    # Save timeline JSON
    os.makedirs(RESULTS_DIR, exist_ok=True)
    tl_path = os.path.join(RESULTS_DIR, 'timeline_v9.json')
    timeline.save_json(tl_path)
    print(f'Timeline saved: {tl_path}')

    # Save curves as CSV
    curves_path = os.path.join(RESULTS_DIR, 'v9_curves.csv')
    with open(curves_path, 'w', encoding='utf-8') as f:
        metric_names = sorted(timeline.curves.keys())
        f.write('step,' + ','.join(metric_names) + '\n')
        for i, step in enumerate(timeline.steps):
            vals = [str(timeline.curves[m][i]) for m in metric_names]
            f.write(f'{step},' + ','.join(vals) + '\n')
    print(f'Curves CSV saved: {curves_path}')

    # Save phase transitions
    pt_path = os.path.join(RESULTS_DIR, 'v9_phase_transitions.json')
    pts = [{'step': pt.step, 'metric': pt.metric, 'delta': pt.delta, 'direction': pt.direction}
           for pt in timeline.phase_transitions]
    with open(pt_path, 'w', encoding='utf-8') as f:
        json.dump(pts, f, indent=2)
    print(f'Phase transitions: {len(pts)}')

    # Save stability scores
    stab_path = os.path.join(RESULTS_DIR, 'v9_bit_stability.json')
    with open(stab_path, 'w', encoding='utf-8') as f:
        json.dump({str(k): v for k, v in sorted(timeline.stability.items())}, f, indent=2)
    print(f'Stability scores saved for {len(timeline.stability)} bits')

    # Compute churn from curves
    if 'churn_rate' in timeline.curves:
        churn_vals = timeline.curves['churn_rate']
        final_churn = churn_vals[-1] if churn_vals else None
        print(f'Final churn rate: {final_churn:.3f}' if final_churn else 'No churn data')

    # Generate plots
    plots_dir = os.path.join(SCRIPT_DIR, '..', 'runs', 'v9_neo', 'plots')
    os.makedirs(plots_dir, exist_ok=True)

    from reptimeline.viz import plot_phase_dashboard, plot_churn_heatmap

    try:
        print('Generating phase dashboard...')
        plot_phase_dashboard(timeline,
                             save_path=os.path.join(plots_dir, 'phase_dashboard.png'))
    except Exception as e:
        print(f'WARNING: phase_dashboard: {e}')

    try:
        print('Generating churn heatmap...')
        plot_churn_heatmap(timeline, max_bits=72,
                           save_path=os.path.join(plots_dir, 'churn_heatmap.png'))
    except Exception as e:
        print(f'WARNING: churn_heatmap: {e}')

    # Swimlane
    try:
        from reptimeline.viz import plot_swimlane
        DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))
        prim_path = os.path.join(DATA_DIR, 'primitivos.json')
        if os.path.exists(prim_path):
            with open(prim_path, 'r', encoding='utf-8') as f:
                prims = json.load(f)
            prim_names = list(prims.keys()) if isinstance(prims, dict) else []
            print(f'Generating swimlane for {len(prim_names)} primitivos...')
            plot_swimlane(timeline, concepts=prim_names[:30], max_bits=72,
                          save_path=os.path.join(plots_dir, 'swimlane_primitivos.png'))
    except Exception as e:
        print(f'WARNING: swimlane: {e}')

    # Layer emergence
    try:
        DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))
        prim_path = os.path.join(DATA_DIR, 'primitivos.json')
        if os.path.exists(prim_path):
            overlay = PrimitiveOverlay(primitivos_path=prim_path)
            prim_report = overlay.analyze(timeline, concepts=list(snapshots[-1].codes.keys()))
            if prim_report.layer_emergence:
                from reptimeline.viz import plot_layer_emergence
                print('Generating layer emergence...')
                plot_layer_emergence(prim_report,
                                     save_path=os.path.join(plots_dir, 'layer_emergence.png'))
    except Exception as e:
        print(f'WARNING: layer_emergence: {e}')

    # Connections null model
    print('\nRunning connections null model (72 primitivos, 100 permutations)...')
    try:
        with open(gold_path, 'r', encoding='utf-8') as f:
            gold = json.load(f)
        prim_set = set(c for c in gold if gold[c].get('capa', 0) >= 1)
        filtered = []
        for snap in snapshots:
            filtered.append(ConceptSnapshot(
                step=snap.step,
                codes={k: v for k, v in snap.codes.items() if k in prim_set},
                metadata=snap.metadata,
            ))

        class BinaryExtractor:
            def shared_features(self, code_a, code_b):
                return [i for i in range(min(len(code_a), len(code_b)))
                        if code_a[i] == 1 and code_b[i] == 1]

        null_tracker = TimelineTracker(extractor=BinaryExtractor())
        null_result = null_tracker.connections_null_model(filtered, n_permutations=100, seed=42)
        print(f'  Observed: {null_result["n_observed"]}')
        print(f'  Expected: {null_result["n_expected"]:.1f} +/- {null_result["null_std"]:.1f}')
        print(f'  O/E ratio: {null_result["oe_ratio"]:.3f}')

        null_path = os.path.join(RESULTS_DIR, 'v9_connections_null.json')
        with open(null_path, 'w') as f:
            json.dump(null_result, f, indent=2)
        print(f'  Saved: {null_path}')
    except Exception as e:
        print(f'WARNING: null model: {e}')

    # Summary
    print()
    print('=' * 60)
    print('  V9 TIMELINE SUMMARY (GPT-Neo 125M, OpenWebText)')
    print('=' * 60)
    print(f'  Timeline: {tl_path}')
    print(f'  Curves:   {curves_path}')
    print(f'  Plots:    {plots_dir}')
    print(f'  Steps:    {timeline.steps[0]} -> {timeline.steps[-1]}')
    print(f'  Births:   {len(timeline.births)}')
    print(f'  Deaths:   {len(timeline.deaths)}')
    print(f'  Connections: {len(timeline.connections)}')
    print(f'  Phase transitions: {len(timeline.phase_transitions)}')
    for pt in timeline.phase_transitions:
        print(f'    step {pt.step}: {pt.metric} {pt.direction} delta={pt.delta:+.4f}')
    print('=' * 60)

    # Compare with v8 if available
    v8_pt_path = os.path.join(RESULTS_DIR, 'v8_phase_transitions.json')
    if os.path.exists(v8_pt_path):
        with open(v8_pt_path, 'r') as f:
            v8_pts = json.load(f)
        print(f'\n  V8 had {len(v8_pts)} phase transitions')
        print(f'  V9 has {len(pts)} phase transitions')
        print('  Cross-model crystallization comparison possible!')


if __name__ == '__main__':
    main()
