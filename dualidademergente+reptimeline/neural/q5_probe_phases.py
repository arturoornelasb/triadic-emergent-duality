"""Q5: Do phase transitions in training align with duality activations?

Probe: Use TimelineTracker to detect phase transitions (entropy jumps,
churn rate spikes), then check if duality activation steps cluster
around those transitions.

Caveat: Phase transitions in training are common (learning rate warmup,
curriculum shifts) and may not relate to ontological structure.

Requiere: pip install reptimeline
Usage: python q5_probe_phases.py --checkpoints <dir>
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import argparse
import json
import math
import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(SCRIPT_DIR, 'results')
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))
STATS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'stats'))
MODEL_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'model'))
sys.path.insert(0, STATS_DIR)
sys.path.insert(0, MODEL_DIR)

from registry import register_pvalue

try:
    from reptimeline import PrimitiveOverlay, TimelineTracker
    from triadic_extractor import TriadicExtractor
    HAS_REPTIMELINE = True
except ImportError:
    HAS_REPTIMELINE = False

# ######################################################################
#  SECTION 0: DATA LOADING
# ######################################################################

with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
    prim_data = json.load(f)

with open(os.path.join(DATA_DIR, 'dualidad_primitivo_map.json'), 'r', encoding='utf-8') as f:
    dual_data = json.load(f)

CIRCLE_ORDER = ['D1_existir', 'D2_espacio', 'D3_tiempo',
                'D4_posibilidad', 'D5_identidad', 'D6_movimiento', 'D7_orden']
SPIRAL_ORDER = ['D8_uno_muchos', 'D9_dentro_fuera', 'D10_parte_todo',
                'D11_vida_muerte', 'D12_causa_efecto',
                'D13_semejante_diferente', 'D14_sujeto_objeto']
ALL_14 = CIRCLE_ORDER + SPIRAL_ORDER


# ######################################################################
#  SECTION 1: CRITICALITY METRICS
# ######################################################################

def autocorrelation_lag1(series):
    """Lag-1 autocorrelation of a time series."""
    n = len(series)
    if n < 3:
        return 0.0
    mean = sum(series) / n
    var = sum((x - mean) ** 2 for x in series) / n
    if var < 1e-12:
        return 0.0
    cov = sum((series[i] - mean) * (series[i + 1] - mean)
              for i in range(n - 1)) / (n - 1)
    return cov / var


def variance_windows(series, window=10):
    """Sliding window variance."""
    n = len(series)
    if n < window:
        return []
    variances = []
    for i in range(n - window + 1):
        w = series[i:i + window]
        m = sum(w) / len(w)
        v = sum((x - m) ** 2 for x in w) / len(w)
        variances.append(v)
    return variances


# ######################################################################
#  SECTION 2: RUN PROBE
# ######################################################################

def run_probe(checkpoints_dir, device='cuda'):
    """Run Q5 probe."""
    if not HAS_REPTIMELINE:
        return None

    # Load concepts from gold primitivos (try 72-bit first, fallback to 65-bit)
    for gold_name in ['gold_primitivos_72.json', 'gold_primitivos_65.json']:
        gold_path = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'model', gold_name))
        if os.path.exists(gold_path):
            with open(gold_path, 'r', encoding='utf-8') as f:
                concepts = list(json.load(f).keys())
            print(f'  Concepts from {gold_name}: {len(concepts)}')
            break
    else:
        print('  ERROR: gold_primitivos_*.json not found')
        return None

    overlay = PrimitiveOverlay(
        primitivos_path=os.path.join(DATA_DIR, 'primitivos.json')
    )
    extractor = TriadicExtractor(checkpoints_dir)
    tracker = TimelineTracker(extractor=extractor, stability_window=3)

    snapshots = extractor.extract_sequence(checkpoints_dir, concepts,
                                           device=device, max_checkpoints=10)
    timeline = tracker.analyze(snapshots)
    report = overlay.analyze(timeline, concepts=concepts)

    return timeline, report


def analyze(timeline, report):
    """Analyze phase transitions vs duality activations."""
    print("=" * 70)
    print("Q5: Phase transitions vs duality activations")
    print("=" * 70)

    # Phase transitions from timeline
    transitions = timeline.phase_transitions
    print(f"\n  Phase transitions detected: {len(transitions)}")
    for pt in transitions:
        print(f"    step={pt.step}, metric={pt.metric}, "
              f"delta={pt.delta:+.3f} ({pt.direction})")

    transition_steps = sorted(set(pt.step for pt in transitions))

    # Duality activation steps from overlay
    # Approximate: median activation step of anchors per duality
    duality_steps = {}
    for le in report.layer_emergence:
        for act in report.activations:
            # Map activation to duality via anchors
            for d_name, d_info in dual_data['dualidades'].items():
                if act.primitive in d_info.get('anclas', []):
                    if d_name not in duality_steps:
                        duality_steps[d_name] = []
                    duality_steps[d_name].append(act.step)

    print(f"\n  Dualidades with activation data: {len(duality_steps)}")

    # For each duality, compute median activation step
    duality_medians = {}
    for d_name in ALL_14:
        if d_name in duality_steps:
            steps = sorted(duality_steps[d_name])
            duality_medians[d_name] = steps[len(steps) // 2]

    # Distance from each duality activation to nearest phase transition
    if transition_steps and duality_medians:
        distances = []
        for d_name, d_step in duality_medians.items():
            min_dist = min(abs(d_step - ts) for ts in transition_steps)
            distances.append(min_dist)
            print(f"    {d_name}: step={d_step}, "
                  f"nearest_transition_dist={min_dist}")

        mean_dist = sum(distances) / len(distances)
        print(f"\n  Mean distance to nearest transition: {mean_dist:.0f} steps")

        # Null: random activation steps, same count
        rng = random.Random(42)
        max_step = max(timeline.steps)
        null_distances = []

        for _ in range(5000):
            null_d = []
            for _ in range(len(duality_medians)):
                rand_step = rng.randint(0, max_step)
                null_d.append(min(abs(rand_step - ts)
                                  for ts in transition_steps))
            null_distances.append(sum(null_d) / len(null_d))

        n_closer = sum(1 for nd in null_distances if nd <= mean_dist)
        p_proximity = (n_closer + 1) / 5001

        print(f"  Null mean distance: "
              f"{sum(null_distances) / len(null_distances):.0f}")
        print(f"  P(random closer than observed): {p_proximity:.4f}")
    else:
        mean_dist = None
        p_proximity = 1.0
        print("  Insufficient data for proximity test.")

    # Criticality: variance and autocorrelation near transitions
    print("\n  --- Criticality indicators ---\n")
    entropy_curve = timeline.curves.get('entropy', [])
    churn_curve = timeline.curves.get('churn_rate', [])

    criticality = {}
    for name, curve in [('entropy', entropy_curve), ('churn', churn_curve)]:
        if len(curve) > 10:
            ac1 = autocorrelation_lag1(curve)
            var_w = variance_windows(curve)
            max_var = max(var_w) if var_w else 0
            criticality[name] = {
                'autocorrelation_lag1': round(ac1, 4),
                'max_variance': round(max_var, 6),
                'mean_variance': round(sum(var_w) / len(var_w), 6) if var_w else 0,
            }
            print(f"  {name}: AC(1)={ac1:.3f}, max_var={max_var:.4f}")

    # Register
    reg_path = os.path.join(STATS_DIR, 'p_values_registry.json')
    register_pvalue('neural_phases', 'q5_transition_proximity', p_proximity,
                    notes=f'mean_dist={mean_dist}, n_transitions={len(transition_steps)}',
                    path=reg_path)

    # Interpretation
    print("\n  --- Interpretation ---\n")
    if p_proximity < 0.05:
        print("  POSITIVE: Duality activations cluster near phase transitions.")
        print("  Confounder: LR schedule, curriculum changes.")
        verdict = 'positive_with_caveats'
    else:
        print("  NULL: Duality activations do not cluster near transitions.")
        verdict = 'null'

    results = {
        'n_transitions': len(transitions),
        'transition_steps': transition_steps,
        'duality_median_steps': {k: v for k, v in duality_medians.items()},
        'mean_dist_to_transition': round(mean_dist, 1) if mean_dist else None,
        'p_proximity': round(p_proximity, 4),
        'criticality': criticality,
        'verdict': verdict,
    }
    return results


# ######################################################################
#  SECTION 3: MAIN
# ######################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Q5: Phase transitions probe')
    parser.add_argument('--checkpoints', required=True)
    parser.add_argument('--device', default='cuda',
                        help='Device (cuda or cpu)')
    args = parser.parse_args()

    if not HAS_REPTIMELINE:
        print("=" * 70)
        print("Q5: Phase Transitions Probe — reptimeline NOT INSTALLED")
        print("=" * 70)
        print("\nInstall with: pip install reptimeline")
        sys.exit(1)

    result = run_probe(args.checkpoints, args.device)
    if result is None:
        sys.exit(1)

    timeline, report = result
    results = analyze(timeline, report)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_path = os.path.join(RESULTS_DIR, 'q5_phases.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to: {out_path}")
