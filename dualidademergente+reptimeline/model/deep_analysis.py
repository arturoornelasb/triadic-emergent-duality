"""
Deep Analysis: Full concept-level map of all 262 anchors.

Shows:
  1. For each anchor: top-5 connections (Jaccard on 65-bit signatures)
  2. Full triadic dependencies (bit-level, translated to concept semantics)
  3. Full dependency list (bit-level)
  4. Concept clusters by signature similarity
  5. Per-domain concept maps

Usage:
    python deep_analysis.py                # from exploration.json
    python deep_analysis.py --recompute    # re-run BitDiscovery on signatures
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json
import math

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'neural', 'results'))


# ######################################################################
#  SECTION 1: LOAD DATA
# ######################################################################

def load_exploration():
    path = os.path.join(RESULTS_DIR, 'exploration.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def jaccard(bits_a, bits_b):
    a = set(bits_a)
    b = set(bits_b)
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)


def hamming_dist(bits_a, bits_b):
    sa = set(bits_a)
    sb = set(bits_b)
    return len(sa.symmetric_difference(sb))


# ######################################################################
#  SECTION 2: CONCEPT CONNECTIONS
# ######################################################################

def compute_all_connections(sigs):
    concepts = list(sigs.keys())
    n = len(concepts)
    connections = {}

    for i in range(n):
        c1 = concepts[i]
        a_bits = sigs[c1]['active_indices']
        sims = []
        for j in range(n):
            if i == j:
                continue
            c2 = concepts[j]
            b_bits = sigs[c2]['active_indices']
            j_sim = jaccard(a_bits, b_bits)
            sims.append((c2, sigs[c2]['domain'], j_sim, hamming_dist(a_bits, b_bits)))
        sims.sort(key=lambda x: -x[2])
        connections[c1] = {
            'domain': sigs[c1]['domain'],
            'n_active': sigs[c1]['n_active'],
            'top_same': [],
            'top_cross': [],
        }
        dom = sigs[c1]['domain']
        for c2, d2, sim, hdist in sims:
            if d2 == dom and len(connections[c1]['top_same']) < 5:
                connections[c1]['top_same'].append((c2, sim, hdist))
            elif d2 != dom and len(connections[c1]['top_cross']) < 5:
                connections[c1]['top_cross'].append((c2, d2, sim, hdist))

    return connections


# ######################################################################
#  SECTION 3: CONCEPT CLUSTERS
# ######################################################################

def find_clusters(sigs, threshold=0.90):
    concepts = list(sigs.keys())
    n = len(concepts)
    clusters = []
    assigned = set()

    for i in range(n):
        if concepts[i] in assigned:
            continue
        cluster = [concepts[i]]
        a_bits = sigs[concepts[i]]['active_indices']
        for j in range(i + 1, n):
            if concepts[j] in assigned:
                continue
            b_bits = sigs[concepts[j]]['active_indices']
            if jaccard(a_bits, b_bits) >= threshold:
                cluster.append(concepts[j])
        if len(cluster) > 1:
            clusters.append(cluster)
            assigned.update(cluster)

    clusters.sort(key=lambda c: -len(c))
    return clusters


# ######################################################################
#  SECTION 4: RECOMPUTE BITDISCOVERY
# ######################################################################

def recompute_discovery(sigs):
    sys.path.insert(0, SCRIPT_DIR)
    from reptimeline import BitDiscovery
    from reptimeline.core import ConceptSnapshot

    codes = {}
    for concept, data in sigs.items():
        codes[concept] = data['bits']

    snap = ConceptSnapshot(step=0, codes=codes)

    discovery = BitDiscovery(
        dead_threshold=0.02,
        dual_threshold=-0.3,
        dep_confidence=0.9,
        triadic_threshold=0.7,
    )
    report = discovery.discover(snap, top_k=10)
    return report


# ######################################################################
#  SECTION 5: MAIN
# ######################################################################

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--recompute', action='store_true',
                        help='Re-run BitDiscovery for full triadic list')
    parser.add_argument('--output', default='deep_analysis.json',
                        help='Output filename')
    args = parser.parse_args()

    data = load_exploration()
    sigs = data['signatures']
    print('Loaded %d concept signatures from exploration.json' % len(sigs))

    # ---- PART 1: All concept connections ----
    print()
    print('=' * 70)
    print('  PART 1: CONCEPT CONNECTIONS (262 anchors)')
    print('=' * 70)

    connections = compute_all_connections(sigs)

    domains = {}
    for c, info in connections.items():
        d = info['domain']
        if d not in domains:
            domains[d] = []
        domains[d].append(c)

    for dom in sorted(domains.keys()):
        print()
        print('  --- %s (%d concepts) ---' % (dom, len(domains[dom])))
        for concept in sorted(domains[dom]):
            info = connections[concept]
            cross = info['top_cross']
            if cross:
                top_str = ', '.join(
                    '%s(%s %.3f)' % (c2, d2[:4], sim)
                    for c2, d2, sim, _ in cross[:3]
                )
            else:
                top_str = '-'
            same = info['top_same']
            if same:
                same_str = ', '.join(
                    '%s(%.3f)' % (c2, sim)
                    for c2, sim, _ in same[:2]
                )
            else:
                same_str = '-'
            print('    %-20s [%d bits] same:[%s]  cross:[%s]' % (
                concept, info['n_active'], same_str, top_str))

    # ---- PART 2: Concept clusters ----
    print()
    print('=' * 70)
    print('  PART 2: CONCEPT CLUSTERS (Jaccard >= 0.90)')
    print('=' * 70)

    clusters = find_clusters(sigs, threshold=0.90)
    print('  Found %d clusters:' % len(clusters))
    for i, cluster in enumerate(clusters):
        doms = [sigs[c]['domain'] for c in cluster]
        dom_set = set(doms)
        cross = 'CROSS-DOMAIN' if len(dom_set) > 1 else doms[0]
        print('    Cluster %d (%s): %s' % (i + 1, cross, cluster))

    # ---- PART 3: BitDiscovery full ----
    triadic_list = []
    dep_list = []
    dual_list = data.get('discovery', {}).get('duals', [])

    if args.recompute:
        print()
        print('=' * 70)
        print('  PART 3: FULL BITDISCOVERY (recomputing...)')
        print('=' * 70)

        report = recompute_discovery(sigs)

        bit_sem = {}
        for bs in report.bit_semantics:
            bit_sem[bs.bit_index] = {
                'rate': bs.activation_rate,
                'top': bs.top_concepts[:4],
                'anti': bs.anti_concepts[:3],
            }

        # 3a: All triadic deps (AND-gate: bit_r activates when bit_i AND bit_j)
        print()
        print('  --- Triadic Dependencies (%d) ---' % len(report.discovered_triadic_deps))
        for td in report.discovered_triadic_deps:
            triadic_list.append({
                'bit_i': td.bit_i,
                'bit_j': td.bit_j,
                'bit_r': td.bit_r,
                'strength': round(td.interaction_strength, 4),
                'p_r_given_ij': round(td.p_r_given_ij, 4),
                'p_r_given_i': round(td.p_r_given_i, 4),
                'p_r_given_j': round(td.p_r_given_j, 4),
            })

        # Group by emergent bit (bit_r)
        by_emergent = {}
        for td in report.discovered_triadic_deps:
            r = td.bit_r
            if r not in by_emergent:
                by_emergent[r] = []
            by_emergent[r].append(td)

        for bit_r in sorted(by_emergent.keys()):
            deps = by_emergent[bit_r]
            sem = bit_sem.get(bit_r, {})
            top = sem.get('top', [])
            rate = sem.get('rate', 0)
            print()
            print('    Emergent bit %d (rate=%.2f, top=%s): %d triadic deps' % (
                bit_r, rate, top[:3], len(deps)))
            for td in sorted(deps, key=lambda x: -x.interaction_strength)[:10]:
                sem_i = bit_sem.get(td.bit_i, {}).get('top', [])[:2]
                sem_j = bit_sem.get(td.bit_j, {}).get('top', [])[:2]
                print('      bit %2d AND bit %2d => bit %2d  str=%.3f  P(r|ij)=%.2f  (%s AND %s)' % (
                    td.bit_i, td.bit_j, td.bit_r, td.interaction_strength,
                    td.p_r_given_ij, sem_i, sem_j))

        # 3b: All deps
        print()
        print('  --- Dependencies (%d) ---' % len(report.discovered_deps))
        for dep in report.discovered_deps:
            dep_list.append({
                'bit_parent': dep.bit_parent,
                'bit_child': dep.bit_child,
                'confidence': round(dep.confidence, 4),
                'support': dep.support,
            })

        dep_list.sort(key=lambda x: -x['confidence'])
        print('  Top 50 dependencies:')
        for dep in dep_list[:50]:
            sem_p = bit_sem.get(dep['bit_parent'], {}).get('top', [])[:2]
            sem_c = bit_sem.get(dep['bit_child'], {}).get('top', [])[:2]
            print('    bit %2d => bit %2d  conf=%.3f  support=%d  (%s => %s)' % (
                dep['bit_parent'], dep['bit_child'], dep['confidence'],
                dep['support'], sem_p, sem_c))

        # 3c: All duals
        print()
        print('  --- Duals (%d) ---' % len(report.discovered_duals))
        dual_list = []
        for d in report.discovered_duals:
            sem_a = bit_sem.get(d.bit_a, {}).get('top', [])[:3]
            sem_b = bit_sem.get(d.bit_b, {}).get('top', [])[:3]
            dual_list.append({
                'bit_a': d.bit_a,
                'bit_b': d.bit_b,
                'r': round(d.anti_correlation, 4),
                'exclusive': d.concepts_exclusive,
                'both': d.concepts_both,
                'sem_a': sem_a,
                'sem_b': sem_b,
            })
            print('    bit %2d <-> bit %2d  r=%.3f  excl=%d  both=%d  (%s <-> %s)' % (
                d.bit_a, d.bit_b, d.anti_correlation,
                d.concepts_exclusive, d.concepts_both,
                sem_a, sem_b))
    else:
        print()
        print('  (Use --recompute to get full triadic + dependency lists)')

    # ---- SAVE ----
    output = {
        'n_concepts': len(sigs),
        'connections': {},
        'clusters_090': clusters,
    }

    for concept, info in connections.items():
        output['connections'][concept] = {
            'domain': info['domain'],
            'n_active_bits': info['n_active'],
            'top_same_domain': [
                {'concept': c2, 'jaccard': round(sim, 4), 'hamming': hdist}
                for c2, sim, hdist in info['top_same']
            ],
            'top_cross_domain': [
                {'concept': c2, 'domain': d2, 'jaccard': round(sim, 4), 'hamming': hdist}
                for c2, d2, sim, hdist in info['top_cross']
            ],
        }

    if args.recompute:
        output['triadic_deps'] = triadic_list
        output['dependencies'] = dep_list
        output['duals'] = dual_list

    out_path = os.path.join(RESULTS_DIR, args.output)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print()
    print('=' * 70)
    print('  Saved to: %s' % out_path)
    print('  Connections: %d concepts' % len(output['connections']))
    print('  Clusters (J>=0.90): %d' % len(clusters))
    if args.recompute:
        print('  Triadic: %d  Deps: %d  Duals: %d' % (
            len(triadic_list), len(dep_list), len(dual_list)))
    print('=' * 70)


if __name__ == '__main__':
    main()
