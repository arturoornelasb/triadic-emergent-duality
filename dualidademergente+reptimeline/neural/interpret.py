"""Consolidate and interpret all neural probe results (Q1-Q8).

Reads JSON results from neural/results/, builds a summary table of
coincidences and divergences, identifies confounders, and generates
recommendations for primitivos.json.

Solo stdlib: json, os, sys.
Usage: python interpret.py
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(SCRIPT_DIR, 'results')
STATS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'stats'))
sys.path.insert(0, STATS_DIR)

# ######################################################################
#  SECTION 0: LOAD ALL RESULTS
# ######################################################################

PROBES = {
    'Q1': {'file': 'q1_layer_order.json', 'question': 'Layer emergence order'},
    'Q2': {'file': 'q2_duals.json', 'question': 'Dual anti-correlation'},
    'Q3': {'file': 'q3_dag.json', 'question': 'DAG structure match'},
    'Q4': {'file': 'q4_triadic.json', 'question': 'Triadic S/C/E/A enrichment'},
    'Q5': {'file': 'q5_phases.json', 'question': 'Phase transition alignment'},
    'Q6': {'file': 'q6_unsupervised.json', 'question': 'Unsupervised recovery'},
    'Q7': {'file': 'q7_causal.json', 'question': 'Causal layer consistency'},
    'Q8': {'file': 'q8_crossarch.json', 'question': 'Cross-architecture consistency'},
}

CONFOUNDERS = {
    'Q1': 'Token frequency bias (common words learned first)',
    'Q2': 'Semantic exclusion in training data',
    'Q3': 'Co-occurrence patterns in training corpus',
    'Q4': 'Nonlinear activation artifacts',
    'Q5': 'LR schedule / curriculum changes',
    'Q6': 'Shared embedding / LLM bias in labeling',
    'Q7': 'Architecture-dependent attention patterns',
    'Q8': 'Shared training data and loss function',
}


def load_results():
    """Load all available probe results."""
    results = {}
    for probe_id, info in PROBES.items():
        path = os.path.join(RESULTS_DIR, info['file'])
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                results[probe_id] = json.load(f)
        else:
            results[probe_id] = None
    return results


# ######################################################################
#  SECTION 1: CLASSIFICATION
# ######################################################################

def classify_result(probe_id, data):
    """Classify probe result as coincidence, divergence, or null."""
    if data is None:
        return 'not_run', 'Probe not executed'

    verdict = data.get('verdict', 'unknown')

    if verdict in ('positive_with_caveats',):
        return 'coincidence', CONFOUNDERS.get(probe_id, 'Unknown confounder')
    elif verdict in ('contradicts_framework',):
        return 'divergence', 'Result contradicts theoretical prediction'
    elif verdict in ('mixed',):
        return 'mixed', 'Partial support, partial divergence'
    elif verdict in ('null', 'no_data', 'insufficient_data'):
        return 'null', 'No significant result'
    else:
        return 'unknown', f'Unrecognized verdict: {verdict}'


# ######################################################################
#  SECTION 2: RECOMMENDATIONS
# ######################################################################

def generate_recommendations(results, classifications):
    """Generate recommendations for primitivos.json based on results."""
    recs = []

    # Q1: If layer order is wrong, suggest reordering
    if classifications['Q1'][0] == 'divergence':
        recs.append({
            'source': 'Q1',
            'type': 'review_layers',
            'description': ('Model learns primitives in reverse layer order. '
                           'Review capa assignments in primitivos.json.'),
            'priority': 'high',
        })

    # Q2: If duals don't anti-correlate, suggest reviewing axes
    if classifications['Q2'][0] == 'null':
        recs.append({
            'source': 'Q2',
            'type': 'review_duals',
            'description': ('Dual axes show no anti-correlation in model. '
                           'Either the model does not encode duality, or '
                           'the axes need revision.'),
            'priority': 'medium',
        })

    # Q3: Novel edges from DAG probe
    q3 = results.get('Q3')
    if q3 and q3.get('best_f1', 0) > 0.3:
        recs.append({
            'source': 'Q3',
            'type': 'add_dependencies',
            'description': ('Model discovers dependencies not in theory. '
                           'Consider adding high-confidence novel edges.'),
            'priority': 'medium',
        })

    # Q4: Emergent triadic enrichment
    q4 = results.get('Q4')
    if q4 and q4.get('counts', {}).get('E', 0) > 5:
        recs.append({
            'source': 'Q4',
            'type': 'document_triadic',
            'description': ('Emergent triadic dependencies found. '
                           'Document which triples show genuine emergence.'),
            'priority': 'low',
        })

    # Q6: Reconciliation suggestions
    q6 = results.get('Q6')
    if q6 and q6.get('n_critical_mismatches', 0) > 0:
        recs.append({
            'source': 'Q6',
            'type': 'reconcile',
            'description': ('Unsupervised discovery flags critical mismatches. '
                           'Review reconciliation report for specifics.'),
            'priority': 'high',
        })

    # General: If most probes are null
    n_null = sum(1 for c in classifications.values() if c[0] == 'null')
    if n_null >= 5:
        recs.append({
            'source': 'overall',
            'type': 'epistemic_caution',
            'description': ('Most probes returned null. The framework may not '
                           'be recoverable from this model architecture. '
                           'This does not falsify the theory — it means the '
                           'neural model is not a good probe for it.'),
            'priority': 'high',
        })

    return recs


# ######################################################################
#  SECTION 3: MAIN OUTPUT
# ######################################################################

def main():
    print("=" * 70)
    print("Neural Probe Interpretation — Q1-Q8 Consolidation")
    print("=" * 70)

    results = load_results()
    classifications = {}

    # Summary table
    print("\n  --- Probe Summary ---\n")
    print(f"  {'Probe':<6} {'Question':<35} {'Result':<15} {'Confounder/Note'}")
    print("  " + "-" * 90)

    for probe_id, info in PROBES.items():
        status, note = classify_result(probe_id, results[probe_id])
        classifications[probe_id] = (status, note)
        print(f"  {probe_id:<6} {info['question']:<35} {status:<15} {note}")

    # Count
    counts = {}
    for status, _ in classifications.values():
        counts[status] = counts.get(status, 0) + 1

    print(f"\n  Coincidences: {counts.get('coincidence', 0)}")
    print(f"  Divergences:  {counts.get('divergence', 0)}")
    print(f"  Mixed:        {counts.get('mixed', 0)}")
    print(f"  Null:         {counts.get('null', 0)}")
    print(f"  Not run:      {counts.get('not_run', 0)}")

    # Recommendations
    recs = generate_recommendations(results, classifications)
    print(f"\n  --- Recommendations ({len(recs)}) ---\n")
    for i, rec in enumerate(recs, 1):
        print(f"  {i}. [{rec['priority'].upper()}] ({rec['source']}) "
              f"{rec['description']}")

    # Key epistemic point
    print("\n  --- Epistemic Summary ---\n")
    print("  REMEMBER: A coincidence between model and theory can mean:")
    print("    a) The theory captures genuine structure")
    print("    b) Both share the same training-data bias")
    print("    c) The test has low specificity")
    print("  A divergence can mean:")
    print("    a) The theory is wrong in that aspect")
    print("    b) The model is not expressive enough")
    print("    c) The probe is measuring the wrong thing")
    print("  Neither coincidence nor divergence is proof.")

    # Save
    os.makedirs(RESULTS_DIR, exist_ok=True)
    output = {
        'classifications': {k: {'status': v[0], 'note': v[1]}
                           for k, v in classifications.items()},
        'counts': counts,
        'recommendations': recs,
    }

    out_path = os.path.join(RESULTS_DIR, 'interpretation.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n  Results saved to: {out_path}")


if __name__ == '__main__':
    main()
