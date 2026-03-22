"""
Fase 3: Exploration — Map concepts through the trained 65-bit triadic head.

Uses the best checkpoint to extract 65-bit signatures for ALL concepts,
then runs reptimeline BitDiscovery + PrimitiveOverlay to find:
  - Which concepts cluster together (shared bits)
  - What duals the model learned (anti-correlated bits)
  - What dependencies exist (if A active, B always active)
  - Cross-domain structure (biology ↔ computer science?)
  - Per-domain separation (do domains form distinct clusters?)

Usage:
    python explore.py                          # 262 gold anchors
    python explore.py --concepts extra.json    # custom concept list
    python explore.py --add "quantum,relativity,photon"  # add extras
    python explore.py --device cuda            # use GPU (after training)

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

import torch
import torch.nn.functional as F
from triadic_extractor import TriadicExtractor
from reptimeline import TimelineTracker, BitDiscovery, PrimitiveOverlay
from reptimeline.core import ConceptSnapshot


# ######################################################################
#  SECTION 1: LOAD CONCEPTS
# ######################################################################

def load_gold_concepts():
    """Load 262 gold anchor concepts with domain labels."""
    gold_path = os.path.join(SCRIPT_DIR, 'gold_primes_65.json')
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

def extract_all(checkpoint_path, concepts, device='cpu'):
    """Extract 65-bit signatures for all concepts."""
    extractor = TriadicExtractor(n_bits=65)
    snap = extractor.extract(checkpoint_path, concepts, device=device)
    return snap, extractor


# ######################################################################
#  SECTION 3: DOMAIN ANALYSIS
# ######################################################################

def domain_separation(snap, gold_data):
    """Compute within-domain vs between-domain similarity."""
    domains = {}
    for concept, data in gold_data.items():
        if concept in snap.codes:
            dom = data['domain']
            if dom not in domains:
                domains[dom] = []
            domains[dom].append(concept)

    results = {}
    domain_names = sorted(domains.keys())

    for dom in domain_names:
        concepts = domains[dom]
        if len(concepts) < 2:
            continue

        # Within-domain similarity (Jaccard)
        within_sims = []
        for i in range(len(concepts)):
            for j in range(i + 1, len(concepts)):
                a = set(k for k, v in enumerate(snap.codes[concepts[i]]) if v == 1)
                b = set(k for k, v in enumerate(snap.codes[concepts[j]]) if v == 1)
                union = a | b
                if union:
                    within_sims.append(len(a & b) / len(union))

        # Between-domain similarity (sample from other domains)
        between_sims = []
        other_concepts = [c for d, cs in domains.items() if d != dom for c in cs]
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

        results[dom] = {
            'n_concepts': len(concepts),
            'within_similarity': round(within_mean, 4),
            'between_similarity': round(between_mean, 4),
            'separation_ratio': round(separation, 4),
        }
        print(f'    {dom:<15} n={len(concepts):>3}  '
              f'within={within_mean:.3f}  between={between_mean:.3f}  '
              f'sep={separation:.3f}')

    return results


def cross_domain_matrix(snap, gold_data):
    """Compute domain-to-domain mean Jaccard similarity matrix."""
    domains = {}
    for concept, data in gold_data.items():
        if concept in snap.codes:
            dom = data['domain']
            if dom not in domains:
                domains[dom] = []
            domains[dom].append(concept)

    domain_names = sorted(domains.keys())
    matrix = {}

    for i, d1 in enumerate(domain_names):
        matrix[d1] = {}
        for j, d2 in enumerate(domain_names):
            sims = []
            for c1 in domains[d1]:
                for c2 in domains[d2]:
                    if c1 == c2:
                        continue
                    a = set(k for k, v in enumerate(snap.codes[c1]) if v == 1)
                    b = set(k for k, v in enumerate(snap.codes[c2]) if v == 1)
                    union = a | b
                    if union:
                        sims.append(len(a & b) / len(union))
            matrix[d1][d2] = round(sum(sims) / len(sims), 4) if sims else 0

    return matrix, domain_names


def find_cross_domain_bridges(snap, gold_data, top_n=20):
    """Find concepts from different domains with highest similarity."""
    bridges = []
    concepts = list(snap.codes.keys())
    domain_map = {c: gold_data[c]['domain'] for c in concepts if c in gold_data}

    for i in range(len(concepts)):
        for j in range(i + 1, len(concepts)):
            c1, c2 = concepts[i], concepts[j]
            if c1 not in domain_map or c2 not in domain_map:
                continue
            if domain_map[c1] == domain_map[c2]:
                continue

            a = set(k for k, v in enumerate(snap.codes[c1]) if v == 1)
            b = set(k for k, v in enumerate(snap.codes[c2]) if v == 1)
            union = a | b
            if not union:
                continue
            sim = len(a & b) / len(union)
            shared = sorted(a & b)
            bridges.append({
                'concept_a': c1, 'domain_a': domain_map[c1],
                'concept_b': c2, 'domain_b': domain_map[c2],
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
#  SECTION 5: MAIN
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
                        help='Number of cross-domain bridges to show')
    args = parser.parse_args()

    print()
    print('=' * 70)
    print('  FASE 3: EXPLORATION — Triadic Semantic Map')
    print('=' * 70)

    # --- Checkpoint ---
    if args.checkpoint:
        ckpt_path = args.checkpoint
    else:
        # Find best.pt in v2 checkpoints
        ckpt_path = os.path.join(SCRIPT_DIR, 'checkpoints', 'gpt2_triadic_65_v2', 'best.pt')
        if not os.path.exists(ckpt_path):
            # Fallback to latest step_*.pt
            import glob
            steps = sorted(glob.glob(os.path.join(
                SCRIPT_DIR, 'checkpoints', 'gpt2_triadic_65_v2', 'step_*.pt')))
            if steps:
                ckpt_path = steps[-1]
            else:
                print('  ERROR: No checkpoint found.')
                sys.exit(1)

    print(f'  Checkpoint: {os.path.basename(ckpt_path)}')
    print(f'  Device: {args.device}')

    # --- Concepts ---
    gold_data = load_gold_concepts()
    concepts = list(gold_data.keys())
    print(f'  Gold anchors: {len(concepts)} (8 domains)')

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
    print('[1/5] Extracting 65-bit signatures...')
    t0 = time.time()
    snap, extractor = extract_all(ckpt_path, concepts, device=args.device)
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
    active = 65 - dead
    mean_rate = sum(bit_rates) / len(bit_rates) if bit_rates else 0
    print(f'  Active bits: {active}/65 (dead: {dead})')
    print(f'  Mean activation rate: {mean_rate:.3f} (ideal: 0.50)')

    # --- Domain separation ---
    print()
    print('[3/5] Domain separation analysis...')
    dom_sep = domain_separation(snap, gold_data)

    # Cross-domain matrix
    print()
    print('  Cross-domain similarity matrix:')
    matrix, dom_names = cross_domain_matrix(snap, gold_data)
    # Header
    header = '              ' + ''.join(f'{d[:6]:>7}' for d in dom_names)
    print(f'  {header}')
    for d1 in dom_names:
        row = f'  {d1[:12]:<14}'
        for d2 in dom_names:
            val = matrix[d1][d2]
            row += f'{val:>7.3f}'
        print(row)

    # --- Cross-domain bridges ---
    print()
    print(f'[4/5] Cross-domain bridges (top {args.top_bridges})...')
    bridges = find_cross_domain_bridges(snap, gold_data, top_n=args.top_bridges)
    for b in bridges:
        print(f'    {b["concept_a"]:<20} ({b["domain_a"][:4]}) <-> '
              f'{b["concept_b"]:<20} ({b["domain_b"][:4]}) '
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

    # --- Primitive Overlay ---
    prim_path = os.path.join(DATA_DIR, 'primitivos.json')
    prim_report = None
    if os.path.exists(prim_path):
        print()
        print('  --- Primitive Overlay ---')
        # Need timeline for overlay — build single-snapshot timeline
        tracker = TimelineTracker(extractor=extractor, stability_window=1)
        timeline = tracker.analyze([snap])
        overlay = PrimitiveOverlay(primitivos_path=prim_path)
        prim_report = overlay.analyze(timeline, concepts=list(snap.codes.keys()))

        if prim_report.dual_coherence:
            print('\n  Dual Coherence:')
            for dc in prim_report.dual_coherence:
                status = 'OK' if dc.coherence_score > 0.5 else 'LOW'
                print(f'    {dc.primitive_a:<20} <-> {dc.primitive_b:<20} '
                      f'coherence={dc.coherence_score:.3f}  [{status}]')

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
        'domain_separation': dom_sep,
        'cross_domain_matrix': matrix,
        'cross_domain_bridges': bridges[:args.top_bridges],
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

    # Save all concept signatures
    results['signatures'] = {
        concept: {
            'bits': code,
            'active_indices': [i for i, v in enumerate(code) if v == 1],
            'n_active': sum(code),
            'domain': gold_data.get(concept, {}).get('domain', 'unknown'),
        }
        for concept, code in snap.codes.items()
    }

    out_path = os.path.join(RESULTS_DIR, 'exploration.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print()
    print('=' * 70)
    print(f'  Results saved to: {out_path}')
    print(f'  Signatures: {len(snap.codes)} concepts x {snap.code_dim} bits')
    print(f'  Unique: {uniq["unique_pct"]}%  Active bits: {active}/65')
    sep_mean = sum(d['separation_ratio'] for d in dom_sep.values()) / len(dom_sep) if dom_sep else 0
    print(f'  Mean domain separation: {sep_mean:.3f}')
    print(f'  Duals: {len(report.discovered_duals)}  '
          f'Deps: {len(report.discovered_deps)}  '
          f'Triadic: {len(report.discovered_triadic_deps)}')
    print('=' * 70)


if __name__ == '__main__':
    main()
