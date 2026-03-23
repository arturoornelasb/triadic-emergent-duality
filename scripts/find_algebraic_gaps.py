"""Find Algebraic Gaps: missing operators and candidate primitivos.

Analyzes all 15 possible inter-capa connections, identifies which have
direct coverage vs. gaps, searches C:\research\first_principles for
candidate concepts, and proposes a capa 6 internal operator.

Usage:
    python find_algebraic_gaps.py
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json
import math
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'data'))
RESULTS_DIR = os.path.normpath(os.path.join(
    SCRIPT_DIR, '..', 'dualidademergente+reptimeline', 'internal', 'results'))
GOLD_PATH = os.path.normpath(os.path.join(
    SCRIPT_DIR, '..', 'dualidademergente+reptimeline', 'model', 'gold_primitivos_72.json'))
FIRST_PRINCIPLES_DIR = os.path.normpath('C:/research/first_principles')


# ######################################################################
#  ALGEBRA DEFINITIONS
# ######################################################################

ALGEBRA_NAMES = {
    1: 'Booleano {0,1}',
    2: 'Fuzzy {0,+}',
    3: 'Ordinal {<,=,>}',
    4: 'Modal {◇,□}',
    5: 'Trivalente {−,0,+}',
    6: 'Probabilístico {0,?}',
}


# ######################################################################
#  SECTION 0: DATA LOADING
# ######################################################################

def load_data():
    with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
        prim_data = json.load(f)
    with open(os.path.join(DATA_DIR, 'dualidad_primitivo_map.json'), 'r', encoding='utf-8') as f:
        dual_data = json.load(f)

    prims = prim_data['primitivos']
    name_to_capa = {p['nombre']: p['capa'] for p in prims}
    name_to_bit = {p['nombre']: p['bit'] for p in prims}
    name_to_deps = {p['nombre']: list(p['deps']) for p in prims}
    name_to_primo = {p['nombre']: p['primo'] for p in prims}

    # Group by capa
    capa_prims = defaultdict(list)
    for p in prims:
        capa_prims[p['capa']].append(p['nombre'])

    # Load gold signatures
    gold = {}
    if os.path.exists(GOLD_PATH):
        with open(GOLD_PATH, 'r', encoding='utf-8') as f:
            gold = json.load(f)

    return prim_data, dual_data, prims, name_to_capa, name_to_bit, name_to_deps, name_to_primo, capa_prims, gold


# ######################################################################
#  SECTION 1: ALL 15 INTER-CAPA CONNECTIONS
# ######################################################################

def analyze_all_connections(dual_data, name_to_capa):
    """Map all 15 possible capa pairs to covering dualities."""

    # Compute capa involvement for each duality
    duality_capas = {}
    for d_id, d_info in dual_data['dualidades'].items():
        all_members = d_info['anclas'] + d_info['secundarios']
        capas = set()
        for m in all_members:
            if m in name_to_capa:
                capas.add(name_to_capa[m])
        duality_capas[d_id] = capas

    # All 15 pairs
    all_pairs = []
    for i in range(1, 7):
        for j in range(i + 1, 7):
            all_pairs.append((i, j))

    coverage = {}
    for (ci, cj) in all_pairs:
        covering = []
        for d_id, capas in duality_capas.items():
            if ci in capas and cj in capas:
                covering.append(d_id)
        coverage[(ci, cj)] = covering

    return coverage, duality_capas


# ######################################################################
#  SECTION 2: GAPS AND COMPOSABILITY
# ######################################################################

def find_gaps_and_composability(coverage):
    """Identify uncovered pairs and check if they're composable via chain."""

    # The transition chain: 1→2→3→4→5→6
    chain_links = {(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)}

    gaps = {}
    for (ci, cj), covering in sorted(coverage.items()):
        if not covering:
            # Check composability: can we reach ci→cj via chain steps?
            distance = cj - ci
            # Path: ci → ci+1 → ... → cj
            path_links = [(k, k + 1) for k in range(ci, cj)]
            all_covered = all(
                len(coverage.get((a, b), [])) > 0 for (a, b) in path_links
            )
            path_ops = []
            for (a, b) in path_links:
                ops = coverage.get((a, b), [])
                path_ops.append(ops[0] if ops else '???')

            gaps[(ci, cj)] = {
                'distance': distance,
                'composable': all_covered,
                'composition_path': path_ops,
            }

    return gaps


# ######################################################################
#  SECTION 3: SEARCH FIRST_PRINCIPLES
# ######################################################################

# Search profiles per gap type
GAP_SEARCH_PROFILES = {
    'capa6_internal': {
        'keywords': [
            'self-reference', 'reflexive', 'metacognition', 'measurement',
            'observer', 'introspection', 'qualia', 'autopoiesis',
            'strange loop', 'fixed point', 'self-awareness', 'consciousness',
        ],
        'files': [
            '09_philosophy_of_science/philosophy_of_mind/first_principles.md',
            '02_physics/quantum_mechanics/first_principles.md',
            '07_formal_sciences/category_theory/first_principles.md',
            '10_interdisciplinary/cognitive_science/first_principles.md',
            '07_formal_sciences/systems_theory/first_principles.md',
        ],
    },
    'capa3_to_5': {
        'keywords': [
            'emergence', 'self-organization', 'autopoiesis', 'dissipative',
            'complexity', 'adaptive', 'life', 'animate', 'organism',
        ],
        'files': [
            '07_formal_sciences/systems_theory/first_principles.md',
            '04_biology/theoretical_biology/first_principles.md',
            '09_philosophy_of_science/philosophy_of_mind/first_principles.md',
            '10_interdisciplinary/cognitive_science/first_principles.md',
        ],
    },
    'capa1_to_3': {
        'keywords': [
            'becoming', 'process', 'temporality', 'event', 'flux',
            'feedback', 'iteration', 'recursion', 'sequence',
        ],
        'files': [
            '07_formal_sciences/systems_theory/first_principles.md',
            '01_mathematics/logic_and_set_theory/first_principles.md',
            '07_formal_sciences/category_theory/first_principles.md',
        ],
    },
}


def search_first_principles(profile_name, profile):
    """Search first_principles files for keywords matching a gap profile."""

    results = []
    keywords = profile['keywords']

    for rel_path in profile['files']:
        full_path = os.path.join(FIRST_PRINCIPLES_DIR, rel_path)
        if not os.path.exists(full_path):
            continue

        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')
        content_lower = content.lower()

        # Count keyword hits
        hits = {}
        for kw in keywords:
            count = content_lower.count(kw.lower())
            if count > 0:
                hits[kw] = count

        if not hits:
            continue

        # Extract principle names (lines starting with ## or ### that contain "Principle" or numbered)
        principles_found = []
        for i, line in enumerate(lines):
            line_lower = line.lower()
            # Match keyword in context
            for kw in keywords:
                if kw.lower() in line_lower:
                    # Get surrounding context (principle name)
                    principle_name = None
                    for j in range(i, max(i - 15, -1), -1):
                        if lines[j].startswith('#'):
                            principle_name = lines[j].lstrip('#').strip()
                            break
                    if principle_name and len(principle_name) < 200:
                        # Get 1-line excerpt
                        excerpt = line.strip()
                        if len(excerpt) > 150:
                            excerpt = excerpt[:147] + '...'
                        principles_found.append({
                            'principle': principle_name,
                            'keyword': kw,
                            'excerpt': excerpt,
                            'source': rel_path,
                            'line': i + 1,
                        })

        # Deduplicate by principle name
        seen = set()
        deduped = []
        for pf in principles_found:
            key = pf['principle']
            if key not in seen:
                seen.add(key)
                deduped.append(pf)

        results.extend(deduped)

    # Sort by number of keyword hits (most relevant first)
    keyword_counts = defaultdict(int)
    for r in results:
        keyword_counts[r['principle']] += 1
    results.sort(key=lambda r: -keyword_counts[r['principle']])

    return results


# ######################################################################
#  SECTION 4: CAPA 6 INTERNAL OPERATOR CANDIDATES
# ######################################################################

def analyze_capa6_candidates(capa_prims, name_to_capa, name_to_deps, gold):
    """Analyze capa 6 primitivos and propose internal operator candidates."""

    c6_prims = capa_prims[6]
    c6_info = []
    for name in c6_prims:
        eng_key = None
        for k, v in gold.items():
            if v.get('nombre') == name:
                eng_key = k
                break
        c6_info.append({
            'nombre': name,
            'english': eng_key,
            'deps': name_to_deps.get(name, []),
            'dep_capas': [name_to_capa.get(d, 0) for d in name_to_deps.get(name, [])],
        })

    # The 4 c6 primitivos form 2 dual pairs:
    # temporal_obs / eterno_obs  (time-bound vs eternal)
    # receptivo / creador_obs    (passive vs active)
    # An internal operator should relate BETWEEN these pairs
    dual_pairs = [
        ('temporal_obs', 'eterno_obs'),
        ('receptivo', 'creador_obs'),
    ]

    # Compute shared deps between pairs
    pair_deps = []
    for a, b in dual_pairs:
        deps_a = set(name_to_deps.get(a, []))
        deps_b = set(name_to_deps.get(b, []))
        shared = deps_a & deps_b
        unique_a = deps_a - deps_b
        unique_b = deps_b - deps_a
        pair_deps.append({
            'pair': [a, b],
            'shared_deps': sorted(shared),
            'unique_a': sorted(unique_a),
            'unique_b': sorted(unique_b),
        })

    # Cross-pair analysis: what connects temporal_obs/eterno_obs WITH receptivo/creador_obs?
    all_pair1 = set(name_to_deps.get('temporal_obs', [])) | set(name_to_deps.get('eterno_obs', []))
    all_pair2 = set(name_to_deps.get('receptivo', [])) | set(name_to_deps.get('creador_obs', []))
    cross_shared = all_pair1 & all_pair2
    cross_unique_1 = all_pair1 - all_pair2
    cross_unique_2 = all_pair2 - all_pair1

    # Jaccard between c6 pairs via gold signatures
    pair_jaccards = []
    for a, b in dual_pairs:
        sig_a = sig_b = None
        for k, v in gold.items():
            if v.get('nombre') == a:
                sig_a = set(v['active_bits'])
            if v.get('nombre') == b:
                sig_b = set(v['active_bits'])
        if sig_a and sig_b:
            inter = len(sig_a & sig_b)
            union = len(sig_a | sig_b)
            jaccard = inter / union if union else 0
            pair_jaccards.append({
                'pair': [a, b],
                'jaccard': round(jaccard, 4),
                'diff_bits': len(sig_a ^ sig_b),
            })

    # Candidate operators from first_principles analysis
    candidates = [
        {
            'name': 'Autopoiesis (Self-Production)',
            'operation': 'The observer produces its own components — operationally closed yet coupled',
            'algebra': 'Maps {0,?} → {0,?}: self-referential closure within probabilistic domain',
            'source': 'systems_theory/first_principles.md',
            'connects': 'Both dual pairs: temporal self-production AND receptive self-modeling',
            'score': 0.85,
        },
        {
            'name': 'Measurement/Collapse (Observer Effect)',
            'operation': 'Observation fixes indeterminate state — the act of observing changes the observed',
            'algebra': 'Maps {0,?} → {0,1}: reduces probabilistic to boolean (but within meta-level)',
            'source': 'quantum_mechanics/first_principles.md',
            'connects': 'temporal_obs↔eterno_obs (collapse of temporal superposition)',
            'score': 0.80,
        },
        {
            'name': 'Global Workspace (Conscious Access)',
            'operation': 'One process wins and broadcasts to all — selective gating of awareness',
            'algebra': 'Maps {0,?} → {0,?}: competitive selection within probabilistic states',
            'source': 'cognitive_science/first_principles.md',
            'connects': 'receptivo↔creador_obs (passive reception vs active broadcast)',
            'score': 0.75,
        },
        {
            'name': 'Intentionality (Aboutness)',
            'operation': 'Mental states are directed toward objects — the content-vehicle distinction',
            'algebra': 'Maps observer → observed: creates referential link within meta-level',
            'source': 'philosophy_of_mind/first_principles.md',
            'connects': 'Cross-pair: links what observer IS (temporal/eternal) to what it DOES (receive/create)',
            'score': 0.70,
        },
    ]

    return {
        'c6_primitivos': c6_info,
        'dual_pairs': pair_deps,
        'cross_pair': {
            'shared_deps': sorted(cross_shared),
            'unique_pair1': sorted(cross_unique_1),
            'unique_pair2': sorted(cross_unique_2),
        },
        'pair_jaccards': pair_jaccards,
        'candidates': candidates,
    }


# ######################################################################
#  SECTION 5: PROPOSED NEW PRIMITIVOS FOR GAPS
# ######################################################################

def propose_new_primitivos(gaps, capa_prims, name_to_capa, name_to_deps, gold):
    """For significant gaps, propose primitivos that could fill them."""

    proposals = []

    # Only propose for gaps that are NOT composable or have distance > 2
    for (ci, cj), gap_info in sorted(gaps.items()):
        if gap_info['distance'] <= 1:
            continue  # Adjacent pairs without coverage are transition gaps, not new-primitivo territory

        # For each significant gap, evaluate if a new primitivo would help
        if (ci, cj) == (1, 3):
            proposals.append({
                'gap': '%d→%d' % (ci, cj),
                'gap_name': 'Boolean→Ordinal (Existence→Time)',
                'candidate': 'devenir (becoming)',
                'definition': 'The transition from pure existence to temporal sequence',
                'proposed_capa': 2,  # Would bridge 1→3 via enhancement of capa 2
                'deps': ['vacío', 'uno', 'flujo_temporal'],
                'source': 'Process metaphysics (Whitehead), Systems theory (feedback)',
                'impact': 'Would create direct Boolean→Ordinal path without Fuzzy intermediary',
                'priority': 'LOW — composable via chain, and D8+D6 already covers this indirectly',
            })
        elif (ci, cj) == (3, 5):
            proposals.append({
                'gap': '%d→%d' % (ci, cj),
                'gap_name': 'Ordinal→Trivalent (Time→Life)',
                'candidate': 'emergencia (emergence)',
                'definition': 'Spontaneous arising of organized complexity from temporal process',
                'proposed_capa': 4,  # Would bridge 3→5 via capa 4
                'deps': ['flujo_temporal', 'orden', 'vida'],
                'source': 'Systems theory (dissipative structures, self-organization)',
                'impact': 'Would create direct Ordinal→Trivalent path',
                'priority': 'LOW — composable via D7+D5, and biological emergence is implicit in vida deps',
            })
        elif (ci, cj) == (1, 5) or (ci, cj) == (1, 6):
            proposals.append({
                'gap': '%d→%d' % (ci, cj),
                'gap_name': '%s→%s' % (ALGEBRA_NAMES[ci], ALGEBRA_NAMES[cj]),
                'candidate': None,
                'definition': None,
                'proposed_capa': None,
                'deps': None,
                'source': 'N/A — too far apart, composition via chain is natural',
                'impact': 'Would bypass 3-4 algebraic layers',
                'priority': 'NONE — long-range gaps are features, not bugs',
            })

    # Special proposal: capa 6 internal
    proposals.append({
        'gap': '6↔6',
        'gap_name': 'Probabilistic internal operator',
        'candidate': 'reflexión (self-observation)',
        'definition': 'The observer observing itself — operational closure of meta-level',
        'proposed_capa': 6,
        'deps': ['consciente', 'temporal_obs', 'receptivo'],
        'source': 'Autopoiesis (systems theory), Measurement problem (QM), Hard problem (philo of mind)',
        'impact': 'Would complete the algebraic layer system — every capa would have an internal operator',
        'priority': 'HIGH — structural gap, needed for theoretical completeness',
    })

    return proposals


# ######################################################################
#  SECTION 6: IMPACT ANALYSIS ON JACCARD
# ######################################################################

def analyze_jaccard_impact(proposals, gold, name_to_bit):
    """Estimate how proposed new primitivos would affect existing Jaccard values."""

    impacts = []
    for prop in proposals:
        if not prop.get('candidate') or not prop.get('deps'):
            continue

        # Simulate: if we added this primitivo, which existing pairs would change?
        new_deps = prop['deps']
        new_dep_bits = set()
        for d in new_deps:
            if d in name_to_bit:
                new_dep_bits.add(name_to_bit[d])

        # Check overlap with existing c6 observer primitivos
        affected_pairs = []
        c6_names = ['temporal_obs', 'eterno_obs', 'receptivo', 'creador_obs']
        for name in c6_names:
            for k, v in gold.items():
                if v.get('nombre') == name:
                    existing_bits = set(v['active_bits'])
                    overlap = existing_bits & new_dep_bits
                    if overlap:
                        affected_pairs.append({
                            'primitivo': name,
                            'overlap_bits': sorted(overlap),
                            'overlap_count': len(overlap),
                        })

        impacts.append({
            'candidate': prop['candidate'],
            'gap': prop['gap'],
            'new_dep_bits': sorted(new_dep_bits),
            'affected': affected_pairs,
        })

    return impacts


# ######################################################################
#  MAIN
# ######################################################################

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    print('=' * 70)
    print('  FIND ALGEBRAIC GAPS')
    print('  Missing operators, candidates from first_principles')
    print('=' * 70)

    (prim_data, dual_data, prims, name_to_capa, name_to_bit,
     name_to_deps, name_to_primo, capa_prims, gold) = load_data()

    # ---- SECTION 1: All 15 connections ----
    print()
    print('=' * 70)
    print('  SECTION 1: ALL 15 INTER-CAPA CONNECTIONS')
    print('=' * 70)

    coverage, duality_capas = analyze_all_connections(dual_data, name_to_capa)

    print()
    print('  %-8s %-30s %-30s %s' % ('Pair', 'From', 'To', 'Coverage'))
    print('  ' + '-' * 90)
    covered_count = 0
    for (ci, cj) in sorted(coverage.keys()):
        covering = coverage[(ci, cj)]
        status = ', '.join(covering) if covering else '--- GAP ---'
        if covering:
            covered_count += 1
        print('  %-8s %-30s %-30s %s' % (
            '%d→%d' % (ci, cj),
            ALGEBRA_NAMES[ci],
            ALGEBRA_NAMES[cj],
            status))

    print()
    print('  Coverage: %d/15 pairs have direct operators' % covered_count)

    # ---- SECTION 2: Gaps and composability ----
    print()
    print('=' * 70)
    print('  SECTION 2: GAPS AND COMPOSABILITY')
    print('=' * 70)

    gaps = find_gaps_and_composability(coverage)

    if not gaps:
        print()
        print('  No gaps found — all 15 pairs covered!')
    else:
        print()
        for (ci, cj), gap_info in sorted(gaps.items()):
            comp_str = 'YES' if gap_info['composable'] else 'NO'
            path_str = ' → '.join(gap_info['composition_path'])
            print('  Gap %d→%d (distance=%d)  Composable: %s' % (
                ci, cj, gap_info['distance'], comp_str))
            if gap_info['composable']:
                print('    Composition: %s' % path_str)
            else:
                print('    WARNING: NOT composable via chain!')

    # ---- SECTION 3: First principles search ----
    print()
    print('=' * 70)
    print('  SECTION 3: FIRST PRINCIPLES SEARCH')
    print('=' * 70)

    fp_results = {}
    for profile_name, profile in GAP_SEARCH_PROFILES.items():
        print()
        print('  --- %s ---' % profile_name)
        results = search_first_principles(profile_name, profile)
        fp_results[profile_name] = results

        if not results:
            print('    No matches found')
        else:
            seen = set()
            count = 0
            for r in results:
                if r['principle'] not in seen and count < 8:
                    seen.add(r['principle'])
                    print('    [%s] %s' % (r['keyword'], r['principle']))
                    if r['excerpt']:
                        excerpt = r['excerpt'][:100]
                        print('      "%s"' % excerpt)
                    count += 1
            if len(results) > len(seen):
                print('    ... and %d more matches' % (len(results) - len(seen)))

    # ---- SECTION 4: Capa 6 internal operator ----
    print()
    print('=' * 70)
    print('  SECTION 4: CAPA 6 INTERNAL OPERATOR CANDIDATES')
    print('=' * 70)

    c6_analysis = analyze_capa6_candidates(
        capa_prims, name_to_capa, name_to_deps, gold)

    print()
    print('  Capa 6 primitivos:')
    for info in c6_analysis['c6_primitivos']:
        print('    %-20s deps=%s  dep_capas=%s' % (
            info['nombre'], info['deps'], info['dep_capas']))

    print()
    print('  Dual pairs within capa 6:')
    for pd in c6_analysis['dual_pairs']:
        print('    %s / %s' % (pd['pair'][0], pd['pair'][1]))
        print('      shared deps: %s' % pd['shared_deps'])

    print()
    print('  Cross-pair analysis:')
    cp = c6_analysis['cross_pair']
    print('    Shared between pair1 and pair2: %s' % cp['shared_deps'])
    print('    Unique to pair1 (temp/eternal): %s' % cp['unique_pair1'])
    print('    Unique to pair2 (recv/creator): %s' % cp['unique_pair2'])

    if c6_analysis['pair_jaccards']:
        print()
        print('  Jaccard of c6 dual pairs:')
        for pj in c6_analysis['pair_jaccards']:
            print('    %s/%s: Jaccard=%.4f  diff=%d bits' % (
                pj['pair'][0], pj['pair'][1], pj['jaccard'], pj['diff_bits']))

    print()
    print('  Candidate internal operators (ranked):')
    for i, cand in enumerate(c6_analysis['candidates'], 1):
        print('    %d. %s (score=%.2f)' % (i, cand['name'], cand['score']))
        print('       Operation: %s' % cand['operation'])
        print('       Algebra:   %s' % cand['algebra'])
        print('       Connects:  %s' % cand['connects'])
        print('       Source:    %s' % cand['source'])

    # ---- SECTION 5: Proposed new primitivos ----
    print()
    print('=' * 70)
    print('  SECTION 5: PROPOSED NEW PRIMITIVOS')
    print('=' * 70)

    proposals = propose_new_primitivos(
        gaps, capa_prims, name_to_capa, name_to_deps, gold)

    print()
    for prop in proposals:
        print('  Gap: %s (%s)' % (prop['gap'], prop['gap_name']))
        if prop['candidate']:
            print('    Candidate:  %s' % prop['candidate'])
            print('    Definition: %s' % prop['definition'])
            print('    Capa:       %s' % prop['proposed_capa'])
            print('    Deps:       %s' % prop['deps'])
            print('    Source:     %s' % prop['source'])
            print('    Impact:     %s' % prop['impact'])
            print('    Priority:   %s' % prop['priority'])
        else:
            print('    No candidate needed: %s' % prop['source'])
        print()

    # ---- SECTION 6: Jaccard impact ----
    print()
    print('=' * 70)
    print('  SECTION 6: JACCARD IMPACT ANALYSIS')
    print('=' * 70)

    impacts = analyze_jaccard_impact(proposals, gold, name_to_bit)

    print()
    for imp in impacts:
        print('  Candidate: %s (gap %s)' % (imp['candidate'], imp['gap']))
        print('    New dep bits: %s' % imp['new_dep_bits'])
        if imp['affected']:
            for aff in imp['affected']:
                print('    Affects %s: %d shared bits %s' % (
                    aff['primitivo'], aff['overlap_count'], aff['overlap_bits']))
        else:
            print('    No overlap with existing c6 primitivos')
        print()

    # ---- BUILD RESULTS ----
    results = {
        'coverage': {
            '%d→%d' % (ci, cj): {
                'operators': covering,
                'covered': len(covering) > 0,
            }
            for (ci, cj), covering in sorted(coverage.items())
        },
        'covered_pairs': covered_count,
        'total_pairs': 15,
        'gaps': {
            '%d→%d' % (ci, cj): info
            for (ci, cj), info in sorted(gaps.items())
        },
        'first_principles_matches': {
            profile: [
                {
                    'principle': r['principle'],
                    'keyword': r['keyword'],
                    'source': r['source'],
                }
                for r in results_list[:10]
            ]
            for profile, results_list in fp_results.items()
        },
        'capa6_analysis': {
            'primitivos': c6_analysis['c6_primitivos'],
            'dual_pairs': c6_analysis['dual_pairs'],
            'cross_pair': c6_analysis['cross_pair'],
            'pair_jaccards': c6_analysis['pair_jaccards'],
            'candidates': c6_analysis['candidates'],
        },
        'proposals': proposals,
        'jaccard_impact': impacts,
    }

    # ---- Save ----
    out_path = os.path.join(RESULTS_DIR, 'algebraic_gaps.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # ---- SYNTHESIS ----
    print()
    print('=' * 70)
    print('  SYNTHESIS')
    print('=' * 70)
    print()
    print('  Inter-capa coverage:  %d/15 pairs' % covered_count)
    print('  Gaps identified:      %d' % len(gaps))
    composable = sum(1 for g in gaps.values() if g['composable'])
    print('  Composable via chain: %d/%d' % (composable, len(gaps)))
    print('  Capa 6 internal:      MISSING (4 candidates ranked)')
    high_priority = sum(1 for p in proposals if p.get('priority', '').startswith('HIGH'))
    print('  High-priority proposals: %d' % high_priority)
    print()
    print('  Results saved: %s' % out_path)
    print('=' * 70)


if __name__ == '__main__':
    main()
