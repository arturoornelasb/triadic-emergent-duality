"""Quick script to save V7 timeline JSON and generate plots.

The full explore.py --timeline got stuck on the swimlane with 2166 concepts.
This script extracts the timeline, saves it, and generates plots with
only the 72 primitivos for the swimlane (manageable size).
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
from reptimeline import TimelineTracker, BitDiscovery, PrimitiveOverlay
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

    # Find checkpoints
    ckpt_dir = os.path.join(SCRIPT_DIR, 'checkpoints', 'v7_contrastive')
    step_files = globmod.glob(os.path.join(ckpt_dir, 'step_*.pt'))
    step_files.sort(key=lambda f: int(os.path.basename(f).split('_')[1].split('.')[0]))

    # Sample 20 evenly
    max_ckpt = 20
    if len(step_files) > max_ckpt:
        indices = [int(i * (len(step_files) - 1) / (max_ckpt - 1)) for i in range(max_ckpt)]
        step_files = [step_files[i] for i in indices]

    print(f'Checkpoints: {len(step_files)}')

    # Extract
    extractor = TriadicExtractor(n_bits=72)
    snapshots = []
    t0 = time.time()
    for i, sf in enumerate(step_files):
        snap = extractor.extract(sf, concepts, device=device)
        snapshots.append(snap)
        if (i + 1) % 5 == 0 or i == len(step_files) - 1:
            elapsed = time.time() - t0
            print(f'  {i+1}/{len(step_files)} done (step {snap.step}) [{elapsed:.0f}s]')

    # Analyze
    print('Analyzing timeline...')
    tracker = TimelineTracker(extractor=extractor, stability_window=3)
    timeline = tracker.analyze(snapshots)
    timeline.print_summary()

    # Save timeline JSON
    os.makedirs(RESULTS_DIR, exist_ok=True)
    tl_path = os.path.join(RESULTS_DIR, 'timeline_v7.json')
    timeline.save_json(tl_path)
    print(f'Timeline saved: {tl_path}')

    # Save curves as CSV for easy analysis
    curves_path = os.path.join(RESULTS_DIR, 'v7_curves.csv')
    with open(curves_path, 'w', encoding='utf-8') as f:
        metric_names = sorted(timeline.curves.keys())
        f.write('step,' + ','.join(metric_names) + '\n')
        for i, step in enumerate(timeline.steps):
            vals = [str(timeline.curves[m][i]) for m in metric_names]
            f.write(f'{step},' + ','.join(vals) + '\n')
    print(f'Curves CSV saved: {curves_path}')

    # Save phase transitions
    pt_path = os.path.join(RESULTS_DIR, 'v7_phase_transitions.json')
    pts = [{'step': pt.step, 'metric': pt.metric, 'delta': pt.delta, 'direction': pt.direction}
           for pt in timeline.phase_transitions]
    with open(pt_path, 'w', encoding='utf-8') as f:
        json.dump(pts, f, indent=2)
    print(f'Phase transitions: {len(pts)}')

    # Save stability scores
    stab_path = os.path.join(RESULTS_DIR, 'v7_bit_stability.json')
    with open(stab_path, 'w', encoding='utf-8') as f:
        json.dump({str(k): v for k, v in sorted(timeline.stability.items())}, f, indent=2)
    print(f'Stability scores saved for {len(timeline.stability)} bits')

    # Generate plots — ONLY with manageable subset for swimlane
    plots_dir = os.path.join(SCRIPT_DIR, '..', 'runs', 'v7_contrastive', 'plots')
    os.makedirs(plots_dir, exist_ok=True)

    from reptimeline.viz import plot_phase_dashboard, plot_churn_heatmap

    # Phase dashboard (already done, but regenerate to be safe)
    try:
        print('Generating phase dashboard...')
        plot_phase_dashboard(timeline,
                             save_path=os.path.join(plots_dir, 'phase_dashboard.png'))
    except Exception as e:
        print(f'WARNING: phase_dashboard: {e}')

    # Churn heatmap (per-bit, 72 bits — manageable)
    try:
        print('Generating churn heatmap...')
        plot_churn_heatmap(timeline, max_bits=72,
                           save_path=os.path.join(plots_dir, 'churn_heatmap.png'))
    except Exception as e:
        print(f'WARNING: churn_heatmap: {e}')

    # Swimlane — ONLY primitivos (72 concepts, not 2166)
    try:
        from reptimeline.viz import plot_swimlane
        # Get only primitivo names (concepts that have a 'target' key with 72 bits)
        DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))
        prim_path = os.path.join(DATA_DIR, 'primitivos.json')
        if os.path.exists(prim_path):
            with open(prim_path, 'r', encoding='utf-8') as f:
                prims = json.load(f)
            prim_names = list(prims.keys()) if isinstance(prims, dict) else []
            print(f'Generating swimlane for {len(prim_names)} primitivos...')
            plot_swimlane(timeline, concepts=prim_names[:30], max_bits=72,
                          save_path=os.path.join(plots_dir, 'swimlane_primitivos.png'))
        else:
            print('No primitivos.json found, skipping swimlane')
    except Exception as e:
        print(f'WARNING: swimlane: {e}')

    # Layer emergence (if overlay available)
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

    # Interactive HTML plots
    try:
        from reptimeline.viz.interactive import (
            plot_phase_dashboard_interactive,
            plot_swimlane_interactive,
        )
        print('Generating interactive HTML plots...')
        plot_phase_dashboard_interactive(
            timeline, save_html=os.path.join(plots_dir, 'phase_dashboard.html'))
        plot_swimlane_interactive(
            timeline, max_bits=72,
            save_html=os.path.join(plots_dir, 'swimlane.html'))
    except Exception as e:
        print(f'WARNING: interactive: {e}')

    print()
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


if __name__ == '__main__':
    main()
