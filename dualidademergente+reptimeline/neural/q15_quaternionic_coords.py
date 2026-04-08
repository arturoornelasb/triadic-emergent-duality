"""Q15 Quaternionic Coordinates: assign (r, i, j, k) to each of the 72 primitives.

Conjecture C5 from formalizacion_k.tex (P9):
  Each primitive gets explicit coordinates (r0, i0, j0, k0) in H.
  Layer constraints:
    L1-L2: i = j = k = 0  (only real axis)
    L3-L4: k = 0           (no recursive selection)
    L5:    k >= 0           (weak k if depends on consciente)
    L6:    k > 0            (observer level)

Method — four components derived from empirical data + ontological structure:
  r = mean positive activation across concepts (semantic presence)
  i = dual anti-correlation (opposition strength)
  j = normalized DAG depth (structural ordering)
  k = recursive dependency score (meta/observation level)

Cross-validated on v8 (GPT-2 Medium) and v9 (GPT-Neo 125M).

Roadmap #15.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json
import math
import argparse
from collections import defaultdict

import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'model'))
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))
RESULTS_DIR = os.path.join(SCRIPT_DIR, 'results')
sys.path.insert(0, MODEL_DIR)


# ── DAG utilities ──────────────────────────────────────────────

def build_dag(primitivos):
    """Build adjacency list from deps. Returns name->children and name->prim."""
    name_to_prim = {p['nombre']: p for p in primitivos}
    children = defaultdict(list)
    for p in primitivos:
        for dep_name in p.get('deps', []):
            if dep_name in name_to_prim:
                children[dep_name].append(p['nombre'])
    return children, name_to_prim


def compute_dag_depth(primitivos):
    """Compute topological depth for each primitive (longest path from any root)."""
    name_to_prim = {p['nombre']: p for p in primitivos}
    depths = {}

    def _depth(name):
        if name in depths:
            return depths[name]
        deps = name_to_prim[name].get('deps', [])
        valid_deps = [d for d in deps if d in name_to_prim]
        if not valid_deps:
            depths[name] = 0
            return 0
        d = max(_depth(dep) for dep in valid_deps) + 1
        depths[name] = d
        return d

    for p in primitivos:
        _depth(p['nombre'])
    return depths


def compute_meta_score(primitivos):
    """Score how 'recursive/meta' each primitive is.

    k-score = number of meta-primitives in the transitive dependency closure.
    Meta-primitives: consciente, pensar, saber, querer, decir.
    """
    META_NAMES = {'consciente', 'pensar', 'saber', 'querer', 'decir'}
    name_to_prim = {p['nombre']: p for p in primitivos}
    cache = {}

    def _meta_deps(name):
        if name in cache:
            return cache[name]
        result = set()
        if name in META_NAMES:
            result.add(name)
        deps = name_to_prim.get(name, {}).get('deps', [])
        for dep in deps:
            if dep in name_to_prim:
                result |= _meta_deps(dep)
        cache[name] = result
        return result

    scores = {}
    for p in primitivos:
        meta_deps = _meta_deps(p['nombre'])
        scores[p['nombre']] = len(meta_deps)
    return scores


# ── Dual pairs ─────────────────────────────────────────────────

def build_dual_map(primitivos):
    """Map bit -> dual_bit for primitives with explicit duals."""
    name_to_bit = {p['nombre']: p['bit'] for p in primitivos}
    dual_map = {}
    for p in primitivos:
        if 'dual' in p and p['dual'] in name_to_bit:
            dual_map[p['bit']] = name_to_bit[p['dual']]
    return dual_map


# ── Main ───────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Q15: Quaternionic coordinates for 72 primitives')
    parser.add_argument('--checkpoints', type=str, nargs='+', required=True,
                        help='One or more checkpoint paths (e.g. v8/best.pt v9/best.pt)')
    parser.add_argument('--labels', type=str, nargs='+', default=None,
                        help='Labels for each checkpoint (e.g. v8 v9)')
    parser.add_argument('--device', type=str, default='cpu')
    parser.add_argument('--gold-file', type=str, default='gold_extended_v7.json')
    args = parser.parse_args()

    if args.labels and len(args.labels) != len(args.checkpoints):
        print('Error: --labels must match --checkpoints count')
        return

    labels = args.labels or [f'ckpt{i}' for i in range(len(args.checkpoints))]

    print('=' * 65)
    print('  Q15: Quaternionic Coordinates for 72 Primitives')
    print('  Conjecture C5 — (r, i, j, k) assignment')
    print('=' * 65)

    # ── Load primitivos ──
    with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
        prim_data = json.load(f)
    primitivos = prim_data['primitivos']
    bit_to_prim = {p['bit']: p for p in primitivos}
    name_to_prim = {p['nombre']: p for p in primitivos}

    # ── Load concepts ──
    gold_path = os.path.join(MODEL_DIR, args.gold_file)
    with open(gold_path, 'r', encoding='utf-8') as f:
        gold = json.load(f)
    concepts = list(gold.keys())
    print(f'\n  Primitives: {len(primitivos)}')
    print(f'  Concepts: {len(concepts)}')

    # ── Precompute structural quantities (checkpoint-independent) ──

    # DAG depth
    dag_depths = compute_dag_depth(primitivos)
    max_depth = max(dag_depths.values()) if dag_depths else 1

    # Meta scores (for k)
    meta_scores = compute_meta_score(primitivos)
    max_meta = max(meta_scores.values()) if meta_scores else 1

    # Dual map (bit -> dual_bit)
    dual_map = build_dual_map(primitivos)

    print(f'  DAG max depth: {max_depth}')
    print(f'  Meta max score: {max_meta}')
    print(f'  Dual pairs: {len(dual_map) // 2}')

    # ── Extract continuous projections from each checkpoint ──
    from triadic_extractor import TriadicExtractor
    extractor = TriadicExtractor(n_bits=72)

    all_results = {}

    for ckpt_path, label in zip(args.checkpoints, labels):
        print(f'\n  --- Checkpoint: {label} ({os.path.basename(ckpt_path)}) ---')
        snap = extractor.extract(ckpt_path, concepts, device=args.device)

        extracted = [c for c in concepts if c in snap.continuous]
        n = len(extracted)
        print(f'  Extracted: {n} concepts with continuous projections')

        # Build matrix: (n_concepts, 72) of continuous values
        cont_matrix = np.array([snap.continuous[c] for c in extracted])  # (N, 72)

        # ── Compute r: mean positive activation ──
        # For each bit, how strongly it activates (positive) across concepts
        positive_activations = np.maximum(cont_matrix, 0)  # clip negatives
        r_raw = positive_activations.mean(axis=0)  # (72,)
        # Normalize to [0, 1]
        r_max = r_raw.max() if r_raw.max() > 0 else 1.0
        r_norm = r_raw / r_max

        # ── Compute i: dual anti-correlation ──
        i_raw = np.zeros(72)
        for bit_b in range(72):
            if bit_b not in bit_to_prim:
                continue
            prim = bit_to_prim[bit_b]
            layer = prim['capa']

            # Layer constraint: i = 0 for L1-L2
            if layer <= 2:
                i_raw[bit_b] = 0.0
                continue

            if bit_b in dual_map:
                dual_bit = dual_map[bit_b]
                # Anti-correlation with dual partner
                corr = np.corrcoef(cont_matrix[:, bit_b], cont_matrix[:, dual_bit])[0, 1]
                if np.isnan(corr):
                    corr = 0.0
                # Anti-correlation -> positive i (more opposed = higher i)
                i_raw[bit_b] = max(0.0, -corr)
            else:
                # No explicit dual: use variance as proxy for opposition
                # High variance = strong dichotomy (some concepts activate, others don't)
                std_b = cont_matrix[:, bit_b].std()
                i_raw[bit_b] = std_b

        # Normalize i to [0, 1]
        i_nonzero = i_raw[i_raw > 0]
        i_max = i_nonzero.max() if len(i_nonzero) > 0 else 1.0
        i_norm = i_raw / i_max

        # ── Compute j: DAG depth (structural ordering) ──
        j_raw = np.zeros(72)
        for bit_b in range(72):
            if bit_b not in bit_to_prim:
                continue
            prim = bit_to_prim[bit_b]
            layer = prim['capa']

            # Layer constraint: j = 0 for L1-L2
            if layer <= 2:
                j_raw[bit_b] = 0.0
                continue

            name = prim['nombre']
            depth = dag_depths.get(name, 0)
            j_raw[bit_b] = depth / max_depth

        j_norm = j_raw  # already in [0, 1]

        # ── Compute k: recursive/meta score ──
        k_raw = np.zeros(72)
        for bit_b in range(72):
            if bit_b not in bit_to_prim:
                continue
            prim = bit_to_prim[bit_b]
            layer = prim['capa']

            # Layer constraint: k = 0 for L1-L4
            if layer <= 4:
                k_raw[bit_b] = 0.0
                continue

            name = prim['nombre']
            score = meta_scores.get(name, 0)

            if layer == 6:
                # L6 always has k > 0 (minimum 0.1 even if no meta-deps)
                k_raw[bit_b] = max(score / max_meta, 0.1)
            else:
                # L5: k > 0 only if depends on meta-primitives
                k_raw[bit_b] = score / max_meta

        k_norm = k_raw  # already in [0, 1]

        # ── Assemble coordinates ──
        coords = {}
        for bit_b in range(72):
            if bit_b not in bit_to_prim:
                continue
            prim = bit_to_prim[bit_b]
            name = prim['nombre']
            layer = prim['capa']

            r_val = float(r_norm[bit_b])
            i_val = float(i_norm[bit_b])
            j_val = float(j_norm[bit_b])
            k_val = float(k_norm[bit_b])

            # Compute norms
            raw_norm = math.sqrt(r_val**2 + i_val**2 + j_val**2 + k_val**2)
            # Unit quaternion (on S3)
            if raw_norm > 0:
                q_unit = [r_val/raw_norm, i_val/raw_norm, j_val/raw_norm, k_val/raw_norm]
            else:
                q_unit = [1.0, 0.0, 0.0, 0.0]

            coords[name] = {
                'bit': bit_b,
                'prime': prim['primo'],
                'layer': layer,
                'r': round(r_val, 4),
                'i': round(i_val, 4),
                'j': round(j_val, 4),
                'k': round(k_val, 4),
                'norm': round(raw_norm, 4),
                'unit_quaternion': [round(x, 4) for x in q_unit],
                'dag_depth': dag_depths.get(name, 0),
                'meta_score': meta_scores.get(name, 0),
                'has_dual': bit_b in dual_map,
            }

        # ── Print results by layer ──
        print(f'\n  === Coordinates ({label}) ===')
        for layer in range(1, 7):
            layer_prims = [p for p in primitivos if p['capa'] == layer]
            layer_name = prim_data['capas'][str(layer)]['nombre']
            print(f'\n  Layer {layer} — {layer_name} ({len(layer_prims)} primitives)')
            print(f'  {"Primitive":<20} {"r":>6} {"i":>6} {"j":>6} {"k":>6} {"norm":>6}  {"dual":>12}')
            print(f'  {"-"*20} {"-"*6} {"-"*6} {"-"*6} {"-"*6} {"-"*6}  {"-"*12}')
            for p in layer_prims:
                c = coords[p['nombre']]
                dual_name = p.get('dual', '')
                print(f'  {p["nombre"]:<20} {c["r"]:6.3f} {c["i"]:6.3f} {c["j"]:6.3f} '
                      f'{c["k"]:6.3f} {c["norm"]:6.3f}  {dual_name:>12}')

        # ── Verify layer constraints ──
        print(f'\n  === Layer Constraint Verification ({label}) ===')
        violations = []
        for name, c in coords.items():
            layer = c['layer']
            if layer <= 2:
                if c['i'] > 0 or c['j'] > 0 or c['k'] > 0:
                    violations.append(f'  L{layer} {name}: i={c["i"]}, j={c["j"]}, k={c["k"]} (expected 0,0,0)')
            elif layer <= 4:
                if c['k'] > 0:
                    violations.append(f'  L{layer} {name}: k={c["k"]} (expected 0)')
            elif layer == 6:
                if c['k'] <= 0:
                    violations.append(f'  L6 {name}: k={c["k"]} (expected > 0)')

        if violations:
            print(f'  VIOLATIONS: {len(violations)}')
            for v in violations:
                print(f'    {v}')
        else:
            print(f'  All constraints satisfied.')

        # ── Statistics ──
        layers_r = defaultdict(list)
        layers_i = defaultdict(list)
        layers_j = defaultdict(list)
        layers_k = defaultdict(list)
        for name, c in coords.items():
            layers_r[c['layer']].append(c['r'])
            layers_i[c['layer']].append(c['i'])
            layers_j[c['layer']].append(c['j'])
            layers_k[c['layer']].append(c['k'])

        print(f'\n  === Layer Statistics ({label}) ===')
        print(f'  {"Layer":>5} {"mean_r":>7} {"mean_i":>7} {"mean_j":>7} {"mean_k":>7}')
        for layer in range(1, 7):
            mr = np.mean(layers_r[layer]) if layers_r[layer] else 0
            mi = np.mean(layers_i[layer]) if layers_i[layer] else 0
            mj = np.mean(layers_j[layer]) if layers_j[layer] else 0
            mk = np.mean(layers_k[layer]) if layers_k[layer] else 0
            print(f'  L{layer:>4} {mr:7.3f} {mi:7.3f} {mj:7.3f} {mk:7.3f}')

        all_results[label] = coords

    # ── Cross-model comparison (if multiple checkpoints) ──
    if len(all_results) >= 2:
        labels_list = list(all_results.keys())
        print(f'\n  === Cross-Model Comparison ({labels_list[0]} vs {labels_list[1]}) ===')
        c1 = all_results[labels_list[0]]
        c2 = all_results[labels_list[1]]
        common = set(c1.keys()) & set(c2.keys())

        diffs_r, diffs_i, diffs_j, diffs_k = [], [], [], []
        for name in common:
            diffs_r.append(abs(c1[name]['r'] - c2[name]['r']))
            diffs_i.append(abs(c1[name]['i'] - c2[name]['i']))
            diffs_j.append(abs(c1[name]['j'] - c2[name]['j']))
            diffs_k.append(abs(c1[name]['k'] - c2[name]['k']))

        print(f'  Common primitives: {len(common)}')
        print(f'  Mean |delta_r|: {np.mean(diffs_r):.4f}')
        print(f'  Mean |delta_i|: {np.mean(diffs_i):.4f}')
        print(f'  Mean |delta_j|: {np.mean(diffs_j):.4f}  (structural, should be 0)')
        print(f'  Mean |delta_k|: {np.mean(diffs_k):.4f}  (structural, should be 0)')

        # Correlation of r values (empirical component)
        r1 = [c1[n]['r'] for n in sorted(common)]
        r2 = [c2[n]['r'] for n in sorted(common)]
        corr_r = np.corrcoef(r1, r2)[0, 1]
        print(f'  Correlation r(v8) vs r(v9): {corr_r:.4f}')

        # Correlation of i values
        i1 = [c1[n]['i'] for n in sorted(common)]
        i2 = [c2[n]['i'] for n in sorted(common)]
        corr_i = np.corrcoef(i1, i2)[0, 1]
        print(f'  Correlation i(v8) vs i(v9): {corr_i:.4f}')

        # Most divergent primitives
        total_diffs = {}
        for name in common:
            td = math.sqrt(
                (c1[name]['r'] - c2[name]['r'])**2 +
                (c1[name]['i'] - c2[name]['i'])**2
            )
            total_diffs[name] = td
        sorted_diffs = sorted(total_diffs.items(), key=lambda x: x[1], reverse=True)
        print(f'\n  Top 5 most divergent (r,i distance):')
        for name, d in sorted_diffs[:5]:
            print(f'    {name:<20} delta={d:.4f}  '
                  f'v8=({c1[name]["r"]:.3f},{c1[name]["i"]:.3f})  '
                  f'v9=({c2[name]["r"]:.3f},{c2[name]["i"]:.3f})')

    # ── Save results ──
    os.makedirs(RESULTS_DIR, exist_ok=True)
    output = {
        'description': 'Quaternionic coordinates (r,i,j,k) for 72 primitives — Conjecture C5',
        'method': {
            'r': 'Mean positive activation across concepts (semantic presence)',
            'i': 'Dual anti-correlation or variance proxy (opposition strength)',
            'j': 'Normalized DAG depth (structural ordering)',
            'k': 'Recursive meta-dependency score (observation level)',
        },
        'constraints': {
            'L1-L2': 'i=j=k=0',
            'L3-L4': 'k=0',
            'L5': 'k>=0 (based on meta-dependencies)',
            'L6': 'k>0 (always)',
        },
        'checkpoints': {label: os.path.basename(ckpt) for label, ckpt in zip(labels, args.checkpoints)},
        'coordinates': {},
    }

    for label, coords in all_results.items():
        output['coordinates'][label] = coords

    out_path = os.path.join(RESULTS_DIR, 'q15_quaternionic_coords.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f'\n  Results saved: {out_path}')

    # ── Also save a clean CSV for the paper ──
    csv_path = os.path.join(RESULTS_DIR, 'q15_quaternionic_coords.csv')
    with open(csv_path, 'w', encoding='utf-8') as f:
        if len(all_results) == 1:
            label = list(all_results.keys())[0]
            f.write('bit,prime,name,layer,r,i,j,k,norm\n')
            for p in primitivos:
                c = all_results[label][p['nombre']]
                f.write(f'{c["bit"]},{c["prime"]},{p["nombre"]},{c["layer"]},'
                        f'{c["r"]:.4f},{c["i"]:.4f},{c["j"]:.4f},{c["k"]:.4f},{c["norm"]:.4f}\n')
        else:
            # Multi-checkpoint: include all
            f.write('bit,prime,name,layer,checkpoint,r,i,j,k,norm\n')
            for label, coords in all_results.items():
                for p in primitivos:
                    c = coords[p['nombre']]
                    f.write(f'{c["bit"]},{c["prime"]},{p["nombre"]},{c["layer"]},{label},'
                            f'{c["r"]:.4f},{c["i"]:.4f},{c["j"]:.4f},{c["k"]:.4f},{c["norm"]:.4f}\n')
    print(f'  CSV saved: {csv_path}')

    print('\n' + '=' * 65)
    print('  DONE: Quaternionic coordinates assigned to 72 primitives.')
    print('  Conjecture C5 — empirically grounded, layer-constrained.')
    print('=' * 65)


if __name__ == '__main__':
    main()
