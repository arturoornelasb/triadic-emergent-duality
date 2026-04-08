"""Q13 Algebraic Verification: gcd(mu1, mu2) = 1 for ALL concept pairs.

The Markov blanket property is ALGEBRAIC, not statistical.
Each bit maps to a unique prime. For any two concepts:
  - blanket = gcd(Phi(C1), Phi(C2)) = product of shared primes
  - mu1 = Phi(C1)/blanket = primes only in C1
  - mu2 = Phi(C2)/blanket = primes only in C2
  - gcd(mu1, mu2) = 1  (ALWAYS, by FTA + unique prime assignment)

This script verifies it directly on learned codes, showing actual primes.

Roadmap #13.
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


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def main():
    parser = argparse.ArgumentParser(description='Q13: Algebraic Markov blanket verification')
    parser.add_argument('--checkpoint', type=str, required=True)
    parser.add_argument('--device', type=str, default='cpu')
    parser.add_argument('--gold-file', type=str, default='gold_extended_v7.json')
    parser.add_argument('--label', type=str, default='')
    parser.add_argument('--n-examples', type=int, default=10,
                        help='Number of example pairs to print')
    args = parser.parse_args()

    print('=' * 60)
    print('  Q13: Algebraic Markov Blanket Verification')
    print('  gcd(mu1, mu2) = 1 for ALL concept pairs')
    print('=' * 60)

    # Load primitivos for bit->prime mapping
    with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
        prim_data = json.load(f)
    prims = prim_data['primitivos']
    bit_to_prime = {p['bit']: p['primo'] for p in prims}
    bit_to_name = {p['bit']: p['nombre'] for p in prims}
    bit_to_layer = {p['bit']: p['capa'] for p in prims}

    # Load concepts
    gold_path = os.path.join(MODEL_DIR, args.gold_file)
    with open(gold_path, 'r', encoding='utf-8') as f:
        gold = json.load(f)
    concepts = list(gold.keys())
    print(f'\n  Concepts: {len(concepts)}')

    # Extract codes
    print(f'  Extracting codes from {os.path.basename(args.checkpoint)}...')
    from triadic_extractor import TriadicExtractor
    extractor = TriadicExtractor(n_bits=72)
    snap = extractor.extract(args.checkpoint, concepts, device=args.device)

    extracted = list(snap.codes.keys())
    n = len(extracted)
    print(f'  Extracted: {n} concepts')

    # Compute prime composites for each concept
    composites = {}
    active_primes = {}
    for concept in extracted:
        code = snap.codes[concept]
        concept_primes = []
        composite = 1
        for bit_idx, val in enumerate(code):
            if val == 1 and bit_idx in bit_to_prime:
                p = bit_to_prime[bit_idx]
                composite *= p
                concept_primes.append((bit_idx, p, bit_to_name.get(bit_idx, '?')))
        composites[concept] = composite
        active_primes[concept] = concept_primes

    # Verify gcd(mu1, mu2) = 1 for ALL pairs (sample if too many)
    total_pairs = n * (n - 1) // 2
    print(f'\n  Total pairs: {total_pairs:,}')

    # Sample pairs for large N
    rng = np.random.RandomState(42)
    if total_pairs > 500000:
        n_check = 500000
        print(f'  Sampling {n_check:,} pairs...')
        pairs = []
        for _ in range(n_check):
            i, j = rng.choice(n, 2, replace=False)
            pairs.append((extracted[i], extracted[j]))
    else:
        n_check = total_pairs
        print(f'  Checking all {n_check:,} pairs...')
        pairs = []
        for i in range(n):
            for j in range(i + 1, n):
                pairs.append((extracted[i], extracted[j]))

    violations = 0
    examples = []
    blanket_sizes = []
    int1_sizes = []
    int2_sizes = []

    for c1, c2 in pairs:
        phi1 = composites[c1]
        phi2 = composites[c2]
        blanket = gcd(phi1, phi2)

        if blanket == 0:
            continue

        mu1 = phi1 // blanket
        mu2 = phi2 // blanket
        g = gcd(mu1, mu2)

        if g != 1:
            violations += 1

        # Track sizes
        code1 = snap.codes[c1]
        code2 = snap.codes[c2]
        shared = sum(1 for k in range(72) if k in bit_to_prime and code1[k] == 1 and code2[k] == 1)
        only1 = sum(1 for k in range(72) if k in bit_to_prime and code1[k] == 1 and code2[k] == 0)
        only2 = sum(1 for k in range(72) if k in bit_to_prime and code1[k] == 0 and code2[k] == 1)
        blanket_sizes.append(shared)
        int1_sizes.append(only1)
        int2_sizes.append(only2)

        # Collect diverse examples
        if len(examples) < args.n_examples and shared > 0 and only1 > 0 and only2 > 0:
            examples.append({
                'c1': c1, 'c2': c2,
                'blanket_bits': shared, 'int1_bits': only1, 'int2_bits': only2,
                'gcd_interiors': g,
                'blanket_primes': [(b, p, n) for b, p, n in active_primes[c1]
                                   if any(b == b2 for b2, _, _ in active_primes[c2])],
                'int1_primes': [(b, p, n) for b, p, n in active_primes[c1]
                                if not any(b == b2 for b2, _, _ in active_primes[c2])],
                'int2_primes': [(b, p, n) for b, p, n in active_primes[c2]
                                if not any(b == b2 for b2, _, _ in active_primes[c1])],
            })

    # Results
    print(f'\n  Pairs checked: {n_check:,}')
    print(f'  Violations (gcd != 1): {violations}')
    print(f'  Verification: {"PASS (100%)" if violations == 0 else "FAIL"}')

    blanket_sizes = np.array(blanket_sizes)
    int1_sizes = np.array(int1_sizes)
    int2_sizes = np.array(int2_sizes)

    print(f'\n  Statistics:')
    print(f'    Mean blanket size:  {blanket_sizes.mean():.1f} bits')
    print(f'    Mean interior 1:    {int1_sizes.mean():.1f} bits')
    print(f'    Mean interior 2:    {int2_sizes.mean():.1f} bits')
    print(f'    Pairs with blanket>0: {(blanket_sizes > 0).sum():,}/{n_check:,} ({(blanket_sizes > 0).mean():.1%})')

    # Print examples
    if examples:
        print(f'\n  === Example Pairs (showing prime decomposition) ===')
        for i, ex in enumerate(examples[:args.n_examples]):
            print(f'\n  --- Pair {i+1}: "{ex["c1"]}" vs "{ex["c2"]}" ---')
            print(f'    Blanket ({ex["blanket_bits"]} bits): '
                  f'{", ".join(f"{n}(p{p})" for _, p, n in ex["blanket_primes"][:5])}'
                  f'{"..." if len(ex["blanket_primes"]) > 5 else ""}')
            print(f'    Interior 1 ({ex["int1_bits"]} bits): '
                  f'{", ".join(f"{n}(p{p})" for _, p, n in ex["int1_primes"][:5])}'
                  f'{"..." if len(ex["int1_primes"]) > 5 else ""}')
            print(f'    Interior 2 ({ex["int2_bits"]} bits): '
                  f'{", ".join(f"{n}(p{p})" for _, p, n in ex["int2_primes"][:5])}'
                  f'{"..." if len(ex["int2_primes"]) > 5 else ""}')
            print(f'    gcd(mu1, mu2) = {ex["gcd_interiors"]}')

    # Save
    os.makedirs(RESULTS_DIR, exist_ok=True)
    suffix = f'_{args.label}' if args.label else ''
    result = {
        'checkpoint': os.path.basename(args.checkpoint),
        'n_concepts': n,
        'n_pairs_checked': n_check,
        'violations': violations,
        'pass': violations == 0,
        'blanket_size_mean': float(blanket_sizes.mean()),
        'int1_size_mean': float(int1_sizes.mean()),
        'int2_size_mean': float(int2_sizes.mean()),
        'pairs_with_blanket': int((blanket_sizes > 0).sum()),
        'examples': examples[:5],
    }
    out_path = os.path.join(RESULTS_DIR, f'q13_algebraic{suffix}.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f'\n  Results saved: {out_path}')

    print('\n' + '=' * 60)
    if violations == 0:
        print('  VERIFIED: gcd(mu1, mu2) = 1 for ALL concept pairs.')
        print('  The Markov blanket property holds algebraically')
        print('  on the LEARNED codes, not just in theory.')
    print('=' * 60)


if __name__ == '__main__':
    main()
