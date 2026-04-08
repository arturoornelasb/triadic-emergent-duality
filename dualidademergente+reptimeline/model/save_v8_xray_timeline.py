"""Extract V8_xray timeline — high-resolution view of the phase transition.

Adapted from save_v9_xray_timeline.py. Reads checkpoints from v8_xray/ (every 1000 steps)
to capture the micro-dynamics of the churn explosion between steps 30K-45K.

This does NOT modify any V8 original data. Results go to v8_xray_* files.
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

    # Find V8_xray checkpoints
    ckpt_dir = os.path.join(SCRIPT_DIR, 'checkpoints', 'v8_xray')
    step_files = globmod.glob(os.path.join(ckpt_dir, 'step_*.pt'))
    step_files.sort(key=lambda f: int(os.path.basename(f).split('_')[1].split('.')[0]))

    if not step_files:
        print(f'ERROR: No checkpoints found in {ckpt_dir}')
        print('Run train_v8_xray.bat first.')
        sys.exit(1)

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
    tl_path = os.path.join(RESULTS_DIR, 'timeline_v8_xray.json')
    timeline.save_json(tl_path)
    print(f'Timeline saved: {tl_path}')

    # Save curves as CSV
    curves_path = os.path.join(RESULTS_DIR, 'v8_xray_curves.csv')
    with open(curves_path, 'w', encoding='utf-8') as f:
        metric_names = sorted(timeline.curves.keys())
        f.write('step,' + ','.join(metric_names) + '\n')
        for i, step in enumerate(timeline.steps):
            vals = [str(timeline.curves[m][i]) for m in metric_names]
            f.write(f'{step},' + ','.join(vals) + '\n')
    print(f'Curves CSV saved: {curves_path}')

    # Save phase transitions
    pt_path = os.path.join(RESULTS_DIR, 'v8_xray_phase_transitions.json')
    pts = [{'step': pt.step, 'metric': pt.metric, 'delta': pt.delta, 'direction': pt.direction}
           for pt in timeline.phase_transitions]
    with open(pt_path, 'w', encoding='utf-8') as f:
        json.dump(pts, f, indent=2)
    print(f'Phase transitions: {len(pts)}')

    # Generate plots
    plots_dir = os.path.join(SCRIPT_DIR, '..', 'runs', 'v8_xray', 'plots')
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

    # Per-step churn detail (the key output for xray)
    print()
    print('=' * 74)
    print('  V8_XRAY: PHASE TRANSITION MICRO-DYNAMICS (GPT-2 Medium)')
    print('=' * 74)
    if 'churn_rate' in timeline.curves:
        churn_vals = timeline.curves['churn_rate']
        entropy_vals = timeline.curves.get('entropy', [])
        util_vals = timeline.curves.get('utilization', [])
        print(f'  {"Step":>8}  {"Churn":>8}  {"Entropy":>8}  {"Util":>8}  {"dChurn":>8}')
        print(f'  {"-"*8}  {"-"*8}  {"-"*8}  {"-"*8}  {"-"*8}')
        for i, step in enumerate(timeline.steps):
            churn = churn_vals[i]
            ent = entropy_vals[i] if i < len(entropy_vals) else 0
            util = util_vals[i] if i < len(util_vals) else 0
            delta = churn - churn_vals[i-1] if i > 0 else 0
            marker = ' <-- jump' if delta > 0.1 else ''
            print(f'  {step:>8}  {churn:>8.4f}  {ent:>8.4f}  {util:>8.4f}  {delta:>+8.4f}{marker}')

        # Find the exact explosion step
        max_delta_idx = 0
        max_delta = 0
        for i in range(1, len(churn_vals)):
            d = churn_vals[i] - churn_vals[i-1]
            if d > max_delta:
                max_delta = d
                max_delta_idx = i
        if max_delta > 0.1:
            print(f'\n  EXPLOSION detected between step {timeline.steps[max_delta_idx-1]} '
                  f'and step {timeline.steps[max_delta_idx]}')
            print(f'  Churn jump: {churn_vals[max_delta_idx-1]:.4f} -> {churn_vals[max_delta_idx]:.4f} '
                  f'(delta={max_delta:.4f})')
            print(f'\n  --> Next: zoom with train_v8_xray_zoom.bat from step {timeline.steps[max_delta_idx-1]} '
                  f'to step {timeline.steps[max_delta_idx]} with --save-every 50')
        else:
            print('\n  No sharp explosion detected — transition is gradual at this resolution.')

    print('=' * 74)
    print(f'  Results:  {RESULTS_DIR}/v8_xray_*')
    print(f'  Plots:    {plots_dir}')
    print('=' * 74)


if __name__ == '__main__':
    main()
