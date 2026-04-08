"""Extract V9_xray_zoom timeline — ultra-high-resolution view of the explosion.

Reads checkpoints from v9_xray_zoom/ (every 50 steps, steps 5000-6000)
to capture the exact micro-sequence of the phase transition.

Paso 1 (v9_xray) revealed the explosion occurs between step 5001 and 5501:
  - bit_acc_test: 52% -> 78%
  - sub_test: 0.7% -> 96.7%
  - dead_bits: 29 -> 32

This script shows whether all bits/layers activate simultaneously
or if there is a detectable micro-sequence.

Results go to v9_xray_zoom_* files. Does NOT modify any prior data.
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

    # Find V9_xray_zoom checkpoints
    ckpt_dir = os.path.join(SCRIPT_DIR, 'checkpoints', 'v9_xray_zoom')
    step_files = globmod.glob(os.path.join(ckpt_dir, 'step_*.pt'))
    step_files.sort(key=lambda f: int(os.path.basename(f).split('_')[1].split('.')[0]))

    if not step_files:
        print(f'ERROR: No checkpoints found in {ckpt_dir}')
        print('Run train_v9_xray_zoom.bat first.')
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
    tl_path = os.path.join(RESULTS_DIR, 'timeline_v9_xray_zoom.json')
    timeline.save_json(tl_path)
    print(f'Timeline saved: {tl_path}')

    # Save curves as CSV
    curves_path = os.path.join(RESULTS_DIR, 'v9_xray_zoom_curves.csv')
    with open(curves_path, 'w', encoding='utf-8') as f:
        metric_names = sorted(timeline.curves.keys())
        f.write('step,' + ','.join(metric_names) + '\n')
        for i, step in enumerate(timeline.steps):
            vals = [str(timeline.curves[m][i]) for m in metric_names]
            f.write(f'{step},' + ','.join(vals) + '\n')
    print(f'Curves CSV saved: {curves_path}')

    # Save phase transitions
    pt_path = os.path.join(RESULTS_DIR, 'v9_xray_zoom_phase_transitions.json')
    pts = [{'step': pt.step, 'metric': pt.metric, 'delta': pt.delta, 'direction': pt.direction}
           for pt in timeline.phase_transitions]
    with open(pt_path, 'w', encoding='utf-8') as f:
        json.dump(pts, f, indent=2)
    print(f'Phase transitions: {len(pts)}')

    # Generate plots
    plots_dir = os.path.join(SCRIPT_DIR, '..', 'runs', 'v9_xray_zoom', 'plots')
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

    # Per-step detail table
    print()
    print('=' * 70)
    print('  V9_XRAY_ZOOM: EXPLOSION MICRO-DYNAMICS (50-step resolution)')
    print('=' * 70)
    if 'churn_rate' in timeline.curves:
        churn_vals = timeline.curves['churn_rate']
        entropy_vals = timeline.curves.get('entropy', [])
        util_vals = timeline.curves.get('utilization', [])
        print(f'  {"Step":>6}  {"Churn":>8}  {"Entropy":>8}  {"Util":>8}  {"dChurn":>8}  {"dEntropy":>8}')
        print(f'  {"-"*6}  {"-"*8}  {"-"*8}  {"-"*8}  {"-"*8}  {"-"*8}')
        for i, step in enumerate(timeline.steps):
            churn = churn_vals[i]
            ent = entropy_vals[i] if i < len(entropy_vals) else 0
            util = util_vals[i] if i < len(util_vals) else 0
            dc = churn - churn_vals[i-1] if i > 0 else 0
            de = ent - (entropy_vals[i-1] if i > 0 and i-1 < len(entropy_vals) else ent)
            marker = ''
            if dc > 0.1:
                marker = ' <-- JUMP'
            elif dc > 0.05:
                marker = ' <-- shift'
            print(f'  {step:>6}  {churn:>8.4f}  {ent:>8.4f}  {util:>8.4f}  {dc:>+8.4f}  {de:>+8.4f}{marker}')

    # Per-layer activation analysis
    print()
    print('  --- Per-layer first activation ---')
    try:
        DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))
        prim_path = os.path.join(DATA_DIR, 'primitivos.json')
        with open(prim_path, 'r', encoding='utf-8') as f:
            prim_data = json.load(f)
        prims = prim_data['primitivos']

        # Group primitives by layer
        layers = {}
        for p in prims:
            layer = p.get('capa', 0)
            if layer not in layers:
                layers[layer] = []
            layers[layer].append(p['nombre'])

        # For each snapshot, count how many primitives per layer have non-zero codes
        print(f'  {"Step":>6}', end='')
        for l in sorted(layers.keys()):
            print(f'  L{l}({len(layers[l])})', end='')
        print()

        for snap in snapshots:
            print(f'  {snap.step:>6}', end='')
            for l in sorted(layers.keys()):
                active = 0
                for name in layers[l]:
                    if name in snap.codes:
                        code = snap.codes[name]
                        if any(b == 1 for b in code):
                            active += 1
                print(f'  {active:>6}', end='')
            print()
    except Exception as e:
        print(f'  Could not analyze layers: {e}')

    print('=' * 70)
    print(f'  Results:  {RESULTS_DIR}/v9_xray_zoom_*')
    print(f'  Plots:    {plots_dir}')
    print('=' * 70)


if __name__ == '__main__':
    main()
