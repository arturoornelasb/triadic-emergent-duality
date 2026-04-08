"""Q32 Inter-rater reliability: model-based second rater for D/A/N classification.

The first rater (reference_domains.json) classified each of the 72 primitives
as D (Definitorio), A (Accesorio), or N (No aplica) for each domain.

The second rater is the TRAINED MODEL: for each domain, we compute
how often each primitive bit is active in domain concepts vs non-domain concepts.
Classification rule:
  D: activation rate in domain significantly higher than baseline (ratio > 1.5)
  N: activation rate in domain significantly lower than baseline (ratio < 0.5)
  A: everything else

This is an INDEPENDENT rater — the model learned from text, not from
the human D/A/N annotations. Cohen's kappa between human and model
measures how much the learned representations agree with expert judgment.

Roadmap #32.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json
import csv
import math
from collections import defaultdict

import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'model'))
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))
RESULTS_DIR = os.path.join(SCRIPT_DIR, 'results')
RATER_DIR = os.path.join(DATA_DIR, 'interrater')
sys.path.insert(0, MODEL_DIR)


def cohens_kappa(labels_a, labels_b, categories=None):
    """Cohen's kappa for inter-rater reliability."""
    n = len(labels_a)
    if n == 0:
        return {'kappa': 0.0, 'p_observed': 0.0, 'p_expected': 0.0,
                'interpretation': 'no_data', 'n': 0, 'confusion': {}}

    if categories is None:
        categories = sorted(set(labels_a) | set(labels_b))

    matrix = {c1: {c2: 0 for c2 in categories} for c1 in categories}
    for a, b in zip(labels_a, labels_b):
        if a in matrix and b in matrix[a]:
            matrix[a][b] += 1

    p_o = sum(matrix[c][c] for c in categories) / n
    p_e = 0.0
    for c in categories:
        p_a = sum(matrix[c][c2] for c2 in categories) / n
        p_b = sum(matrix[c1][c] for c1 in categories) / n
        p_e += p_a * p_b

    if abs(1 - p_e) < 1e-10:
        kappa = 1.0 if p_o == 1.0 else 0.0
    else:
        kappa = (p_o - p_e) / (1 - p_e)

    if kappa < 0:       interp = 'poor'
    elif kappa < 0.21:  interp = 'slight'
    elif kappa < 0.41:  interp = 'fair'
    elif kappa < 0.61:  interp = 'moderate'
    elif kappa < 0.81:  interp = 'substantial'
    else:               interp = 'almost_perfect'

    return {
        'kappa': round(kappa, 4),
        'p_observed': round(p_o, 4),
        'p_expected': round(p_e, 4),
        'interpretation': interp,
        'n': n,
        'confusion': {c1: dict(matrix[c1]) for c1 in categories},
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Q32: Model-based inter-rater reliability')
    parser.add_argument('--checkpoint', type=str, required=True)
    parser.add_argument('--device', type=str, default='cpu')
    parser.add_argument('--gold-file', type=str, default='gold_extended_v7.json')
    parser.add_argument('--d-threshold', type=float, default=1.5,
                        help='Ratio threshold for D classification')
    parser.add_argument('--n-threshold', type=float, default=0.5,
                        help='Ratio threshold for N classification')
    args = parser.parse_args()

    print('=' * 70)
    print('  Q32: Inter-Rater Reliability — Model as Second Rater')
    print('=' * 70)

    # Load primitivos
    with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
        prim_data = json.load(f)
    primitivos = prim_data['primitivos']
    bit_to_name = {p['bit']: p['nombre'] for p in primitivos}
    name_to_bit = {p['nombre']: p['bit'] for p in primitivos}

    # Load reference domains (rater 1)
    with open(os.path.join(DATA_DIR, 'reference_domains.json'), 'r', encoding='utf-8') as f:
        dom_data = json.load(f)

    # Load gold concepts
    gold_path = os.path.join(MODEL_DIR, args.gold_file)
    with open(gold_path, 'r', encoding='utf-8') as f:
        gold = json.load(f)
    concepts = list(gold.keys())

    # Extract binary codes from checkpoint
    print(f'\n  Extracting codes from {os.path.basename(args.checkpoint)}...')
    from triadic_extractor import TriadicExtractor
    extractor = TriadicExtractor(n_bits=72)
    snap = extractor.extract(args.checkpoint, concepts, device=args.device)
    extracted = [c for c in concepts if c in snap.codes]
    print(f'  Extracted: {len(extracted)} concepts')

    # Build code matrix: (n_concepts, 72)
    code_matrix = np.array([snap.codes[c] for c in extracted])  # (N, 72)

    # Global activation rate per bit
    global_rate = code_matrix.mean(axis=0)  # (72,)

    # For each domain, identify which concepts belong to it
    # Gold concepts have prefixes like "01_mathematics_...", "02_physics_...", etc.
    DOMAIN_PREFIX_MAP = {
        'Mathematics': ['01_mathematics', '07_formal'],
        'Physics': ['02_physics'],
        'Chemistry': ['03_chemistry'],
        'Biology': ['04_biology'],
        'Philosophy': ['09_philosophy'],
        'Linguistics': ['08_social'],
        'Psychology': ['08_social', '12_medical'],
        'Music': [],
        'Astrology': [],
        'Alchemy': [],
        'Phrenology': [],
    }
    DOMAIN_KEYWORDS = {
        'Music': ['music', 'harmon', 'rhythm', 'melody', 'chord', 'song', 'note',
                  'tempo', 'pitch', 'scale', 'symphony', 'opera', 'instrument',
                  'acoustic', 'sonic', 'tonal', 'compos'],
        'Linguistics': ['linguist', 'syntax', 'semantic', 'phonolog', 'morpholog',
                        'grammar', 'language', 'discourse', 'pragmatic', 'lexic'],
        'Psychology': ['psycholog', 'cogniti', 'emotion', 'behavior', 'perception',
                       'memory', 'motivation', 'personality', 'conscious', 'mental'],
        'Astrology': ['zodiac', 'horoscope', 'constellation', 'natal', 'retrograde',
                      'astrolog', 'celestial'],
        'Alchemy': ['transmut', 'philosopher', 'elixir', 'alchemi', 'quintessence'],
        'Phrenology': ['phrenolog', 'skull', 'cranium', 'bump', 'cranial'],
    }

    domain_concepts = {}
    for domain_name in dom_data['domains']:
        matching = set()
        prefixes = DOMAIN_PREFIX_MAP.get(domain_name, [])
        for concept in extracted:
            for prefix in prefixes:
                if concept.startswith(prefix):
                    matching.add(concept)
                    break
        keywords = DOMAIN_KEYWORDS.get(domain_name, [])
        if keywords:
            for concept in extracted:
                text = gold.get(concept, {}).get('text', '').lower()
                if any(kw in concept.lower() or kw in text for kw in keywords):
                    matching.add(concept)
        domain_concepts[domain_name] = list(matching)

    # Compute model-based D/A/N for each domain
    all_results = {}
    os.makedirs(RATER_DIR, exist_ok=True)

    for domain_name, domain_info in dom_data['domains'].items():
        dom_concepts = domain_concepts.get(domain_name, [])
        if len(dom_concepts) < 3:
            print(f'\n  {domain_name}: skipping (only {len(dom_concepts)} concepts found)')
            continue

        # Domain activation rate per bit
        dom_codes = np.array([snap.codes[c] for c in dom_concepts])
        dom_rate = dom_codes.mean(axis=0)

        # Ratio: domain rate / global rate (with smoothing)
        epsilon = 0.01
        ratio = (dom_rate + epsilon) / (global_rate + epsilon)

        # Classify
        model_classes = {}
        for p in primitivos:
            bit = p['bit']
            r = ratio[bit]
            if r >= args.d_threshold:
                model_classes[p['nombre']] = 'D'
            elif r <= args.n_threshold:
                model_classes[p['nombre']] = 'N'
            else:
                model_classes[p['nombre']] = 'A'

        # Rater 1 classes
        rater1 = domain_info.get('classes', domain_info)
        if isinstance(rater1, dict) and 'classes' in rater1:
            rater1 = rater1['classes']

        # Build parallel arrays
        labels_1, labels_2 = [], []
        for p in primitivos:
            name = p['nombre']
            if name in rater1 and name in model_classes:
                labels_1.append(rater1[name])
                labels_2.append(model_classes[name])

        kappa = cohens_kappa(labels_1, labels_2, ['D', 'A', 'N'])

        # Print results
        status = domain_info.get('validation_status', '?')
        print(f'\n  === {domain_name} (status={status}, {len(dom_concepts)} concepts) ===')
        print(f'    Cohen kappa: {kappa["kappa"]:.3f} ({kappa["interpretation"]})')
        print(f'    Agreement:   {kappa["p_observed"]:.3f} (chance: {kappa["p_expected"]:.3f})')

        # Confusion matrix
        print(f'    Confusion (Human rows, Model cols):')
        print(f'    {"":>6} {"D":>5} {"A":>5} {"N":>5}')
        for cat in ['D', 'A', 'N']:
            row = kappa['confusion'].get(cat, {})
            print(f'    {cat:>6} {row.get("D",0):>5} {row.get("A",0):>5} {row.get("N",0):>5}')

        # Count disagreements
        n_disagree = sum(1 for a, b in zip(labels_1, labels_2) if a != b)
        print(f'    Disagreements: {n_disagree}/{len(labels_1)}')

        # Save rater2 CSV
        csv_path = os.path.join(RATER_DIR, f'{domain_name}_rater2.csv')
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['primitivo', 'capa', 'definicion', 'clasificacion_DAN',
                             'domain_rate', 'global_rate', 'ratio'])
            for p in primitivos:
                bit = p['bit']
                writer.writerow([
                    p['nombre'], p['capa'], p['def'],
                    model_classes[p['nombre']],
                    f'{dom_rate[bit]:.4f}', f'{global_rate[bit]:.4f}',
                    f'{ratio[bit]:.4f}'
                ])

        all_results[domain_name] = {
            'kappa': kappa['kappa'],
            'interpretation': kappa['interpretation'],
            'agreement': kappa['p_observed'],
            'n_concepts': len(dom_concepts),
            'n_disagreements': n_disagree,
            'status': status,
            'confusion': kappa['confusion'],
        }

    # Summary
    print('\n' + '=' * 70)
    print('  SUMMARY')
    print('=' * 70)
    print(f'\n  {"Domain":<15} {"Kappa":>6} {"Interp":<15} {"Agree":>6} {"Concepts":>8} {"Status":<15}')
    print(f'  {"-"*15} {"-"*6} {"-"*15} {"-"*6} {"-"*8} {"-"*15}')

    kappas_real = []
    kappas_control = []
    for name, r in sorted(all_results.items(), key=lambda x: x[1]['kappa'], reverse=True):
        print(f'  {name:<15} {r["kappa"]:6.3f} {r["interpretation"]:<15} '
              f'{r["agreement"]:6.3f} {r["n_concepts"]:>8} {r["status"]:<15}')
        if r['status'] in ('validated', 'candidate'):
            kappas_real.append(r['kappa'])
        else:
            kappas_control.append(r['kappa'])

    if kappas_real:
        print(f'\n  Real domains mean kappa: {np.mean(kappas_real):.3f}')
    if kappas_control:
        print(f'  Control domains mean kappa: {np.mean(kappas_control):.3f}')
    if kappas_real and kappas_control:
        gap = np.mean(kappas_real) - np.mean(kappas_control)
        print(f'  Gap (real - control): {gap:.3f}')

    # Save
    os.makedirs(RESULTS_DIR, exist_ok=True)
    output = {
        'description': 'Inter-rater reliability: human vs model-based D/A/N classification',
        'method': 'Model activation ratio (domain_rate / global_rate) with thresholds',
        'thresholds': {'D': f'>= {args.d_threshold}', 'N': f'<= {args.n_threshold}', 'A': 'otherwise'},
        'checkpoint': os.path.basename(args.checkpoint),
        'results': all_results,
    }
    out_path = os.path.join(RESULTS_DIR, 'q32_interrater.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f'\n  Results saved: {out_path}')
    print(f'  Rater2 CSVs saved in: {RATER_DIR}')

    print('\n' + '=' * 70)


if __name__ == '__main__':
    main()
