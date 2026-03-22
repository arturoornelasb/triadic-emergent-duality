"""Q6: Can the framework be discovered without anchors?

Probe: Run BitDiscovery + AutoLabeler on a model trained WITHOUT
explicit anchor supervision. If the discovered structure (duals,
layers, DAG) correlates with the theoretical framework, the structure
may be intrinsic rather than imposed by training.

Caveat: AutoLabeler uses embeddings or LLM, both of which carry
their own biases. A label match could reflect shared training data.

Requiere: pip install reptimeline
Usage: python q6_probe_unsupervised.py --checkpoints <dir> --embeddings <path>
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
MODEL_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'model'))
sys.path.insert(0, STATS_DIR)
sys.path.insert(0, MODEL_DIR)

from registry import register_pvalue

try:
    from reptimeline import BitDiscovery, PrimitiveOverlay
    from reptimeline.autolabel import AutoLabeler
    from reptimeline.reconcile import Reconciler
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
bit_to_name = {p.get('bit'): p['nombre'] for p in prims if p.get('bit') is not None}


# ######################################################################
#  SECTION 1: NORMALIZED MUTUAL INFORMATION
# ######################################################################

def nmi(labels_a, labels_b):
    """Normalized Mutual Information between two label assignments.

    Both inputs are lists of cluster labels (same length).
    """
    from collections import Counter

    n = len(labels_a)
    if n == 0:
        return 0.0

    ca = Counter(labels_a)
    cb = Counter(labels_b)
    joint = Counter(zip(labels_a, labels_b))

    # Entropy
    def entropy(counts, total):
        h = 0.0
        for c in counts.values():
            if c > 0:
                p = c / total
                h -= p * math.log(p)
        return h

    ha = entropy(ca, n)
    hb = entropy(cb, n)

    # Mutual information
    mi = 0.0
    for (a, b), count in joint.items():
        if count > 0:
            p_ab = count / n
            p_a = ca[a] / n
            p_b = cb[b] / n
            mi += p_ab * math.log(p_ab / (p_a * p_b))

    denom = (ha + hb) / 2
    if denom < 1e-12:
        return 0.0
    return mi / denom


# ######################################################################
#  SECTION 2: RUN PROBE
# ######################################################################

def run_probe(checkpoints_dir, embeddings_path=None, device='cuda'):
    """Run Q6 probe."""
    if not HAS_REPTIMELINE:
        return None

    # Load concepts from gold primes
    gold_path = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'model', 'gold_primes_65.json'))
    if os.path.exists(gold_path):
        with open(gold_path, 'r', encoding='utf-8') as f:
            concepts = list(json.load(f).keys())
        print(f'  Concepts from gold_primes_65.json: {len(concepts)}')
    else:
        print('  ERROR: gold_primes_65.json not found')
        return None

    extractor = TriadicExtractor(checkpoints_dir)
    ckpts = extractor.discover_checkpoints(checkpoints_dir)
    if not ckpts:
        print("ERROR: No checkpoints found.")
        return None
    last_ckpt = ckpts[-1][1]  # (step, path) tuple
    snapshot = extractor.extract(last_ckpt, concepts, device=device)

    # Discover structure without theoretical guidance
    bd = BitDiscovery()
    discovery = bd.discover(snapshot)

    # Auto-label discovered bits
    labeler = AutoLabeler()
    embeddings = None
    if embeddings_path and os.path.exists(embeddings_path):
        with open(embeddings_path, 'r', encoding='utf-8') as f:
            emb_data = json.load(f)
        # Convert to numpy-like lists (AutoLabeler handles this)
        embeddings = emb_data

    if embeddings:
        try:
            import numpy as np
            emb_np = {k: np.array(v) for k, v in embeddings.items()}
            labels = labeler.label_by_embedding(discovery, emb_np)
        except ImportError:
            labels = []
    else:
        labels = []

    # Reconcile with theory
    overlay = PrimitiveOverlay(
        primitivos_path=os.path.join(DATA_DIR, 'primitivos.json')
    )
    reconciler = Reconciler(overlay=overlay)
    reconciliation = reconciler.reconcile(discovery, snapshot.codes)

    return discovery, labels, reconciliation, snapshot


def analyze(discovery, labels, reconciliation, snapshot):
    """Analyze unsupervised discovery results."""
    print("=" * 70)
    print("Q6: Unsupervised structure discovery")
    print("=" * 70)

    n_active = discovery.n_active_bits
    n_dead = discovery.n_dead_bits
    n_duals = len(discovery.discovered_duals)
    n_deps = len(discovery.discovered_deps)
    n_triadic = len(discovery.discovered_triadic_deps)

    print(f"\n  Active bits: {n_active}, Dead bits: {n_dead}")
    print(f"  Discovered duals: {n_duals}")
    print(f"  Discovered dependencies: {n_deps}")
    print(f"  Discovered triadic deps: {n_triadic}")

    # Reconciliation summary
    agreement = reconciliation.agreement_score
    n_mismatches = reconciliation.metadata.get('total_mismatches', 0)
    n_critical = reconciliation.metadata.get('critical_mismatches', 0)

    print(f"\n  Agreement score: {agreement:.3f}")
    print(f"  Total mismatches: {n_mismatches} (critical: {n_critical})")

    # Dual matching
    print("\n  --- Dual matching ---\n")
    dual_mismatches = reconciliation.dual_mismatches
    theo_duals = prim_data.get('ejes_duales', [])
    n_matched_duals = len(theo_duals) - len([
        dm for dm in dual_mismatches
        if dm.mismatch_type == 'missing_in_model'
    ])
    print(f"  Matched: {n_matched_duals}/{len(theo_duals)} theoretical duals")

    # Layer NMI (if hierarchy was discovered)
    print("\n  --- Layer structure ---\n")
    if discovery.discovered_hierarchy:
        discovered_layers = {}
        for h in discovery.discovered_hierarchy:
            discovered_layers[h.bit_index] = h.layer

        # Compare with theory for bits that have both
        theo_labels = []
        disc_labels = []
        for p in prims:
            bit = p.get('bit')
            if bit is not None and bit in discovered_layers:
                theo_labels.append(p['capa'])
                disc_labels.append(discovered_layers[bit])

        if theo_labels:
            layer_nmi = nmi(theo_labels, disc_labels)
            print(f"  Layer NMI (theory vs discovered): {layer_nmi:.3f}")
        else:
            layer_nmi = 0.0
            print("  No overlapping bits for layer comparison.")
    else:
        layer_nmi = 0.0
        print("  No hierarchy discovered.")

    # Auto-label matching
    print("\n  --- Auto-labels ---\n")
    if labels:
        matched_labels = 0
        for bl in labels[:20]:
            theo_name = bit_to_name.get(bl.bit_index, '???')
            match = 'MATCH' if bl.label.lower() in theo_name.lower() else ''
            if match:
                matched_labels += 1
            print(f"  bit{bl.bit_index}: '{bl.label}' "
                  f"(conf={bl.confidence:.2f}) "
                  f"[theory: {theo_name}] {match}")
        print(f"\n  Label matches: {matched_labels}/{min(len(labels), 20)}")
    else:
        matched_labels = 0
        print("  No auto-labels generated (need embeddings).")

    # Register
    reg_path = os.path.join(STATS_DIR, 'p_values_registry.json')
    # Agreement score as a summary metric (no p-value per se)
    register_pvalue('neural_unsup', 'q6_agreement_score', 1.0,
                    notes=f'agreement={agreement:.3f}, nmi={layer_nmi:.3f}',
                    path=reg_path)

    # Interpretation
    print("\n  --- Interpretation ---\n")
    if agreement > 0.6 and layer_nmi > 0.3:
        print("  POSITIVE: Unsupervised discovery partially recovers theory.")
        print("  Confounder: shared training data, embedding bias.")
        verdict = 'positive_with_caveats'
    elif agreement > 0.3:
        print("  MIXED: Some structural overlap, but significant divergences.")
        verdict = 'mixed'
    else:
        print("  NULL: Unsupervised structure does not resemble theory.")
        verdict = 'null'

    results = {
        'n_active_bits': n_active,
        'n_dead_bits': n_dead,
        'discovered_duals': n_duals,
        'discovered_deps': n_deps,
        'discovered_triadic': n_triadic,
        'agreement_score': round(agreement, 4),
        'n_mismatches': n_mismatches,
        'n_critical_mismatches': n_critical,
        'matched_duals': n_matched_duals,
        'layer_nmi': round(layer_nmi, 4),
        'matched_labels': matched_labels,
        'verdict': verdict,
    }
    return results


# ######################################################################
#  SECTION 3: MAIN
# ######################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Q6: Unsupervised probe')
    parser.add_argument('--checkpoints', required=True)
    parser.add_argument('--embeddings', default=None,
                        help='JSON with concept embeddings for auto-labeling')
    parser.add_argument('--device', default='cuda',
                        help='Device (cuda or cpu)')
    args = parser.parse_args()

    if not HAS_REPTIMELINE:
        print("=" * 70)
        print("Q6: Unsupervised Probe — reptimeline NOT INSTALLED")
        print("=" * 70)
        print("\nInstall with: pip install reptimeline")
        sys.exit(1)

    result = run_probe(args.checkpoints, args.embeddings, args.device)
    if result is None:
        sys.exit(1)

    discovery, labels, reconciliation, snapshot = result
    results = analyze(discovery, labels, reconciliation, snapshot)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_path = os.path.join(RESULTS_DIR, 'q6_unsupervised.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to: {out_path}")
