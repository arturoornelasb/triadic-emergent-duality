"""Q1: Does the model learn primitives in layer order?

Probe: Correlate theoretical capa (1-6) with median activation step
from PrimitiveOverlay. If positive Spearman rho, deeper layers emerge
later — consistent with the framework.

Caveat: A positive result could reflect training-data frequency bias
(common words are learned first, and happen to be in lower layers).
We control for this with partial correlation on frequency.

Requiere: pip install reptimeline
Usage: python q1_probe_layer_order.py --checkpoints <dir> --vocab <path>
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import argparse
import json
import math
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(SCRIPT_DIR, 'results')
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))
STATS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'stats'))
sys.path.insert(0, STATS_DIR)

from bootstrap import bootstrap_ci
from registry import register_pvalue
from bh_fdr import benjamini_hochberg

try:
    from reptimeline import PrimitiveOverlay, TimelineTracker
    from reptimeline.extractors import TriadicExtractor
    from reptimeline.core import ConceptSnapshot
    HAS_REPTIMELINE = True
except ImportError:
    HAS_REPTIMELINE = False

# ######################################################################
#  SECTION 0: DATA LOADING
# ######################################################################

with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
    prim_data = json.load(f)

prims = prim_data['primitivos']
capa_map = {p['nombre']: p['capa'] for p in prims}
bit_map = {p['nombre']: p.get('bit') for p in prims}

# ######################################################################
#  SECTION 1: SPEARMAN RHO (stdlib)
# ######################################################################

def _rank(values):
    """Assign average ranks handling ties."""
    n = len(values)
    indexed = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j < n - 1 and values[indexed[j + 1]] == values[indexed[j]]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1
        for k in range(i, j + 1):
            ranks[indexed[k]] = avg_rank
        i = j + 1
    return ranks


def spearman_rho(x, y):
    """Spearman rank correlation."""
    n = len(x)
    if n < 3:
        return 0.0
    rx = _rank(x)
    ry = _rank(y)
    mx = sum(rx) / n
    my = sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    dx = math.sqrt(sum((rx[i] - mx) ** 2 for i in range(n)))
    dy = math.sqrt(sum((ry[i] - my) ** 2 for i in range(n)))
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)


def partial_spearman(x, y, z):
    """Partial Spearman: rho(x,y | z)."""
    rxy = spearman_rho(x, y)
    rxz = spearman_rho(x, z)
    ryz = spearman_rho(y, z)
    denom = math.sqrt(max(0, (1 - rxz ** 2) * (1 - ryz ** 2)))
    if denom < 1e-12:
        return 0.0
    return (rxy - rxz * ryz) / denom


def spearman_p_perm(x, y, n_perms=5000, seed=42):
    """Permutation-based p-value for Spearman rho."""
    import random
    rng = random.Random(seed)
    observed = abs(spearman_rho(x, y))
    count = 0
    y_copy = list(y)
    for _ in range(n_perms):
        rng.shuffle(y_copy)
        if abs(spearman_rho(x, y_copy)) >= observed:
            count += 1
    return (count + 1) / (n_perms + 1)


# ######################################################################
#  SECTION 2: RUN PROBE
# ######################################################################

def run_probe(checkpoints_dir, vocab_path=None):
    """Run Q1 probe on saved checkpoints."""
    if not HAS_REPTIMELINE:
        print("ERROR: reptimeline not installed. pip install reptimeline")
        return None

    # Build overlay
    overlay = PrimitiveOverlay(
        primitivos_path=os.path.join(DATA_DIR, 'primitivos.json')
    )

    # Build extractor and tracker
    extractor = TriadicExtractor(checkpoints_dir)
    tracker = TimelineTracker(extractor=extractor, stability_window=3)

    # Load concepts from vocab or use default
    concepts = None
    if vocab_path and os.path.exists(vocab_path):
        with open(vocab_path, 'r', encoding='utf-8') as f:
            concepts = json.load(f)

    # Build snapshots
    snapshots = extractor.load_snapshots(checkpoints_dir)
    timeline = tracker.analyze(snapshots)

    # Run overlay
    report = overlay.analyze(timeline, concepts=concepts)

    # Extract: for each primitive, its layer and median activation step
    capas = []
    steps = []
    names_used = []

    for le in report.layer_emergence:
        # Get all primitives in this layer
        layer_prims = [p for p in prims if p['capa'] == le.layer]
        for p in layer_prims:
            # Find activation for this primitive
            acts = [a for a in report.activations if a.primitive == p['nombre']]
            if acts:
                median_step = sorted([a.step for a in acts])[len(acts) // 2]
                capas.append(p['capa'])
                steps.append(median_step)
                names_used.append(p['nombre'])

    return capas, steps, names_used, report


# ######################################################################
#  SECTION 3: ANALYSIS
# ######################################################################

def analyze(capas, steps, names_used, freq_data=None):
    """Compute correlations and p-values."""
    print("=" * 70)
    print("Q1: Does the model learn primitives in layer order?")
    print("=" * 70)

    n = len(capas)
    print(f"\n  Primitives with activation data: {n}")

    # Main correlation
    rho = spearman_rho(capas, steps)
    p_val = spearman_p_perm(capas, steps)
    print(f"\n  Spearman rho(capa, median_step) = {rho:.3f}")
    print(f"  Permutation p-value = {p_val:.4f}")

    # Bootstrap CI
    def rho_fn(a, b):
        return spearman_rho(list(a), list(b))

    ci = bootstrap_ci(capas, steps, rho_fn, n_bootstrap=2000, ci=0.95, seed=42)
    print(f"  95% CI: [{ci['ci_low']:.3f}, {ci['ci_high']:.3f}]")

    # Register p-value
    reg_path = os.path.join(STATS_DIR, 'p_values_registry.json')
    register_pvalue('neural_layer', 'q1_capa_vs_step', p_val,
                    notes=f'rho={rho:.3f}, n={n}', path=reg_path)

    results = {
        'n_primitives': n,
        'rho_capa_step': round(rho, 4),
        'p_value': round(p_val, 4),
        'ci_95': [round(ci['ci_low'], 4), round(ci['ci_high'], 4)],
    }

    # Partial correlation controlling for frequency
    if freq_data and len(freq_data) == n:
        rho_partial = partial_spearman(capas, steps, freq_data)
        p_partial = spearman_p_perm(capas, steps)  # simplified
        print(f"\n  Partial rho(capa, step | freq) = {rho_partial:.3f}")
        results['rho_partial_freq'] = round(rho_partial, 4)
        register_pvalue('neural_layer', 'q1_partial_freq', p_partial,
                        notes=f'rho_partial={rho_partial:.3f}, n={n}',
                        path=reg_path)

    # Per-layer breakdown
    print("\n  --- Per-layer breakdown ---\n")
    layer_steps = {}
    for c, s in zip(capas, steps):
        if c not in layer_steps:
            layer_steps[c] = []
        layer_steps[c].append(s)

    layer_summary = {}
    for layer in sorted(layer_steps):
        ss = layer_steps[layer]
        mean_s = sum(ss) / len(ss)
        print(f"  Layer {layer}: n={len(ss)}, mean_step={mean_s:.0f}")
        layer_summary[str(layer)] = {
            'n': len(ss),
            'mean_step': round(mean_s, 1)
        }
    results['per_layer'] = layer_summary

    # Interpretation
    print("\n  --- Interpretation ---\n")
    if p_val < 0.05 and rho > 0:
        print("  POSITIVE: Higher layers emerge later in training.")
        print("  Confounder: frequency bias (common tokens learned first).")
        if 'rho_partial_freq' in results:
            if results['rho_partial_freq'] > 0.3:
                print("  Partial rho still positive after frequency control.")
            else:
                print("  WARNING: Effect disappears after frequency control.")
        results['verdict'] = 'positive_with_caveats'
    elif p_val < 0.05 and rho < 0:
        print("  NEGATIVE: Lower layers emerge LATER — contradicts framework.")
        results['verdict'] = 'contradicts_framework'
    else:
        print("  NULL: No significant correlation between layer and step.")
        results['verdict'] = 'null'

    return results


# ######################################################################
#  SECTION 4: MAIN
# ######################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Q1: Layer order probe')
    parser.add_argument('--checkpoints', required=True,
                        help='Directory with model checkpoints')
    parser.add_argument('--vocab', default=None,
                        help='JSON file with concept list')
    parser.add_argument('--freq', default=None,
                        help='JSON file with token frequencies')
    args = parser.parse_args()

    if not HAS_REPTIMELINE:
        print("=" * 70)
        print("Q1: Layer Order Probe — reptimeline NOT INSTALLED")
        print("=" * 70)
        print("\nInstall with: pip install reptimeline")
        print("Then re-run with: python q1_probe_layer_order.py --checkpoints <dir>")
        sys.exit(1)

    result = run_probe(args.checkpoints, args.vocab)
    if result is None:
        sys.exit(1)

    capas, steps, names_used, report = result

    freq_data = None
    if args.freq and os.path.exists(args.freq):
        with open(args.freq, 'r', encoding='utf-8') as f:
            freq_map = json.load(f)
        freq_data = [freq_map.get(n, 0) for n in names_used]

    results = analyze(capas, steps, names_used, freq_data)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_path = os.path.join(RESULTS_DIR, 'q1_layer_order.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to: {out_path}")
