"""
Generate extended gold file for V6 densification training.

Combines:
  - 72 original primitivos (exact same signatures from gold_primitivos_72.json)
  - ~2,000+ first_principles mapped to 72-bit signatures

Three-layer mapping for first_principles:
  1. Domain fingerprint — small set of characteristic bits per domain
     (D in this domain but NOT D in most others)
  2. Keyword enrichment — scan text for keywords matching primitivos
  3. Direct dependency expansion — add immediate deps (depth=1) only

Output: model/gold_extended_v6.json
"""

import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
DATA_DIR = os.path.join(REPO_ROOT, 'data')

# Domain mapping: first_principles domain -> reference_domains.json domain
DOMAIN_MAP = {
    '01_mathematics': 'Mathematics',
    '02_physics': 'Physics',
    '03_chemistry': 'Chemistry',
    '04_biology': 'Biology',
    '05_earth_sciences': 'Physics',
    '06_computer_science': 'Mathematics',
    '07_formal_sciences': 'Mathematics',
    '08_social_sciences': 'Psychology',
    '09_philosophy_of_science': 'Philosophy',
    '10_interdisciplinary': 'Physics',
    '11_engineering': 'Physics',
    '12_medical_sciences': 'Biology',
    '13_architecture_and_design': 'Physics',
    '14_agricultural_sciences': 'Biology',
}


def load_primitivos():
    """Load primitivos.json and build lookup structures."""
    path = os.path.join(DATA_DIR, 'primitivos.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    prims = data['primitivos']
    by_name = {p['nombre']: p for p in prims}
    name_to_bit = {p['nombre']: p['bit'] for p in prims}
    return prims, by_name, name_to_bit


def load_domain_fingerprints():
    """Compute characteristic bits per domain.

    A bit is "characteristic" of a domain if it's D there but NOT D in
    at least MIN_ABSENT other domains. This gives a small fingerprint
    (typically 3-12 bits) that discriminates domains from each other.
    """
    path = os.path.join(DATA_DIR, 'reference_domains.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    prims, by_name, name_to_bit = load_primitivos()

    # Skip Astrology (negative control)
    valid_domains = [d for d in data['domains'] if d != 'Astrology']

    # Count how many domains classify each bit as D
    bit_d_count = {}  # bit -> count of domains where it's D
    domain_d_bits = {}  # domain -> set of D bits

    for domain_name in valid_domains:
        classes = data['domains'][domain_name].get('classes', {})
        d_bits = set()
        for prim_name, classification in classes.items():
            if classification == 'D' and prim_name in name_to_bit:
                bit = name_to_bit[prim_name]
                d_bits.add(bit)
                bit_d_count[bit] = bit_d_count.get(bit, 0) + 1
        domain_d_bits[domain_name] = d_bits

    n_domains = len(valid_domains)
    # A bit is characteristic if D in <= half the domains
    max_d_count = n_domains // 2  # D in at most 4/8 domains

    fingerprints = {}
    for domain_name in valid_domains:
        char_bits = set()
        for bit in domain_d_bits[domain_name]:
            if bit_d_count.get(bit, 0) <= max_d_count:
                char_bits.add(bit)
        fingerprints[domain_name] = char_bits

    return fingerprints


def load_keyword_map():
    """Load keyword_primitivo_map.json."""
    path = os.path.join(SCRIPT_DIR, 'keyword_primitivo_map.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Remove comment key
    data.pop('_comment', None)
    return data


def expand_bits_direct_deps(active_bits, prims, prims_by_name):
    """Given active bit indices, add only immediate (depth=1) deps."""
    bit_to_name = {p['bit']: p['nombre'] for p in prims}
    expanded = set(active_bits)
    for bit in list(active_bits):
        name = bit_to_name.get(bit)
        if name:
            p = prims_by_name.get(name)
            if p:
                for dep_name in p.get('deps', []):
                    if dep_name in prims_by_name:
                        expanded.add(prims_by_name[dep_name]['bit'])
    return expanded


def map_principle_to_bits(principle, domain_fingerprints, keyword_map, prims, prims_by_name):
    """Map a single first_principle to a set of active bit indices."""
    active = set()

    # Layer 1: Domain fingerprint (characteristic bits only)
    ref_domain = DOMAIN_MAP.get(principle['domain'])
    if ref_domain and ref_domain in domain_fingerprints:
        active |= domain_fingerprints[ref_domain]

    # Layer 2: Keyword enrichment
    text = principle['text'].lower()
    name = principle['name'].lower()
    combined = text + ' ' + name

    for keyword, bits in keyword_map.items():
        if keyword.lower() in combined:
            active.update(bits)

    # Layer 3: Direct dependency expansion (depth=1 only)
    active = expand_bits_direct_deps(active, prims, prims_by_name)

    return active


def main():
    print('=' * 70)
    print('  GENERATING gold_extended_v6.json')
    print('=' * 70)

    # Load data
    prims, prims_by_name, name_to_bit = load_primitivos()
    domain_fingerprints = load_domain_fingerprints()
    keyword_map = load_keyword_map()

    # Show fingerprint sizes
    print('\n  Domain fingerprints (characteristic bits):')
    for d, bits in sorted(domain_fingerprints.items()):
        print(f'    {d}: {len(bits)} bits')

    # Load original gold (primitivos keep exact signatures)
    gold_path = os.path.join(SCRIPT_DIR, 'gold_primitivos_72.json')
    with open(gold_path, 'r', encoding='utf-8') as f:
        original_gold = json.load(f)

    # Load parsed first_principles
    parsed_path = os.path.join(SCRIPT_DIR, 'parsed_principles.json')
    if not os.path.exists(parsed_path):
        print('  ERROR: Run parse_first_principles.py first')
        sys.exit(1)
    with open(parsed_path, 'r', encoding='utf-8') as f:
        principles = json.load(f)

    print(f'  Original primitivos: {len(original_gold)}')
    print(f'  First principles: {len(principles)}')
    print(f'  Reference domains: {len(domain_fingerprints)}')
    print(f'  Keywords: {len(keyword_map)}')

    n_bits = 72
    extended_gold = dict(original_gold)  # Start with original

    # Mark originals
    for key in extended_gold:
        extended_gold[key]['is_primitivo'] = True

    # Map each first_principle
    skipped = 0
    for p in principles:
        active = map_principle_to_bits(p, domain_fingerprints, keyword_map, prims, prims_by_name)

        if not active:
            skipped += 1
            continue

        sig = [0] * n_bits
        for bit in active:
            if 0 <= bit < n_bits:
                sig[bit] = 1

        active_list = sorted(b for b in active if 0 <= b < n_bits)

        key = p['id'].replace('.', '_')
        # Avoid collisions with original primitivos
        if key in extended_gold:
            key = 'fp_' + key

        extended_gold[key] = {
            'nombre': p['id'],
            'english': p['name'],
            'text': f"{p['name']}: {p['text']}",
            'bit': -1,  # Not a primitivo
            'capa': 0,
            'binary_signature': sig,
            'n_active': sum(sig),
            'active_bits': active_list,
            'dual': None,
            'deps_es': [],
            'source_domain': p['domain'],
            'source_subdomain': p['subdomain'],
            'is_primitivo': False,
        }

    print(f'\n  Extended gold entries: {len(extended_gold)}')
    print(f'  Original primitivos: {sum(1 for v in extended_gold.values() if v.get("is_primitivo"))}')
    print(f'  First principles: {sum(1 for v in extended_gold.values() if not v.get("is_primitivo"))}')
    print(f'  Skipped (no active bits): {skipped}')

    # Stats
    sigs = [tuple(v['binary_signature']) for v in extended_gold.values()]
    unique_sigs = len(set(sigs))
    print(f'\n  Unique signatures: {unique_sigs}/{len(sigs)} ({100*unique_sigs/len(sigs):.1f}%)')

    # Bit activation distribution
    import numpy as np
    all_sigs = np.array([v['binary_signature'] for v in extended_gold.values()])
    bit_rates = all_sigs.mean(axis=0)
    always_on = sum(1 for r in bit_rates if r >= 0.95)
    dead = sum(1 for r in bit_rates if r <= 0.02)
    print(f'  Bit activation: min={bit_rates.min():.3f} max={bit_rates.max():.3f} mean={bit_rates.mean():.3f}')
    print(f'  Always-ON (>=95%): {always_on}')
    print(f'  Dead (<=2%): {dead}')

    # Per-domain stats
    print('\n  Per-domain breakdown:')
    domain_counts = {}
    for v in extended_gold.values():
        d = v.get('source_domain', 'primitivo')
        domain_counts[d] = domain_counts.get(d, 0) + 1
    for d in sorted(domain_counts.keys()):
        print(f'    {d}: {domain_counts[d]}')

    # N_active distribution
    n_actives = [v['n_active'] for v in extended_gold.values()]
    print(f'\n  Active bits per concept: min={min(n_actives)} max={max(n_actives)} '
          f'mean={sum(n_actives)/len(n_actives):.1f}')

    # Save
    out_path = os.path.join(SCRIPT_DIR, 'gold_extended_v6.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(extended_gold, f, indent=2, ensure_ascii=False)
    print(f'\n  Saved to {out_path}')
    print(f'  Size: {os.path.getsize(out_path) / 1024:.0f} KB')


if __name__ == '__main__':
    main()
