"""Extract V8_xray_zoom2 timeline — maximum resolution of the explosion.

Reads checkpoints from v8_xray_zoom2/ (every 5 steps, steps 30005-30150)
to determine if the churn jump has internal micro-structure (cascade).

V8_xray zoom revealed churn jumps from 0.000 to 0.534 between step 30050
and 30100. This script captures ~30 snapshots within that window.

Results go to v8_xray_zoom2_* files. Does NOT modify any prior data.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json
import time
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'neural', 'results'))
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))
sys.path.insert(0, SCRIPT_DIR)

import torch
from triadic_extractor import TriadicExtractor
from reptimeline import TimelineTracker
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

    # Find V8_xray_zoom2 checkpoints
    ckpt_dir = os.path.join(SCRIPT_DIR, 'checkpoints', 'v8_xray_zoom2')
    step_files = globmod.glob(os.path.join(ckpt_dir, 'step_*.pt'))
    step_files.sort(key=lambda f: int(os.path.basename(f).split('_')[1].split('.')[0]))

    if not step_files:
        print(f'ERROR: No checkpoints found in {ckpt_dir}')
        print('Run train_v8_xray_zoom2.bat first.')
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
    tl_path = os.path.join(RESULTS_DIR, 'timeline_v8_xray_zoom2.json')
    timeline.save_json(tl_path)
    print(f'Timeline saved: {tl_path}')

    # Save curves as CSV
    curves_path = os.path.join(RESULTS_DIR, 'v8_xray_zoom2_curves.csv')
    with open(curves_path, 'w', encoding='utf-8') as f:
        metric_names = sorted(timeline.curves.keys())
        f.write('step,' + ','.join(metric_names) + '\n')
        for i, step in enumerate(timeline.steps):
            vals = [str(timeline.curves[m][i]) for m in metric_names]
            f.write(f'{step},' + ','.join(vals) + '\n')
    print(f'Curves CSV saved: {curves_path}')

    # Save phase transitions
    pt_path = os.path.join(RESULTS_DIR, 'v8_xray_zoom2_phase_transitions.json')
    pts = [{'step': pt.step, 'metric': pt.metric, 'delta': pt.delta, 'direction': pt.direction}
           for pt in timeline.phase_transitions]
    with open(pt_path, 'w', encoding='utf-8') as f:
        json.dump(pts, f, indent=2)
    print(f'Phase transitions: {len(pts)}')

    # Generate plots
    plots_dir = os.path.join(SCRIPT_DIR, '..', 'runs', 'v8_xray_zoom2', 'plots')
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

    # Per-step detail table
    print()
    print('=' * 74)
    print('  V8_XRAY_ZOOM2: EXPLOSION AT 5-STEP RESOLUTION (GPT-2 Medium)')
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
            dc = churn - churn_vals[i-1] if i > 0 else 0
            marker = ' <-- jump' if dc > 0.1 else ''
            print(f'  {step:>8}  {churn:>8.4f}  {ent:>8.4f}  {util:>8.4f}  {dc:>+8.4f}{marker}')

        # Classify the transition
        print()
        first_nonzero = None
        for i, c in enumerate(churn_vals):
            if c > 0.01 and first_nonzero is None:
                first_nonzero = timeline.steps[i]
        if first_nonzero:
            print(f'  Churn onset at step {first_nonzero}')

    # Per-bit first-change analysis
    print()
    print('  --- Per-bit first change step ---')
    if len(snapshots) >= 2:
        first_change = {}
        base_codes = snapshots[0].codes
        for concept in base_codes.keys():
            base = base_codes[concept]
            for snap in snapshots[1:]:
                if concept in snap.codes:
                    code = snap.codes[concept]
                    for bit_idx in range(min(len(base), len(code))):
                        if base[bit_idx] != code[bit_idx] and bit_idx not in first_change:
                            first_change[bit_idx] = snap.step
                    base = code  # track cumulative changes

        if first_change:
            by_step = {}
            for bit, step in sorted(first_change.items(), key=lambda x: x[1]):
                if step not in by_step:
                    by_step[step] = []
                by_step[step].append(bit)

            for step in sorted(by_step.keys()):
                bits = by_step[step]
                print(f'  Step {step}: {len(bits)} bits first change — {bits}')

            # Map to primitivos if available
            prim_path = os.path.join(DATA_DIR, 'primitivos.json')
            if os.path.exists(prim_path):
                with open(prim_path, 'r', encoding='utf-8') as f:
                    prim_data = json.load(f)
                prims = prim_data['primitivos']
                bit_map = {p.get('bit'): p for p in prims if p.get('bit') is not None}

                print()
                print('  --- Cascade mapped to ontological layers ---')
                total_bits_changed = 0
                for step in sorted(by_step.keys()):
                    bits = by_step[step]
                    total_bits_changed += len(bits)
                    capas = []
                    names = []
                    for b in bits:
                        p = bit_map.get(b, {})
                        names.append(p.get('nombre', f'?bit{b}'))
                        capas.append(p.get('capa', '?'))
                    dist = Counter(capas)
                    dist_str = ' '.join(f'L{k}({v})' for k, v in sorted(dist.items()) if k != '?')
                    print(f'  Step {step}: {len(bits)} bits — {dist_str}')
                    for b, n, c in zip(bits, names, capas):
                        print(f'    bit {b:>2}: {n:<20} L{c}')

                print(f'\n  Total bits that change: {total_bits_changed} / 72')

                # Stable bits
                changed_bits = set(first_change.keys())
                stable_bits = [b for b in range(72) if b not in changed_bits]
                if stable_bits:
                    print(f'  Stable bits (never change): {stable_bits[:10]}{"..." if len(stable_bits) > 10 else ""}')
                    stable_names = []
                    stable_layers = []
                    for b in stable_bits[:10]:
                        p = bit_map.get(b, {})
                        stable_names.append(p.get('nombre', f'?bit{b}'))
                        stable_layers.append(p.get('capa', '?'))
                    print(f'    Names: {stable_names}')
                    print(f'    Layers: {Counter(stable_layers)}')

    print('=' * 74)
    print(f'  Results:  {RESULTS_DIR}/v8_xray_zoom2_*')
    print(f'  Plots:    {plots_dir}')
    print('=' * 74)


if __name__ == '__main__':
    main()
