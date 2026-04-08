"""Q3: Does the model's discovered dependency graph match the theoretical DAG?

Probe: Run BitDiscovery to find dependencies (P(parent|child) >= threshold),
then compare with the theoretical DAG from primitivos.json using Precision,
Recall, F1, and Structural Hamming Distance (SHD).

Caveat: Co-activation patterns can arise from co-occurrence in training
data, not from structural dependency. A dependency A→B in the model
might just mean tokens containing A also tend to contain B.

Requiere: pip install reptimeline
Usage: python q3_probe_dag.py --checkpoints <dir>
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import argparse
import json
import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(SCRIPT_DIR, 'results')
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))
STATS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'stats'))
MODEL_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'model'))
sys.path.insert(0, STATS_DIR)
sys.path.insert(0, MODEL_DIR)

from bh_fdr import benjamini_hochberg
from registry import register_pvalue

try:
    from reptimeline import BitDiscovery
    from triadic_extractor import TriadicExtractor
    HAS_REPTIMELINE = True
except ImportError:
    HAS_REPTIMELINE = False

# ######################################################################
#  SECTION 0: DATA LOADING
# ######################################################################

with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
    prim_data = json.load(f)

prims = prim_data['primitivos']
name_to_bit = {p['nombre']: p.get('bit') for p in prims}
bit_to_name = {p.get('bit'): p['nombre'] for p in prims if p.get('bit') is not None}

# Theoretical edges: set of (parent_bit, child_bit)
theo_edges = set()
for p in prims:
    child_bit = p.get('bit')
    if child_bit is None:
        continue
    for dep_name in p['deps']:
        parent_bit = name_to_bit.get(dep_name)
        if parent_bit is not None:
            theo_edges.add((parent_bit, child_bit))


# ######################################################################
#  SECTION 1: GRAPH COMPARISON METRICS
# ######################################################################

def precision_recall_f1(discovered_edges, theoretical_edges):
    """Compute P/R/F1 treating theory as ground truth."""
    tp = len(discovered_edges & theoretical_edges)
    fp = len(discovered_edges - theoretical_edges)
    fn = len(theoretical_edges - discovered_edges)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)
           if (precision + recall) > 0 else 0.0)
    return precision, recall, f1, tp, fp, fn


def structural_hamming_distance(discovered_edges, theoretical_edges, n_bits):
    """SHD = |extra edges| + |missing edges| + |reversed edges|."""
    extra = discovered_edges - theoretical_edges
    missing = theoretical_edges - discovered_edges

    # Check for reversed edges
    reversed_edges = set()
    for (a, b) in extra:
        if (b, a) in missing:
            reversed_edges.add((a, b))

    shd = len(extra) + len(missing) - len(reversed_edges)
    max_possible = n_bits * (n_bits - 1)  # all possible directed edges
    normalized = shd / max_possible if max_possible > 0 else 0.0

    return shd, normalized, len(reversed_edges)


# ######################################################################
#  SECTION 2: RUN PROBE
# ######################################################################

def run_probe(checkpoints_dir, device='cuda'):
    """Run Q3 probe."""
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

    extractor = TriadicExtractor(checkpoints_dir)
    ckpts = extractor.discover_checkpoints(checkpoints_dir)
    if not ckpts:
        print("ERROR: No checkpoints found.")
        return None
    last_ckpt = ckpts[-1][1]  # (step, path) tuple
    snapshot = extractor.extract(last_ckpt, concepts, device=device)

    # Run at multiple confidence thresholds
    thresholds = [0.7, 0.8, 0.85, 0.9, 0.95]
    results_per_threshold = []

    for thresh in thresholds:
        bd = BitDiscovery(dep_confidence=thresh)
        discovery = bd.discover(snapshot)

        disc_edges = set()
        for dep in discovery.discovered_deps:
            disc_edges.add((dep.bit_parent, dep.bit_child))

        p, r, f1, tp, fp, fn = precision_recall_f1(disc_edges, theo_edges)
        shd, shd_norm, n_reversed = structural_hamming_distance(
            disc_edges, theo_edges, discovery.n_active_bits)

        results_per_threshold.append({
            'threshold': thresh,
            'discovered_edges': len(disc_edges),
            'precision': round(p, 4),
            'recall': round(r, 4),
            'f1': round(f1, 4),
            'tp': tp, 'fp': fp, 'fn': fn,
            'shd': shd,
            'shd_normalized': round(shd_norm, 4),
            'reversed_edges': n_reversed,
        })

    # Full discovery at default threshold for detailed analysis
    bd_default = BitDiscovery()
    discovery_default = bd_default.discover(snapshot)

    return results_per_threshold, discovery_default, snapshot


def analyze(results_per_threshold, discovery, snapshot):
    """Analyze DAG comparison."""
    print("=" * 70)
    print("Q3: Does the discovered DAG match the theoretical DAG?")
    print("=" * 70)

    print(f"\n  Theoretical edges: {len(theo_edges)}")
    print(f"  Active bits in model: {discovery.n_active_bits}")

    # ROC-like table across thresholds
    print("\n  --- Precision/Recall across confidence thresholds ---\n")
    print(f"  {'Threshold':<12} {'Edges':<8} {'Prec':<8} {'Rec':<8} "
          f"{'F1':<8} {'SHD':<8}")
    print("  " + "-" * 52)

    best_f1 = 0
    best_result = None
    for r in results_per_threshold:
        print(f"  {r['threshold']:<12.2f} {r['discovered_edges']:<8d} "
              f"{r['precision']:<8.3f} {r['recall']:<8.3f} "
              f"{r['f1']:<8.3f} {r['shd']:<8d}")
        if r['f1'] > best_f1:
            best_f1 = r['f1']
            best_result = r

    # Random baseline: how does a random graph compare?
    rng = random.Random(42)
    n_bits = discovery.n_active_bits
    n_random_trials = 1000
    random_f1s = []

    for _ in range(n_random_trials):
        n_edges = len(theo_edges)
        rand_edges = set()
        for _ in range(n_edges):
            a = rng.randint(0, n_bits - 1)
            b = rng.randint(0, n_bits - 1)
            if a != b:
                rand_edges.add((a, b))
        _, _, f1, _, _, _ = precision_recall_f1(rand_edges, theo_edges)
        random_f1s.append(f1)

    random_mean_f1 = sum(random_f1s) / len(random_f1s)
    random_p95 = sorted(random_f1s)[int(0.95 * len(random_f1s))]
    n_better = sum(1 for f in random_f1s if f >= best_f1)
    empirical_p = (n_better + 1) / (n_random_trials + 1)

    print(f"\n  --- Random baseline (same edge count) ---")
    print(f"  Random mean F1: {random_mean_f1:.3f}, p95: {random_p95:.3f}")
    print(f"  Best model F1: {best_f1:.3f}")
    print(f"  Empirical p: {empirical_p:.4f}")

    # Register p-value
    reg_path = os.path.join(STATS_DIR, 'p_values_registry.json')
    register_pvalue('neural_dag', 'q3_dag_f1_vs_random', empirical_p,
                    notes=f'best_f1={best_f1:.3f}, n_edges={len(theo_edges)}',
                    path=reg_path)

    # Top discovered edges not in theory
    disc_default = set()
    for dep in discovery.discovered_deps:
        disc_default.add((dep.bit_parent, dep.bit_child))

    novel_edges = disc_default - theo_edges
    print(f"\n  --- Novel edges (in model, not in theory): {len(novel_edges)} ---\n")
    shown = 0
    for dep in sorted(discovery.discovered_deps,
                      key=lambda d: d.confidence, reverse=True):
        edge = (dep.bit_parent, dep.bit_child)
        if edge in novel_edges and shown < 10:
            p_name = bit_to_name.get(dep.bit_parent, f'bit{dep.bit_parent}')
            c_name = bit_to_name.get(dep.bit_child, f'bit{dep.bit_child}')
            print(f"  {p_name} -> {c_name} (conf={dep.confidence:.3f})")
            shown += 1

    # Interpretation
    print("\n  --- Interpretation ---\n")
    if best_f1 > 0.5 and empirical_p < 0.05:
        print("  POSITIVE: Model DAG significantly matches theory.")
        print("  Confounder: co-occurrence in training data.")
        verdict = 'positive_with_caveats'
    elif best_f1 > 0.2:
        print("  MIXED: Partial overlap, some edges match.")
        verdict = 'mixed'
    else:
        print("  NULL: Model DAG does not resemble theoretical DAG.")
        verdict = 'null'

    results = {
        'theoretical_edges': len(theo_edges),
        'roc_table': results_per_threshold,
        'best_f1': round(best_f1, 4),
        'best_threshold': best_result['threshold'] if best_result else None,
        'random_baseline_mean_f1': round(random_mean_f1, 4),
        'empirical_p': round(empirical_p, 4),
        'n_active_bits': discovery.n_active_bits,
        'n_dead_bits': discovery.n_dead_bits,
        'verdict': verdict,
    }
    return results


# ######################################################################
#  SECTION 3: MAIN
# ######################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Q3: DAG probe')
    parser.add_argument('--checkpoints', required=True)
    parser.add_argument('--device', default='cuda',
                        help='Device (cuda or cpu)')
    args = parser.parse_args()

    if not HAS_REPTIMELINE:
        print("=" * 70)
        print("Q3: DAG Probe — reptimeline NOT INSTALLED")
        print("=" * 70)
        print("\nInstall with: pip install reptimeline")
        sys.exit(1)

    result = run_probe(args.checkpoints, args.device)
    if result is None:
        sys.exit(1)

    results_per_threshold, discovery, snapshot = result
    results = analyze(results_per_threshold, discovery, snapshot)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_path = os.path.join(RESULTS_DIR, 'q3_dag.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to: {out_path}")
