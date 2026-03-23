"""
Fase 3: Exploration — Map concepts through the trained triadic head.

Uses checkpoints to extract N-bit signatures for ALL concepts,
then runs reptimeline BitDiscovery + PrimitiveOverlay to find:
  - Which concepts cluster together (shared bits)
  - What duals the model learned (anti-correlated bits)
  - What dependencies exist (if A active, B always active)
  - Cross-capa structure (capa 1 ↔ capa 5?)
  - Per-capa separation (do capas form distinct clusters?)

With --timeline: builds full multi-checkpoint timeline with visualizations:
  - Swimlane diagram (concept code evolution)
  - Phase dashboard (entropy, churn, utilization)
  - Churn heatmap (per-bit stability)
  - Layer emergence (when each capa's primitives stabilize)
  - Reconciler (discovered vs theory comparison)

Usage:
    python explore.py --run-name gpt2_triadic_72_v5_frozen --gold-file gold_primitivos_72.json --bits 72
    python explore.py --timeline --plots-dir plots/v5  # full timeline + plots
    python explore.py --add "quantum,relativity,photon"  # add extras

Requires: reptimeline, torch, transformers (triadic-microgpt conda env)
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json
import time
import math
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))
RESULTS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'neural', 'results'))
sys.path.insert(0, SCRIPT_DIR)

import glob as globmod
import torch
import torch.nn.functional as F
from triadic_extractor import TriadicExtractor
from reptimeline import TimelineTracker, BitDiscovery, PrimitiveOverlay
from reptimeline.core import ConceptSnapshot
from reptimeline.reconcile import Reconciler


# ######################################################################
#  SECTION 1: LOAD CONCEPTS
# ######################################################################

def load_gold_concepts(gold_file='gold_primitivos_65.json'):
    """Load gold primitivo concepts with capa labels."""
    gold_path = os.path.join(SCRIPT_DIR, gold_file)
    with open(gold_path, 'r', encoding='utf-8') as f:
        gold = json.load(f)
    return gold


def parse_extra_concepts(add_str):
    """Parse comma-separated concept list."""
    if not add_str:
        return []
    return [c.strip() for c in add_str.split(',') if c.strip()]


# ######################################################################
#  SECTION 2: EXTRACTION
# ######################################################################

def extract_all(checkpoint_path, concepts, device='cpu', n_bits=65):
    """Extract n-bit signatures for all concepts."""
    extractor = TriadicExtractor(n_bits=n_bits)
    snap = extractor.extract(checkpoint_path, concepts, device=device)
    return snap, extractor


# ######################################################################
#  SECTION 3: CAPA ANALYSIS
# ######################################################################

def capa_separation(snap, gold_data):
    """Compute within-capa vs between-capa similarity."""
    capas = {}
    for concept, data in gold_data.items():
        if concept in snap.codes:
            capa = 'capa_%d' % data.get('capa', 0)
            if capa not in capas:
                capas[capa] = []
            capas[capa].append(concept)

    results = {}
    group_names = sorted(capas.keys())

    for grp in group_names:
        concepts = capas[grp]
        if len(concepts) < 2:
            continue

        # Within-capa similarity (Jaccard)
        within_sims = []
        for i in range(len(concepts)):
            for j in range(i + 1, len(concepts)):
                a = set(k for k, v in enumerate(snap.codes[concepts[i]]) if v == 1)
                b = set(k for k, v in enumerate(snap.codes[concepts[j]]) if v == 1)
                union = a | b
                if union:
                    within_sims.append(len(a & b) / len(union))

        # Between-capa similarity (sample from other capas)
        between_sims = []
        other_concepts = [c for g, cs in capas.items() if g != grp for c in cs]
        import random
        rng = random.Random(42)
        n_sample = min(100, len(concepts) * len(other_concepts))
        for _ in range(n_sample):
            c_in = rng.choice(concepts)
            c_out = rng.choice(other_concepts)
            a = set(k for k, v in enumerate(snap.codes[c_in]) if v == 1)
            b = set(k for k, v in enumerate(snap.codes[c_out]) if v == 1)
            union = a | b
            if union:
                between_sims.append(len(a & b) / len(union))

        within_mean = sum(within_sims) / len(within_sims) if within_sims else 0
        between_mean = sum(between_sims) / len(between_sims) if between_sims else 0
        separation = within_mean / between_mean if between_mean > 0 else 0

        results[grp] = {
            'n_concepts': len(concepts),
            'within_similarity': round(within_mean, 4),
            'between_similarity': round(between_mean, 4),
            'separation_ratio': round(separation, 4),
        }
        print(f'    {grp:<15} n={len(concepts):>3}  '
              f'within={within_mean:.3f}  between={between_mean:.3f}  '
              f'sep={separation:.3f}')

    return results


def cross_capa_matrix(snap, gold_data):
    """Compute capa-to-capa mean Jaccard similarity matrix."""
    capas = {}
    for concept, data in gold_data.items():
        if concept in snap.codes:
            capa = 'capa_%d' % data.get('capa', 0)
            if capa not in capas:
                capas[capa] = []
            capas[capa].append(concept)

    group_names = sorted(capas.keys())
    matrix = {}

    for i, g1 in enumerate(group_names):
        matrix[g1] = {}
        for j, g2 in enumerate(group_names):
            sims = []
            for c1 in capas[g1]:
                for c2 in capas[g2]:
                    if c1 == c2:
                        continue
                    a = set(k for k, v in enumerate(snap.codes[c1]) if v == 1)
                    b = set(k for k, v in enumerate(snap.codes[c2]) if v == 1)
                    union = a | b
                    if union:
                        sims.append(len(a & b) / len(union))
            matrix[g1][g2] = round(sum(sims) / len(sims), 4) if sims else 0

    return matrix, group_names


def find_cross_capa_bridges(snap, gold_data, top_n=20):
    """Find concepts from different capas with highest similarity."""
    bridges = []
    concepts = list(snap.codes.keys())
    group_map = {c: 'capa_%d' % gold_data[c].get('capa', 0) for c in concepts if c in gold_data}

    for i in range(len(concepts)):
        for j in range(i + 1, len(concepts)):
            c1, c2 = concepts[i], concepts[j]
            if c1 not in group_map or c2 not in group_map:
                continue
            if group_map[c1] == group_map[c2]:
                continue

            a = set(k for k, v in enumerate(snap.codes[c1]) if v == 1)
            b = set(k for k, v in enumerate(snap.codes[c2]) if v == 1)
            union = a | b
            if not union:
                continue
            sim = len(a & b) / len(union)
            shared = sorted(a & b)
            bridges.append({
                'concept_a': c1, 'capa_a': group_map[c1],
                'concept_b': c2, 'capa_b': group_map[c2],
                'jaccard': round(sim, 4),
                'shared_bits': shared,
                'n_shared': len(shared),
            })

    bridges.sort(key=lambda x: x['jaccard'], reverse=True)
    return bridges[:top_n]


# ######################################################################
#  SECTION 4: SIGNATURE ANALYSIS
# ######################################################################

def signature_uniqueness(snap):
    """Check how many concepts have unique 65-bit signatures."""
    sig_map = {}
    for concept, code in snap.codes.items():
        sig = tuple(code)
        if sig not in sig_map:
            sig_map[sig] = []
        sig_map[sig].append(concept)

    n_unique = sum(1 for v in sig_map.values() if len(v) == 1)
    collisions = {k: v for k, v in sig_map.items() if len(v) > 1}

    return {
        'total': len(snap.codes),
        'unique': n_unique,
        'unique_pct': round(n_unique / len(snap.codes) * 100, 1) if snap.codes else 0,
        'n_collisions': len(collisions),
        'collision_groups': [v for v in collisions.values()],
    }


def bit_usage_stats(snap):
    """Per-bit activation rate across all concepts."""
    n = len(snap.codes)
    if n == 0:
        return []
    dim = snap.code_dim
    rates = []
    for bit in range(dim):
        active = sum(1 for code in snap.codes.values() if code[bit] == 1)
        rates.append(round(active / n, 4))
    return rates


# ######################################################################
#  SECTION 5: TIMELINE & VISUALIZATION
# ######################################################################

def extract_timeline(ckpt_dir, concepts, extractor, device='cpu',
                     max_checkpoints=20):
    """Extract snapshots from multiple checkpoints for timeline analysis."""
    # Find all step_*.pt files
    step_files = sorted(globmod.glob(os.path.join(ckpt_dir, 'step_*.pt')))
    best_file = os.path.join(ckpt_dir, 'best.pt')

    if not step_files:
        print('  WARNING: No step_*.pt files found, using best.pt only')
        snap = extractor.extract(best_file, concepts, device=device)
        return [snap]

    # Sample evenly if too many checkpoints
    if len(step_files) > max_checkpoints:
        indices = [int(i * (len(step_files) - 1) / (max_checkpoints - 1))
                   for i in range(max_checkpoints)]
        step_files = [step_files[i] for i in indices]

    print(f'  Extracting from {len(step_files)} checkpoints...')
    snapshots = []
    for i, sf in enumerate(step_files):
        snap = extractor.extract(sf, concepts, device=device)
        snapshots.append(snap)
        if (i + 1) % 5 == 0 or i == len(step_files) - 1:
            print(f'    {i+1}/{len(step_files)} done (step {snap.step})')

    return snapshots


def generate_plots(timeline, prim_report, plots_dir, snap):
    """Generate all reptimeline visualizations."""
    os.makedirs(plots_dir, exist_ok=True)
    n_bits = snap.code_dim

    from reptimeline.viz import (
        plot_swimlane, plot_phase_dashboard, plot_churn_heatmap,
    )

    # 1. Phase dashboard (entropy, churn, utilization)
    try:
        print('    Phase dashboard...')
        plot_phase_dashboard(timeline,
                             save_path=os.path.join(plots_dir, 'phase_dashboard.png'))
    except Exception as e:
        print(f'    WARNING: phase_dashboard failed: {e}')

    # 2. Swimlane (concept code evolution)
    try:
        print('    Swimlane diagram...')
        plot_swimlane(timeline, max_bits=min(n_bits, 72),
                      save_path=os.path.join(plots_dir, 'swimlane.png'))
    except Exception as e:
        print(f'    WARNING: swimlane failed: {e}')

    # 3. Churn heatmap (per-bit stability)
    try:
        print('    Churn heatmap...')
        plot_churn_heatmap(timeline, max_bits=min(n_bits, 72),
                           save_path=os.path.join(plots_dir, 'churn_heatmap.png'))
    except Exception as e:
        print(f'    WARNING: churn_heatmap failed: {e}')

    # 4. Layer emergence
    if prim_report and prim_report.layer_emergence:
        try:
            from reptimeline.viz import plot_layer_emergence
            print('    Layer emergence...')
            plot_layer_emergence(prim_report,
                                 save_path=os.path.join(plots_dir, 'layer_emergence.png'))
        except Exception as e:
            print(f'    WARNING: layer_emergence failed: {e}')

    # 5. Interactive plots (HTML)
    try:
        from reptimeline.viz.interactive import (
            plot_phase_dashboard_interactive,
            plot_swimlane_interactive,
        )
        print('    Interactive phase dashboard (HTML)...')
        plot_phase_dashboard_interactive(
            timeline, save_html=os.path.join(plots_dir, 'phase_dashboard.html'))
        print('    Interactive swimlane (HTML)...')
        plot_swimlane_interactive(
            timeline, max_bits=min(n_bits, 72),
            save_html=os.path.join(plots_dir, 'swimlane.html'))
    except Exception as e:
        print(f'    WARNING: interactive plots failed: {e}')


# ######################################################################
#  SECTION 6: MAIN
# ######################################################################

def main():
    parser = argparse.ArgumentParser(description='Fase 3: Explore trained triadic model')
    parser.add_argument('--checkpoint', default=None,
                        help='Checkpoint path (default: best.pt)')
    parser.add_argument('--concepts', default=None,
                        help='JSON file with extra concept list')
    parser.add_argument('--add', default=None,
                        help='Comma-separated extra concepts')
    parser.add_argument('--device', default='cpu',
                        help='Device (cpu or cuda)')
    parser.add_argument('--top-bridges', type=int, default=30,
                        help='Number of cross-capa bridges to show')
    parser.add_argument('--gold-file', default='gold_primitivos_65.json',
                        help='Gold file (default: gold_primitivos_65.json)')
    parser.add_argument('--bits', type=int, default=65,
                        help='Number of triadic bits (default: 65)')
    parser.add_argument('--run-name', default=None,
                        help='Checkpoint dir name (default: auto-detect)')
    parser.add_argument('--timeline', action='store_true',
                        help='Extract from multiple checkpoints for full timeline')
    parser.add_argument('--max-checkpoints', type=int, default=15,
                        help='Max checkpoints for timeline (default: 15)')
    parser.add_argument('--plots-dir', default=None,
                        help='Directory to save plots (default: plots/<run-name>)')
    parser.add_argument('--csv-dir', default=None,
                        help='Export timeline CSV to this directory')
    args = parser.parse_args()

    print()
    print('=' * 70)
    print('  FASE 3: EXPLORATION — Triadic Semantic Map')
    print('=' * 70)

    # --- Checkpoint ---
    if args.checkpoint:
        ckpt_path = args.checkpoint
    else:
        # Auto-detect checkpoint dir
        run_name = args.run_name
        if run_name is None:
            # Try v4 first, then v3
            for candidate in ['gpt2_triadic_72_v4', 'gpt2_triadic_65_v3']:
                if os.path.exists(os.path.join(SCRIPT_DIR, 'checkpoints', candidate, 'best.pt')):
                    run_name = candidate
                    break
            if run_name is None:
                run_name = 'gpt2_triadic_65_v3'
        ckpt_path = os.path.join(SCRIPT_DIR, 'checkpoints', run_name, 'best.pt')
        if not os.path.exists(ckpt_path):
            import glob
            steps = sorted(glob.glob(os.path.join(
                SCRIPT_DIR, 'checkpoints', run_name, 'step_*.pt')))
            if steps:
                ckpt_path = steps[-1]
            else:
                print('  ERROR: No checkpoint found for %s.' % run_name)
                sys.exit(1)

    print(f'  Checkpoint: {os.path.basename(ckpt_path)}')
    print(f'  Device: {args.device}')

    # --- Concepts ---
    gold_data = load_gold_concepts(args.gold_file)
    concepts = list(gold_data.keys())
    n_bits = args.bits
    print(f'  Gold file: {args.gold_file}')
    print(f'  Gold primitivos: {len(concepts)} (6 capas)')
    print(f'  Bits: {n_bits}')

    if args.concepts:
        with open(args.concepts, 'r', encoding='utf-8') as f:
            extra = json.load(f)
        if isinstance(extra, list):
            concepts.extend(extra)
        elif isinstance(extra, dict):
            concepts.extend(extra.keys())
        print(f'  + Extra from {args.concepts}: {len(extra)}')

    if args.add:
        extras = parse_extra_concepts(args.add)
        concepts.extend(extras)
        print(f'  + Extra from --add: {len(extras)}')

    concepts = list(dict.fromkeys(concepts))  # deduplicate preserving order
    print(f'  Total concepts: {len(concepts)}')

    # --- Extract ---
    print()
    print('[1/5] Extracting %d-bit signatures...' % n_bits)
    t0 = time.time()
    snap, extractor = extract_all(ckpt_path, concepts, device=args.device, n_bits=n_bits)
    elapsed = time.time() - t0
    print(f'  Extracted {len(snap.codes)} concepts in {elapsed:.1f}s')
    print(f'  Code dim: {snap.code_dim}')

    # --- Signature uniqueness ---
    print()
    print('[2/5] Signature analysis...')
    uniq = signature_uniqueness(snap)
    print(f'  Unique signatures: {uniq["unique"]}/{uniq["total"]} ({uniq["unique_pct"]}%)')
    if uniq['collision_groups']:
        print(f'  Collisions ({uniq["n_collisions"]} groups):')
        for group in uniq['collision_groups'][:10]:
            print(f'    {group}')

    bit_rates = bit_usage_stats(snap)
    dead = sum(1 for r in bit_rates if r < 0.02 or r > 0.98)
    active = len(bit_rates) - dead
    mean_rate = sum(bit_rates) / len(bit_rates) if bit_rates else 0
    print(f'  Active bits: {active}/{len(bit_rates)} (dead: {dead})')
    print(f'  Mean activation rate: {mean_rate:.3f} (ideal: 0.50)')

    # --- Capa separation ---
    print()
    print('[3/5] Capa separation analysis...')
    capa_sep = capa_separation(snap, gold_data)

    # Cross-capa matrix
    print()
    print('  Cross-capa similarity matrix:')
    matrix, grp_names = cross_capa_matrix(snap, gold_data)
    # Header
    header = '              ' + ''.join(f'{g[:6]:>7}' for g in grp_names)
    print(f'  {header}')
    for g1 in grp_names:
        row = f'  {g1[:12]:<14}'
        for g2 in grp_names:
            val = matrix[g1][g2]
            row += f'{val:>7.3f}'
        print(row)

    # --- Cross-capa bridges ---
    print()
    print(f'[4/5] Cross-capa bridges (top {args.top_bridges})...')
    bridges = find_cross_capa_bridges(snap, gold_data, top_n=args.top_bridges)
    for b in bridges:
        print(f'    {b["concept_a"]:<20} ({b["capa_a"]}) <-> '
              f'{b["concept_b"]:<20} ({b["capa_b"]}) '
              f'J={b["jaccard"]:.3f} ({b["n_shared"]} shared bits)')

    # --- BitDiscovery ---
    print()
    print('[5/5] BitDiscovery (unsupervised structure)...')
    discovery = BitDiscovery(
        dead_threshold=0.02,
        dual_threshold=-0.3,
        dep_confidence=0.9,
        triadic_threshold=0.7,
    )
    report = discovery.discover(snap, top_k=10)

    print(f'  Active bits: {report.n_active_bits}')
    print(f'  Dead bits:   {report.n_dead_bits}')
    print(f'  Discovered duals: {len(report.discovered_duals)}')
    print(f'  Discovered deps:  {len(report.discovered_deps)}')
    print(f'  Discovered triadic: {len(report.discovered_triadic_deps)}')

    if report.discovered_duals:
        print('\n  --- Top Discovered Duals ---')
        for d in report.discovered_duals[:15]:
            print(f'    bit {d.bit_a:>2} <-> bit {d.bit_b:>2}: '
                  f'r={d.anti_correlation:+.3f}  '
                  f'exclusive={d.concepts_exclusive}  both={d.concepts_both}')

    # Bit semantics: which concepts define each bit
    print('\n  --- Bit Semantics (active bits) ---')
    active_bits = [b for b in report.bit_semantics if 0.02 < b.activation_rate < 0.98]
    active_bits.sort(key=lambda b: abs(b.activation_rate - 0.5))  # most discriminative first
    for b in active_bits[:20]:
        top = ', '.join(b.top_concepts[:4])
        anti = ', '.join(b.anti_concepts[:2]) if b.anti_concepts else '-'
        print(f'    bit {b.bit_index:>2}: rate={b.activation_rate:.2f}  '
              f'top=[{top}]  anti=[{anti}]')

    # --- Timeline extraction (multi-checkpoint) ---
    timeline = None
    snapshots = None
    if args.timeline:
        print()
        print('[6/8] Timeline extraction (multi-checkpoint)...')
        ckpt_dir = os.path.dirname(ckpt_path)
        snapshots = extract_timeline(ckpt_dir, concepts, extractor,
                                     device=args.device,
                                     max_checkpoints=args.max_checkpoints)
        tracker = TimelineTracker(extractor=extractor, stability_window=3)
        timeline = tracker.analyze(snapshots)

        print(f'  Snapshots: {len(snapshots)}')
        print(f'  Steps: {timeline.steps[0]} → {timeline.steps[-1]}')
        print(f'  Births: {len(timeline.births)}')
        print(f'  Deaths: {len(timeline.deaths)}')
        print(f'  Connections: {len(timeline.connections)}')
        print(f'  Phase transitions: {len(timeline.phase_transitions)}')

        if timeline.phase_transitions:
            print('  Detected phase transitions:')
            for pt in timeline.phase_transitions:
                print(f'    step {pt.step}: {pt.metric} '
                      f'delta={pt.delta:+.4f} ({pt.direction})')
    else:
        # Single-snapshot timeline for overlay (backward compat)
        tracker = TimelineTracker(extractor=extractor, stability_window=1)
        timeline = tracker.analyze([snap])

    # --- Primitive Overlay (full analysis) ---
    prim_path = os.path.join(DATA_DIR, 'primitivos.json')
    prim_report = None
    if os.path.exists(prim_path):
        step_label = '7/8' if args.timeline else '6/6'
        print()
        print(f'[{step_label}] Primitive Overlay (full analysis)...')
        overlay = PrimitiveOverlay(primitivos_path=prim_path)
        prim_report = overlay.analyze(timeline, concepts=list(snap.codes.keys()))

        # Dual coherence (all 14+ pairs now)
        if prim_report.dual_coherence:
            print('\n  Dual Coherence (%d pairs):' % len(prim_report.dual_coherence))
            for dc in prim_report.dual_coherence:
                status = 'OK' if dc.coherence_score > 0.5 else 'LOW'
                print(f'    {dc.primitive_a:<20} <-> {dc.primitive_b:<20} '
                      f'coherence={dc.coherence_score:.3f}  [{status}]')
            cohs = [dc.coherence_score for dc in prim_report.dual_coherence]
            print(f'    {"MEAN":<20}     {"":20} '
                  f'coherence={sum(cohs)/len(cohs):.3f}')

        # Layer emergence
        if prim_report.layer_emergence:
            print('\n  Layer Emergence:')
            for le in prim_report.layer_emergence:
                print(f'    Layer {le.layer} ({le.layer_name}): '
                      f'activated={le.primitives_activated}/{le.n_primitives} '
                      f'median_step={le.median_activation_step}')

        # Dependency completions (top 10)
        if prim_report.deps_completions:
            print(f'\n  Dependency Completions ({len(prim_report.deps_completions)} total):')
            for dc in prim_report.deps_completions[:10]:
                print(f'    {dc.primitive:<20} step={dc.step}  '
                      f'deps={dc.deps}')

        # Reconciler: theory vs discovered
        try:
            reconciler = Reconciler(overlay)
            reconciliation = reconciler.reconcile(report, timeline)
            print('\n  Reconciler (theory vs discovered):')
            if hasattr(reconciliation, 'mismatches') and reconciliation.mismatches:
                for mm in reconciliation.mismatches[:10]:
                    print(f'    {mm}')
            elif hasattr(reconciliation, 'summary'):
                print(f'    {reconciliation.summary}')
            else:
                print(f'    {reconciliation}')
        except Exception as e:
            print(f'  Reconciler skipped: {e}')

    # --- Visualizations ---
    if args.timeline or args.plots_dir:
        plots_dir = args.plots_dir
        if plots_dir is None:
            run_label = args.run_name or 'current'
            plots_dir = os.path.normpath(
                os.path.join(SCRIPT_DIR, '..', 'runs', run_label, 'plots'))

        step_label = '8/8' if args.timeline else '7/7'
        print()
        print(f'[{step_label}] Generating visualizations...')
        print(f'  Output: {plots_dir}')
        generate_plots(timeline, prim_report, plots_dir, snap)
        print(f'  Done — plots saved to {plots_dir}')

    # --- CSV export ---
    if args.csv_dir:
        print()
        print(f'  Exporting timeline CSV to {args.csv_dir}...')
        csv_paths = timeline.to_csv(args.csv_dir)
        for p in csv_paths:
            print(f'    {p}')

    # ######################################################################
    #  SAVE RESULTS
    # ######################################################################

    os.makedirs(RESULTS_DIR, exist_ok=True)

    results = {
        'checkpoint': os.path.basename(ckpt_path),
        'step': snap.step,
        'n_concepts': len(snap.codes),
        'device': args.device,
        'signature_uniqueness': uniq,
        'bit_activation_rates': bit_rates,
        'active_bits': active,
        'dead_bits': dead,
        'capa_separation': capa_sep,
        'cross_capa_matrix': matrix,
        'cross_capa_bridges': bridges[:args.top_bridges],
        'discovery': {
            'n_duals': len(report.discovered_duals),
            'n_deps': len(report.discovered_deps),
            'n_triadic': len(report.discovered_triadic_deps),
            'duals': [
                {'bit_a': d.bit_a, 'bit_b': d.bit_b,
                 'r': round(d.anti_correlation, 4),
                 'exclusive': d.concepts_exclusive,
                 'both': d.concepts_both}
                for d in report.discovered_duals
            ],
            'bit_semantics': [
                {'bit': b.bit_index,
                 'rate': round(b.activation_rate, 4),
                 'top': b.top_concepts[:5],
                 'anti': b.anti_concepts[:3]}
                for b in report.bit_semantics
                if 0.02 < b.activation_rate < 0.98
            ],
        },
    }

    if prim_report and prim_report.dual_coherence:
        results['dual_coherence'] = [
            {'a': dc.primitive_a, 'b': dc.primitive_b,
             'score': round(dc.coherence_score, 4)}
            for dc in prim_report.dual_coherence
        ]

    if prim_report and prim_report.layer_emergence:
        results['layer_emergence'] = [
            {'layer': le.layer, 'name': le.layer_name,
             'activated': le.primitives_activated,
             'total': le.n_primitives,
             'median_step': le.median_activation_step}
            for le in prim_report.layer_emergence
        ]

    if args.timeline and timeline:
        results['timeline'] = {
            'n_snapshots': len(timeline.steps),
            'steps': timeline.steps,
            'n_births': len(timeline.births),
            'n_deaths': len(timeline.deaths),
            'n_connections': len(timeline.connections),
            'n_phase_transitions': len(timeline.phase_transitions),
            'phase_transitions': [
                {'step': pt.step, 'metric': pt.metric,
                 'delta': round(pt.delta, 4), 'direction': pt.direction}
                for pt in timeline.phase_transitions
            ],
        }

    # Save all concept signatures
    results['signatures'] = {
        concept: {
            'bits': code,
            'active_indices': [i for i, v in enumerate(code) if v == 1],
            'n_active': sum(code),
            'capa': gold_data.get(concept, {}).get('capa', 0),
        }
        for concept, code in snap.codes.items()
    }

    out_path = os.path.join(RESULTS_DIR, 'exploration.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Save timeline JSON separately (for later re-analysis)
    if args.timeline and timeline:
        tl_path = os.path.join(RESULTS_DIR, 'timeline.json')
        timeline.save_json(tl_path)
        print(f'  Timeline saved: {tl_path}')

    print()
    print('=' * 70)
    print(f'  Results saved to: {out_path}')
    print(f'  Signatures: {len(snap.codes)} concepts x {snap.code_dim} bits')
    print(f'  Unique: {uniq["unique_pct"]}%  Active bits: {active}/{snap.code_dim}')
    sep_mean = sum(d['separation_ratio'] for d in capa_sep.values()) / len(capa_sep) if capa_sep else 0
    print(f'  Mean capa separation: {sep_mean:.3f}')
    print(f'  Duals: {len(report.discovered_duals)}  '
          f'Deps: {len(report.discovered_deps)}  '
          f'Triadic: {len(report.discovered_triadic_deps)}')
    if prim_report and prim_report.dual_coherence:
        cohs = [dc.coherence_score for dc in prim_report.dual_coherence]
        print(f'  Dual coherence: {sum(cohs)/len(cohs):.3f} '
              f'({len(cohs)} pairs)')
    if args.timeline:
        plots_dir = args.plots_dir or os.path.normpath(
            os.path.join(SCRIPT_DIR, '..', 'runs', args.run_name or 'current', 'plots'))
        print(f'  Plots: {plots_dir}')
    print('=' * 70)


if __name__ == '__main__':
    main()
