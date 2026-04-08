"""Q13: Empirical Markov Blanket Test — MI ≈ 0 between coprime interiors.

The algebraic proof (FTA) guarantees gcd(μ₁, μ₂) = 1 for concept interiors
given the blanket. This probe tests whether the LEARNED 72-bit codes from
TriadicGPT empirically satisfy this property.

Five tests:
  T1. Bit-pair MI matrix: MI(bit_i, bit_j) across all concepts
  T2. Layer-level MI heatmap: average MI between algebraic layers
  T3. DAG structure: MI for connected vs coprime bit pairs
  T4. Per-pair blanket test: correlation(|interior₁|, |interior₂| | blanket)
  T5. Null model: shuffled codes establish significance (permutation test)

Roadmap #13.

Usage:
  python q13_probe_markov_blanket.py --checkpoint <best.pt> --device cuda
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json
import argparse
import math
from collections import defaultdict

import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'model'))
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))
RESULTS_DIR = os.path.join(SCRIPT_DIR, 'results')
sys.path.insert(0, MODEL_DIR)


# ======================================================================
# Mutual Information for binary variables
# ======================================================================

def mi_binary(x, y):
    """Mutual information between two binary arrays. Returns MI in bits."""
    n = len(x)
    if n == 0:
        return 0.0
    # 2x2 contingency table
    c00 = c01 = c10 = c11 = 0
    for xi, yi in zip(x, y):
        if xi == 0:
            if yi == 0:
                c00 += 1
            else:
                c01 += 1
        else:
            if yi == 0:
                c10 += 1
            else:
                c11 += 1
    mi = 0.0
    for count, px_idx, py_idx in [
        (c00, c00 + c01, c00 + c10),
        (c01, c00 + c01, c01 + c11),
        (c10, c10 + c11, c00 + c10),
        (c11, c10 + c11, c01 + c11),
    ]:
        if count == 0:
            continue
        pxy = count / n
        px = (c00 + c01 if px_idx == c00 + c01 else c10 + c11) / n
        py = (c00 + c10 if py_idx == c00 + c10 else c01 + c11) / n
        if px > 0 and py > 0:
            mi += pxy * math.log2(pxy / (px * py))
    return max(mi, 0.0)  # clip numerical noise


def mi_binary_fast(codes_matrix):
    """Compute full MI matrix for binary code matrix (N_concepts x N_bits).
    Returns N_bits x N_bits MI matrix."""
    n_concepts, n_bits = codes_matrix.shape
    mi_matrix = np.zeros((n_bits, n_bits))

    # Pre-compute marginals
    p1 = codes_matrix.mean(axis=0)  # P(bit=1) for each bit
    p0 = 1.0 - p1

    for i in range(n_bits):
        for j in range(i + 1, n_bits):
            # Joint distribution
            both_1 = np.sum(codes_matrix[:, i] & codes_matrix[:, j]) / n_concepts
            both_0 = np.sum((1 - codes_matrix[:, i]) & (1 - codes_matrix[:, j])) / n_concepts
            i1_j0 = p1[i] - both_1
            i0_j1 = p1[j] - both_1

            mi = 0.0
            for pxy, px, py in [
                (both_0, p0[i], p0[j]),
                (i0_j1, p0[i], p1[j]),
                (i1_j0, p1[i], p0[j]),
                (both_1, p1[i], p1[j]),
            ]:
                if pxy > 1e-12 and px > 1e-12 and py > 1e-12:
                    mi += pxy * math.log2(pxy / (px * py))

            mi_matrix[i, j] = max(mi, 0.0)
            mi_matrix[j, i] = mi_matrix[i, j]

    return mi_matrix


# ======================================================================
# DAG utilities
# ======================================================================

def load_primitivos():
    """Load primitivos.json, return list and lookup dicts."""
    path = os.path.join(DATA_DIR, 'primitivos.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    prims = data['primitivos']
    by_name = {p['nombre']: p for p in prims}
    by_bit = {p['bit']: p for p in prims}
    return prims, by_name, by_bit, data


def build_dag(prims, by_name):
    """Build adjacency list from dependency DAG. Returns {bit: set(dep_bits)}."""
    dag = defaultdict(set)
    for p in prims:
        bit = p['bit']
        for dep_name in p.get('deps', []):
            if dep_name in by_name:
                dep_bit = by_name[dep_name]['bit']
                dag[bit].add(dep_bit)
    return dag


def transitive_closure(dag, n_bits=72):
    """Compute transitive closure: for each bit, all bits reachable (ancestors + descendants)."""
    # Build bidirectional graph
    graph = defaultdict(set)
    for bit, deps in dag.items():
        for d in deps:
            graph[bit].add(d)
            graph[d].add(bit)

    # BFS from each bit
    reachable = {}
    for start in range(n_bits):
        visited = set()
        queue = [start]
        while queue:
            node = queue.pop(0)
            if node in visited:
                continue
            visited.add(node)
            for neighbor in graph.get(node, set()):
                if neighbor not in visited:
                    queue.append(neighbor)
        visited.discard(start)
        reachable[start] = visited

    return reachable


def classify_bit_pairs(prims, by_name, by_bit, n_bits=72):
    """Classify each bit pair by DAG relationship."""
    dag = build_dag(prims, by_name)
    reachable = transitive_closure(dag, n_bits)

    # Direct edges (parent-child)
    direct_edges = set()
    for bit, deps in dag.items():
        for d in deps:
            direct_edges.add((min(bit, d), max(bit, d)))

    # Layer lookup
    layer_of = {}
    for p in prims:
        layer_of[p['bit']] = p['capa']

    # Dual pairs
    dual_pairs = set()
    for p in prims:
        if 'dual' in p:
            dual_name = p['dual']
            if dual_name in by_name:
                dual_bit = by_name[dual_name]['bit']
                dual_pairs.add((min(p['bit'], dual_bit), max(p['bit'], dual_bit)))

    classifications = {}
    valid_bits = set(p['bit'] for p in prims)
    for i in sorted(valid_bits):
        for j in sorted(valid_bits):
            if j <= i:
                continue
            pair = (i, j)
            if pair in direct_edges:
                cat = 'parent-child'
            elif pair in dual_pairs:
                cat = 'dual-axis'
            elif j in reachable.get(i, set()):
                cat = 'dag-connected'
            elif layer_of.get(i) == layer_of.get(j):
                cat = 'same-layer-coprime'
            elif abs(layer_of.get(i, 0) - layer_of.get(j, 0)) == 1:
                cat = 'adjacent-layer-coprime'
            else:
                cat = 'distant-coprime'
            classifications[pair] = cat

    return classifications, layer_of


# ======================================================================
# T4: Partial correlation test (correct Markov blanket test)
# ======================================================================

def partial_correlation_test(codes_matrix, dag, prims, n_bits=72):
    """Test Markov property via partial correlations.

    The DAG Markov property says: conditioning on all other variables,
    non-adjacent nodes should have partial correlation ~ 0.

    Uses precision matrix: P = R^{-1}, partial_corr(i,j) = -P_ij/sqrt(P_ii*P_jj)
    """
    # Find active (non-constant) bits
    stds = codes_matrix.std(axis=0)
    active_bits = [i for i in range(n_bits) if stds[i] > 0.01]
    n_active = len(active_bits)

    if n_active < 5:
        return {'error': 'too few active bits'}

    # Correlation matrix on active bits only
    sub = codes_matrix[:, active_bits].astype(float)
    R = np.corrcoef(sub.T)

    # Regularize to ensure invertibility
    R += np.eye(n_active) * 1e-6

    try:
        P = np.linalg.inv(R)
    except np.linalg.LinAlgError:
        return {'error': 'singular correlation matrix'}

    # Partial correlations
    partial = np.zeros((n_active, n_active))
    for i in range(n_active):
        for j in range(n_active):
            if i != j:
                partial[i, j] = -P[i, j] / math.sqrt(abs(P[i, i] * P[j, j]))

    # Map back to original bit indices
    # Direct edges in DAG
    direct_edges = set()
    for bit, deps in dag.items():
        for d in deps:
            direct_edges.add((min(bit, d), max(bit, d)))

    # Classify partial correlations
    edge_partials = []
    non_edge_partials = []
    for ai in range(n_active):
        for aj in range(ai + 1, n_active):
            bi, bj = active_bits[ai], active_bits[aj]
            pair = (min(bi, bj), max(bi, bj))
            pc = abs(partial[ai, aj])
            if pair in direct_edges:
                edge_partials.append(pc)
            else:
                non_edge_partials.append(pc)

    result = {
        'n_active_bits': n_active,
        'edge_partial_mean': float(np.mean(edge_partials)) if edge_partials else 0,
        'edge_partial_std': float(np.std(edge_partials)) if edge_partials else 0,
        'non_edge_partial_mean': float(np.mean(non_edge_partials)) if non_edge_partials else 0,
        'non_edge_partial_std': float(np.std(non_edge_partials)) if non_edge_partials else 0,
        'n_edges': len(edge_partials),
        'n_non_edges': len(non_edge_partials),
    }

    # Near-zero threshold: |partial| < 0.05 considered "independent"
    if non_edge_partials:
        near_zero = sum(1 for p in non_edge_partials if p < 0.05)
        result['non_edge_near_zero_frac'] = near_zero / len(non_edge_partials)
        result['non_edge_below_01'] = sum(1 for p in non_edge_partials if p < 0.10) / len(non_edge_partials)

    # Ratio test: edge partials should be larger than non-edge
    if edge_partials and non_edge_partials:
        from scipy.stats import mannwhitneyu
        stat, pval = mannwhitneyu(edge_partials, non_edge_partials, alternative='greater')
        result['mann_whitney_U'] = float(stat)
        result['mann_whitney_p'] = float(pval)
        result['ratio'] = float(np.mean(edge_partials) / max(np.mean(non_edge_partials), 1e-10))

    return result


def dag_distance_vs_mi(mi_matrix, dag, prims, by_name, n_bits=72):
    """Compute shortest DAG distance between all bit pairs and correlate with MI."""
    # Build bidirectional graph
    graph = defaultdict(set)
    for bit, deps in dag.items():
        for d in deps:
            graph[bit].add(d)
            graph[d].add(bit)

    valid_bits = sorted(set(p['bit'] for p in prims if p['bit'] < n_bits))

    # BFS shortest path for all pairs
    distances = {}
    for start in valid_bits:
        dist = {start: 0}
        queue = [start]
        while queue:
            node = queue.pop(0)
            for neighbor in graph.get(node, set()):
                if neighbor not in dist and neighbor in set(valid_bits):
                    dist[neighbor] = dist[node] + 1
                    queue.append(neighbor)
        for end in valid_bits:
            if end > start and end in dist:
                distances[(start, end)] = dist[end]

    # Correlate distance with MI
    dists = []
    mis = []
    for (i, j), d in distances.items():
        if i < n_bits and j < n_bits:
            dists.append(d)
            mis.append(mi_matrix[i, j])

    dists = np.array(dists)
    mis = np.array(mis)

    if len(dists) > 0:
        r = float(np.corrcoef(dists, mis)[0, 1])
        # Per-distance mean MI
        per_dist = {}
        for d in sorted(set(dists)):
            mask = dists == d
            per_dist[int(d)] = {'mean_mi': float(mis[mask].mean()),
                                'std_mi': float(mis[mask].std()),
                                'n': int(mask.sum())}
        return {
            'correlation': r,
            'n_pairs': len(dists),
            'per_distance': per_dist,
        }
    return {'error': 'no valid pairs'}


# ======================================================================
# T5: Null model
# ======================================================================

def null_model_mi(codes_matrix, n_perm=1000):
    """Shuffle codes and compute mean MI for null distribution."""
    rng = np.random.RandomState(42)
    n_concepts, n_bits = codes_matrix.shape
    null_mean_mis = []

    for _ in range(n_perm):
        shuffled = codes_matrix.copy()
        for col in range(n_bits):
            rng.shuffle(shuffled[:, col])
        # Compute mean off-diagonal MI (sample 200 random pairs for speed)
        mi_sum = 0.0
        n_sample = 200
        pairs = [(rng.randint(n_bits), rng.randint(n_bits)) for _ in range(n_sample)]
        count = 0
        for i, j in pairs:
            if i == j:
                continue
            mi_sum += mi_binary(shuffled[:, i].tolist(), shuffled[:, j].tolist())
            count += 1
        null_mean_mis.append(mi_sum / max(count, 1))

    return null_mean_mis


# ======================================================================
# Plotting
# ======================================================================

def plot_results(mi_matrix, layer_of, classifications, results, plots_dir):
    """Generate diagnostic plots."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    os.makedirs(plots_dir, exist_ok=True)
    prims_bits = sorted(layer_of.keys())

    # --- Plot 1: MI matrix sorted by layer ---
    sorted_bits = sorted(prims_bits, key=lambda b: (layer_of[b], b))
    idx = [b for b in sorted_bits if b < mi_matrix.shape[0]]
    mi_sub = mi_matrix[np.ix_(idx, idx)]

    fig, ax = plt.subplots(figsize=(12, 10))
    im = ax.imshow(mi_sub, cmap='hot', aspect='equal', interpolation='nearest')
    plt.colorbar(im, ax=ax, label='MI (bits)')

    # Layer boundaries
    boundaries = []
    prev_layer = None
    for pos, bit in enumerate(idx):
        if layer_of[bit] != prev_layer:
            if prev_layer is not None:
                boundaries.append(pos - 0.5)
            prev_layer = layer_of[bit]
    for b in boundaries:
        ax.axhline(b, color='cyan', lw=1, alpha=0.7)
        ax.axvline(b, color='cyan', lw=1, alpha=0.7)

    ax.set_title('Bit-pair MI Matrix (sorted by layer)')
    ax.set_xlabel('Bit (sorted by layer)')
    ax.set_ylabel('Bit (sorted by layer)')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'mi_matrix_by_layer.png'), dpi=150)
    plt.close()
    print(f'    Plot: mi_matrix_by_layer.png')

    # --- Plot 2: Layer-level MI heatmap ---
    layer_mi = results.get('layer_mi', {})
    layers = sorted(set(layer_of.values()))
    n_layers = len(layers)
    layer_grid = np.zeros((n_layers, n_layers))
    for i, li in enumerate(layers):
        for j, lj in enumerate(layers):
            key = f'L{li}_L{lj}'
            layer_grid[i, j] = layer_mi.get(key, 0)

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(layer_grid, cmap='YlOrRd', aspect='equal')
    plt.colorbar(im, ax=ax, label='Mean MI (bits)')
    ax.set_xticks(range(n_layers))
    ax.set_xticklabels([f'L{l}' for l in layers])
    ax.set_yticks(range(n_layers))
    ax.set_yticklabels([f'L{l}' for l in layers])
    for i in range(n_layers):
        for j in range(n_layers):
            ax.text(j, i, f'{layer_grid[i,j]:.4f}', ha='center', va='center', fontsize=7)
    ax.set_title('Mean MI Between Algebraic Layers')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'layer_mi_heatmap.png'), dpi=150)
    plt.close()
    print(f'    Plot: layer_mi_heatmap.png')

    # --- Plot 3: MI distribution by DAG category ---
    categories = defaultdict(list)
    for (i, j), cat in classifications.items():
        if i < mi_matrix.shape[0] and j < mi_matrix.shape[0]:
            categories[cat].append(mi_matrix[i, j])

    fig, ax = plt.subplots(figsize=(12, 6))
    cat_order = ['parent-child', 'dual-axis', 'dag-connected',
                 'same-layer-coprime', 'adjacent-layer-coprime', 'distant-coprime']
    cat_data = [categories.get(c, []) for c in cat_order]
    cat_labels = [f'{c}\n(n={len(d)})' for c, d in zip(cat_order, cat_data)]

    bp = ax.boxplot(cat_data, labels=cat_labels, patch_artist=True)
    colors = ['#e74c3c', '#f39c12', '#3498db', '#95a5a6', '#bdc3c7', '#2ecc71']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax.set_ylabel('MI (bits)')
    ax.set_title('MI Distribution by DAG Relationship Category')
    ax.axhline(0, color='gray', ls='--', lw=0.5)

    # Add null model line if available
    null_mean = results.get('null_model', {}).get('null_mean_mi')
    if null_mean is not None:
        ax.axhline(null_mean, color='green', ls='--', lw=1.5,
                   label=f'Null model mean: {null_mean:.5f}')
        ax.legend()

    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'mi_by_dag_category.png'), dpi=150)
    plt.close()
    print(f'    Plot: mi_by_dag_category.png')

    # --- Plot 4: Distance vs MI ---
    dist_mi = results.get('distance_vs_mi', {})
    if 'per_distance' in dist_mi:
        fig, ax = plt.subplots(figsize=(8, 5))
        dists = sorted(dist_mi['per_distance'].keys(), key=int)
        means = [dist_mi['per_distance'][d]['mean_mi'] for d in dists]
        stds = [dist_mi['per_distance'][d]['std_mi'] for d in dists]
        ns = [dist_mi['per_distance'][d]['n'] for d in dists]
        ax.bar([int(d) for d in dists], means, yerr=stds, alpha=0.7,
               color='steelblue', capsize=3)
        for d, m, n in zip(dists, means, ns):
            ax.text(int(d), m + 0.001, f'n={n}', ha='center', fontsize=7)
        ax.set_xlabel('DAG Hop Distance')
        ax.set_ylabel('Mean MI (bits)')
        r = dist_mi.get('correlation', 0)
        ax.set_title(f'MI vs DAG Distance (r={r:.3f})')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(plots_dir, 'distance_vs_mi.png'), dpi=150)
        plt.close()
        print(f'    Plot: distance_vs_mi.png')


# ======================================================================
# Main
# ======================================================================

def main():
    parser = argparse.ArgumentParser(description='Q13: Markov Blanket MI Probe')
    parser.add_argument('--checkpoint', type=str, required=True,
                        help='Path to best.pt checkpoint')
    parser.add_argument('--device', type=str, default='cpu')
    parser.add_argument('--gold-file', type=str, default='gold_extended_v7.json')
    parser.add_argument('--n-perm', type=int, default=1000,
                        help='Number of null model permutations')
    parser.add_argument('--plots-dir', type=str, default=None)
    parser.add_argument('--label', type=str, default='',
                        help='Label for output files (e.g. v8, v9)')
    args = parser.parse_args()

    print('=' * 60)
    print('  Q13: Empirical Markov Blanket Test — MI ≈ 0')
    print('  Roadmap #13')
    print('=' * 60)

    # --- Load concepts ---
    gold_path = os.path.join(MODEL_DIR, args.gold_file)
    with open(gold_path, 'r', encoding='utf-8') as f:
        gold = json.load(f)
    concepts = list(gold.keys())
    print(f'\n  Concepts: {len(concepts)}')

    # --- Load primitivos and build DAG ---
    prims, by_name, by_bit, prim_data = load_primitivos()
    classifications, layer_of = classify_bit_pairs(prims, by_name, by_bit)
    print(f'  Primitivos: {len(prims)}')
    print(f'  Bit pairs classified: {len(classifications)}')

    cat_counts = defaultdict(int)
    for cat in classifications.values():
        cat_counts[cat] += 1
    for cat, cnt in sorted(cat_counts.items()):
        print(f'    {cat}: {cnt}')

    # --- Extract codes ---
    print(f'\n  Extracting codes from {os.path.basename(args.checkpoint)}...')
    from triadic_extractor import TriadicExtractor
    extractor = TriadicExtractor(n_bits=72)
    snap = extractor.extract(args.checkpoint, concepts, device=args.device)

    extracted_concepts = list(snap.codes.keys())
    n_concepts = len(extracted_concepts)
    print(f'  Extracted: {n_concepts} concepts')

    # Build binary matrix (N x 72)
    n_bits = 72
    codes_matrix = np.zeros((n_concepts, n_bits), dtype=np.int32)
    for idx, concept in enumerate(extracted_concepts):
        code = snap.codes[concept]
        for b in range(min(len(code), n_bits)):
            codes_matrix[idx, b] = code[b]

    active_per_bit = codes_matrix.mean(axis=0)
    dead_bits = np.sum(active_per_bit < 0.01) + np.sum(active_per_bit > 0.99)
    print(f'  Dead/saturated bits: {int(dead_bits)}/72')
    print(f'  Mean active bits per concept: {codes_matrix.sum(axis=1).mean():.1f}')

    results = {
        'checkpoint': os.path.basename(args.checkpoint),
        'n_concepts': n_concepts,
        'n_bits': n_bits,
        'dead_bits': int(dead_bits),
    }

    # === T1: Bit-pair MI matrix ===
    print('\n  T1: Computing 72x72 MI matrix...')
    mi_matrix = mi_binary_fast(codes_matrix)
    mean_mi = mi_matrix[np.triu_indices(n_bits, k=1)].mean()
    max_mi = mi_matrix[np.triu_indices(n_bits, k=1)].max()
    print(f'    Mean MI (all pairs): {mean_mi:.6f}')
    print(f'    Max MI: {max_mi:.6f}')

    results['mi_matrix_stats'] = {
        'mean': float(mean_mi),
        'max': float(max_mi),
        'std': float(mi_matrix[np.triu_indices(n_bits, k=1)].std()),
    }

    # === T2: Layer-level MI ===
    print('\n  T2: Layer-level MI...')
    layers = sorted(set(layer_of.values()))
    bits_by_layer = defaultdict(list)
    for bit, layer in layer_of.items():
        bits_by_layer[layer].append(bit)

    layer_mi = {}
    for li in layers:
        for lj in layers:
            mis = []
            for bi in bits_by_layer[li]:
                for bj in bits_by_layer[lj]:
                    if bi != bj and bi < n_bits and bj < n_bits:
                        mis.append(mi_matrix[bi, bj])
            key = f'L{li}_L{lj}'
            layer_mi[key] = float(np.mean(mis)) if mis else 0.0

    results['layer_mi'] = layer_mi

    print(f'    {"":>8}', end='')
    for lj in layers:
        print(f'  L{lj:>4}', end='')
    print()
    for li in layers:
        print(f'    L{li:<4}   ', end='')
        for lj in layers:
            key = f'L{li}_L{lj}'
            print(f'  {layer_mi[key]:.4f}', end='')
        print()

    # Check: non-adjacent layers should have lower MI
    adjacent_mis = []
    non_adjacent_mis = []
    for li in layers:
        for lj in layers:
            if li >= lj:
                continue
            key = f'L{li}_L{lj}'
            if abs(li - lj) == 1:
                adjacent_mis.append(layer_mi[key])
            elif abs(li - lj) >= 2:
                non_adjacent_mis.append(layer_mi[key])

    if adjacent_mis and non_adjacent_mis:
        print(f'\n    Adjacent layers mean MI:     {np.mean(adjacent_mis):.6f}')
        print(f'    Non-adjacent layers mean MI: {np.mean(non_adjacent_mis):.6f}')
        ratio = np.mean(non_adjacent_mis) / np.mean(adjacent_mis) if np.mean(adjacent_mis) > 0 else float('inf')
        print(f'    Ratio (non-adj/adj):         {ratio:.4f}')
        results['layer_mi_summary'] = {
            'adjacent_mean': float(np.mean(adjacent_mis)),
            'non_adjacent_mean': float(np.mean(non_adjacent_mis)),
            'ratio': float(ratio),
        }

    # === T3: MI by DAG category ===
    print('\n  T3: MI by DAG relationship...')
    cat_mis = defaultdict(list)
    for (i, j), cat in classifications.items():
        if i < n_bits and j < n_bits:
            cat_mis[cat].append(mi_matrix[i, j])

    cat_order = ['parent-child', 'dual-axis', 'dag-connected',
                 'same-layer-coprime', 'adjacent-layer-coprime', 'distant-coprime']
    results['dag_category_mi'] = {}
    for cat in cat_order:
        vals = cat_mis.get(cat, [])
        if vals:
            m = float(np.mean(vals))
            s = float(np.std(vals))
            print(f'    {cat:>25}: mean={m:.6f} std={s:.6f} n={len(vals)}')
            results['dag_category_mi'][cat] = {
                'mean': m, 'std': s, 'n': len(vals),
                'median': float(np.median(vals)),
                'max': float(np.max(vals)),
            }

    # Key test: coprime (distant) should be significantly lower than connected
    connected_vals = cat_mis.get('parent-child', []) + cat_mis.get('dag-connected', [])
    coprime_vals = cat_mis.get('distant-coprime', [])
    if connected_vals and coprime_vals:
        from scipy.stats import mannwhitneyu
        stat, pval = mannwhitneyu(connected_vals, coprime_vals, alternative='greater')
        print(f'\n    Mann-Whitney (connected > coprime): U={stat:.0f}, p={pval:.2e}')
        effect_size = np.mean(connected_vals) - np.mean(coprime_vals)
        print(f'    Effect size (mean diff): {effect_size:.6f}')
        results['t3_test'] = {
            'U_statistic': float(stat),
            'p_value': float(pval),
            'effect_size': float(effect_size),
            'connected_mean': float(np.mean(connected_vals)),
            'coprime_mean': float(np.mean(coprime_vals)),
        }

    # === T4: Partial correlation test (correct Markov test) ===
    print('\n  T4: Partial correlations (precision matrix)...')
    dag = build_dag(prims, by_name)
    pc = partial_correlation_test(codes_matrix, dag, prims)
    results['partial_correlation'] = pc

    if 'error' not in pc:
        print(f'    Active bits: {pc["n_active_bits"]}')
        print(f'    DAG edges:     |partial| mean = {pc["edge_partial_mean"]:.4f} (n={pc["n_edges"]})')
        print(f'    Non-edges:     |partial| mean = {pc["non_edge_partial_mean"]:.4f} (n={pc["n_non_edges"]})')
        if 'non_edge_near_zero_frac' in pc:
            print(f'    Non-edges |partial| < 0.05:   {pc["non_edge_near_zero_frac"]:.1%}')
            print(f'    Non-edges |partial| < 0.10:   {pc["non_edge_below_01"]:.1%}')
        if 'ratio' in pc:
            print(f'    Edge/non-edge ratio:           {pc["ratio"]:.2f}')
            print(f'    Mann-Whitney p:                {pc["mann_whitney_p"]:.2e}')
        markov_pass = pc.get('non_edge_near_zero_frac', 0) > 0.50
    else:
        print(f'    Error: {pc["error"]}')
        markov_pass = False

    # === T4b: DAG distance vs MI ===
    print('\n  T4b: DAG distance vs MI...')
    dist_mi = dag_distance_vs_mi(mi_matrix, dag, prims, by_name)
    results['distance_vs_mi'] = dist_mi

    if 'correlation' in dist_mi:
        print(f'    Distance-MI correlation: r = {dist_mi["correlation"]:.4f} (n={dist_mi["n_pairs"]})')
        print(f'    Per-distance mean MI:')
        for d, info in sorted(dist_mi['per_distance'].items()):
            print(f'      hop {d}: MI = {info["mean_mi"]:.6f} (n={info["n"]})')
        dist_pass = dist_mi['correlation'] < -0.10  # MI should decrease with distance
    else:
        dist_pass = False

    # === T5: Null model ===
    print(f'\n  T5: Null model ({args.n_perm} permutations)...')
    null_mis = null_model_mi(codes_matrix, n_perm=args.n_perm)
    null_mean = float(np.mean(null_mis))
    null_std = float(np.std(null_mis))
    print(f'    Null mean MI: {null_mean:.6f} ± {null_std:.6f}')

    # How many real coprime pairs exceed null?
    if coprime_vals:
        coprime_above_null = sum(1 for v in coprime_vals if v > null_mean + 2 * null_std)
        print(f'    Coprime pairs above null (2σ): {coprime_above_null}/{len(coprime_vals)}')
        coprime_mean = float(np.mean(coprime_vals))
        z_score = (coprime_mean - null_mean) / null_std if null_std > 0 else 0
        print(f'    Coprime mean vs null: z = {z_score:.2f}')
    else:
        coprime_above_null = 0
        z_score = 0.0

    results['null_model'] = {
        'null_mean_mi': null_mean,
        'null_std_mi': null_std,
        'coprime_above_null_2sigma': int(coprime_above_null) if coprime_vals else 0,
        'coprime_z_score': float(z_score),
        'n_permutations': args.n_perm,
    }

    # === Overall verdict ===
    print('\n' + '=' * 60)
    print('  SUMMARY')
    print('=' * 60)

    verdicts = []

    # T2: Layer hierarchy
    if 'layer_mi_summary' in results:
        r = results['layer_mi_summary']['ratio']
        v = r < 0.8  # non-adjacent should be notably less
        verdicts.append(('T2: Layer hierarchy (non-adj/adj < 0.8)', v, f'ratio={r:.3f}'))

    # T3: Connected > coprime
    if 't3_test' in results:
        p = results['t3_test']['p_value']
        v = p < 0.05
        verdicts.append(('T3: Connected > coprime MI', v, f'p={p:.2e}'))

    # T4: Partial correlations — non-edges near zero
    v = markov_pass
    nz = pc.get('non_edge_near_zero_frac', 0)
    verdicts.append(('T4: Non-edge |partial| < 0.05 (>50%)', v, f'{nz:.1%}'))

    # T4b: MI decreases with DAG distance
    v = dist_pass
    dr = dist_mi.get('correlation', 0)
    verdicts.append(('T4b: Distance-MI correlation < -0.10', v, f'r={dr:.3f}'))

    all_pass = all(v for _, v, _ in verdicts)
    for name, passed, detail in verdicts:
        status = 'PASS' if passed else 'FAIL'
        print(f'  {status:>4} | {name:<40} | {detail}')

    n_pass = sum(v for _, v, _ in verdicts)
    results['verdict'] = {
        'all_pass': bool(all_pass),
        'tests': {name: {'pass': bool(v), 'detail': detail} for name, v, detail in verdicts},
        'conclusion': 'POSITIVE' if all_pass else 'MIXED' if n_pass >= 2 else 'NEGATIVE',
    }

    print(f'\n  Overall: {results["verdict"]["conclusion"]}')
    if all_pass:
        print('  The learned codes empirically satisfy the Markov blanket property.')
    print('=' * 60)

    # === Save ===
    os.makedirs(RESULTS_DIR, exist_ok=True)
    suffix = f'_{args.label}' if args.label else ''
    out_path = os.path.join(RESULTS_DIR, f'q13_markov_blanket{suffix}.json')

    def jsonify(obj):
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, (np.float32, np.float64)):
            return float(obj)
        if isinstance(obj, (np.int32, np.int64)):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, dict):
            return {k: jsonify(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [jsonify(v) for v in obj]
        return obj

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(jsonify(results), f, indent=2)
    print(f'\n  Results saved: {out_path}')

    # === Plots ===
    if args.plots_dir is None:
        args.plots_dir = os.path.join(SCRIPT_DIR, '..', 'runs',
                                       f'q13_markov{suffix}', 'plots')
    try:
        plot_results(mi_matrix, layer_of, classifications, results, args.plots_dir)
    except Exception as e:
        print(f'  Plots failed: {e}')

    return results


if __name__ == '__main__':
    main()
