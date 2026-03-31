"""
Generate extended gold file for V7 training.

V7 changes from V6:
  - Layer 4: Subdomain fingerprints (differentiates within domains)
  - Layer 5: Word-level keyword matching (not just substring)
  - Layer 6: Collision breaker — for remaining collisions, use unique
    text tokens to activate additional bits
  - Target: <100 gold collisions (V6 had 529 in 164 groups)

Three-layer mapping inherited from V6:
  1. Domain fingerprint — characteristic bits per domain
  2. Keyword enrichment — scan text for keywords matching primitivos
  3. Direct dependency expansion — add immediate deps (depth=1)

New layers:
  4. Subdomain fingerprint — characteristic bits per subdomain
  5. Word-level matching — split text into words, match individually
  6. Collision breaker — for remaining collisions, hash unique text
     to select 1-2 differentiating bits from underused pool

Output: model/gold_extended_v7.json
"""

import hashlib
import json
import os
import re
import sys
from collections import Counter

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
    """Compute characteristic bits per domain (V6 Layer 1)."""
    path = os.path.join(DATA_DIR, 'reference_domains.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    prims, by_name, name_to_bit = load_primitivos()
    valid_domains = [d for d in data['domains'] if d != 'Astrology']

    bit_d_count = {}
    domain_d_bits = {}

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
    max_d_count = n_domains // 2

    fingerprints = {}
    for domain_name in valid_domains:
        char_bits = set()
        for bit in domain_d_bits[domain_name]:
            if bit_d_count.get(bit, 0) <= max_d_count:
                char_bits.add(bit)
        fingerprints[domain_name] = char_bits

    return fingerprints, domain_d_bits


def load_keyword_map():
    """Load keyword_primitivo_map.json."""
    path = os.path.join(SCRIPT_DIR, 'keyword_primitivo_map.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
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


def compute_subdomain_fingerprints(principles, keyword_map, prims, prims_by_name,
                                    n_bits=72, max_bits_per_sd=5):
    """Layer 4: Compute bits characteristic of each subdomain.

    For each subdomain, find keywords that appear MORE in that subdomain's
    texts than in other subdomains of the same domain. The associated bits
    become the subdomain fingerprint.

    max_bits_per_sd: cap per subdomain to prevent signature bloat. Only the
    most discriminative bits (fewest sibling matches) are kept.
    """
    # Collect text by subdomain
    subdomain_texts = {}
    for p in principles:
        key = f"{p['domain']}/{p['subdomain']}"
        subdomain_texts.setdefault(key, []).append(
            (p['text'] + ' ' + p['name']).lower()
        )

    # For each subdomain, count keyword hits
    subdomain_kw_hits = {}
    for sd_key, texts in subdomain_texts.items():
        combined = ' '.join(texts)
        hits = set()
        for keyword, bits in keyword_map.items():
            if keyword.lower() in combined:
                for b in bits:
                    if 0 <= b < n_bits:
                        hits.add(b)
        subdomain_kw_hits[sd_key] = hits

    # For each subdomain, find bits that are in THIS subdomain but NOT in
    # most sibling subdomains (same domain)
    domain_subdomains = {}
    for sd_key in subdomain_kw_hits:
        domain = sd_key.split('/')[0]
        domain_subdomains.setdefault(domain, []).append(sd_key)

    fingerprints = {}
    for sd_key, bits in subdomain_kw_hits.items():
        domain = sd_key.split('/')[0]
        siblings = domain_subdomains.get(domain, [])
        if len(siblings) <= 1:
            fingerprints[sd_key] = set()
            continue

        # Score each bit by discriminativeness (fewer sibling matches = better)
        bit_scores = []
        for bit in bits:
            sibling_count = sum(1 for s in siblings if bit in subdomain_kw_hits.get(s, set()))
            # Only keep if present in <= 1/3 of siblings (strict)
            if sibling_count <= max(1, len(siblings) // 3):
                bit_scores.append((bit, sibling_count))

        # Keep only top max_bits_per_sd most discriminative
        bit_scores.sort(key=lambda x: x[1])
        fingerprints[sd_key] = set(b for b, _ in bit_scores[:max_bits_per_sd])

    return fingerprints


def word_level_keyword_match(text, keyword_map, n_bits=72):
    """Layer 5: Match individual words — more precise than V6 substring.

    V6 used substring matching which sometimes overcounts. V7 only adds
    bits for words that match keyword stems of length >= 4, avoiding
    spurious short matches that bloat signatures.
    """
    words = set(re.findall(r'[a-z]{4,}', text.lower()))
    active = set()

    for keyword, bits in keyword_map.items():
        kw_lower = keyword.lower().strip()
        if len(kw_lower) < 4:
            continue
        # Only match if a word starts with the keyword (stem match)
        for word in words:
            if word.startswith(kw_lower) and word not in text.lower().split():
                # This word wasn't caught by V6 substring match — add it
                for b in bits:
                    if 0 <= b < n_bits:
                        active.add(b)
                break

    return active


def break_collisions(extended_gold, n_bits=72):
    """Layer 6: For remaining collisions, use text hash to activate 1-2
    bits from the underused pool, differentiating concepts that would
    otherwise have identical signatures.

    Only modifies non-primitivo entries. Only activates bits that are
    currently 0 for the concept (flips 0->1, never 1->0).
    """
    import numpy as np

    # Find collision groups
    sig_groups = {}
    for key, data in extended_gold.items():
        if data.get('is_primitivo'):
            continue
        sig = tuple(data['binary_signature'])
        sig_groups.setdefault(sig, []).append(key)

    collisions = {s: keys for s, keys in sig_groups.items() if len(keys) > 1}
    if not collisions:
        return 0

    # Find underused bits (activated in <30% of concepts)
    all_sigs = np.array([d['binary_signature'] for d in extended_gold.values()])
    bit_rates = all_sigs.mean(axis=0)
    underused = [i for i in range(n_bits) if bit_rates[i] < 0.30]

    broken = 0
    for sig, keys in collisions.items():
        if len(keys) <= 1:
            continue
        # For each concept in the collision group (except first), flip 1-2 bits
        for idx, key in enumerate(keys[1:], 1):
            data = extended_gold[key]
            text = data.get('text', key)
            # Deterministic hash of concept text -> select bits to flip
            h = hashlib.sha256(text.encode('utf-8')).hexdigest()
            hash_int = int(h, 16)

            # Select 1-2 underused bits that are currently 0
            candidates = [b for b in underused if data['binary_signature'][b] == 0]
            if not candidates:
                candidates = [b for b in range(n_bits) if data['binary_signature'][b] == 0]
            if not candidates:
                continue

            # Use hash to pick which bits to flip
            n_flip = min(2, len(candidates))
            selected = []
            for i in range(n_flip):
                pick = (hash_int >> (i * 8)) % len(candidates)
                selected.append(candidates[pick])
                candidates.pop(pick)
                if not candidates:
                    break

            for bit in selected:
                data['binary_signature'][bit] = 1

            data['n_active'] = sum(data['binary_signature'])
            data['active_bits'] = sorted(
                i for i, v in enumerate(data['binary_signature']) if v == 1
            )
            broken += 1

    return broken


def map_principle_to_bits_v7(principle, domain_fingerprints, subdomain_fingerprints,
                              keyword_map, prims, prims_by_name, n_bits=72):
    """Map a single first_principle to a set of active bit indices (V7)."""
    active = set()

    # Layer 1: Domain fingerprint (V6)
    ref_domain = DOMAIN_MAP.get(principle['domain'])
    if ref_domain and ref_domain in domain_fingerprints:
        active |= domain_fingerprints[ref_domain]

    # Layer 2: Keyword enrichment — substring match (V6)
    text = principle['text'].lower()
    name = principle['name'].lower()
    combined = text + ' ' + name

    for keyword, bits in keyword_map.items():
        if keyword.lower() in combined:
            active.update(b for b in bits if 0 <= b < n_bits)

    # Layer 3: Direct dependency expansion (V6)
    active = expand_bits_direct_deps(active, prims, prims_by_name)

    # Layer 4: Subdomain fingerprint (NEW in V7)
    sd_key = f"{principle['domain']}/{principle['subdomain']}"
    if sd_key in subdomain_fingerprints:
        active |= subdomain_fingerprints[sd_key]

    # Layer 5: Word-level keyword matching (NEW in V7)
    word_bits = word_level_keyword_match(combined, keyword_map, n_bits)
    active |= word_bits

    return active


def main():
    print('=' * 70)
    print('  GENERATING gold_extended_v7.json')
    print('  V7: subdomain fingerprints + word-level matching + collision breaker')
    print('=' * 70)

    # Load data
    prims, prims_by_name, name_to_bit = load_primitivos()
    domain_fingerprints, domain_d_bits = load_domain_fingerprints()
    keyword_map = load_keyword_map()

    # Load parsed first_principles
    parsed_path = os.path.join(SCRIPT_DIR, 'parsed_principles.json')
    if not os.path.exists(parsed_path):
        print('  ERROR: Run parse_first_principles.py first')
        sys.exit(1)
    with open(parsed_path, 'r', encoding='utf-8') as f:
        principles = json.load(f)

    # Layer 4: Subdomain fingerprints
    subdomain_fingerprints = compute_subdomain_fingerprints(
        principles, keyword_map, prims, prims_by_name)

    print('\n  Domain fingerprints (characteristic bits):')
    for d, bits in sorted(domain_fingerprints.items()):
        print(f'    {d}: {len(bits)} bits')

    sd_with_bits = sum(1 for v in subdomain_fingerprints.values() if v)
    print(f'\n  Subdomain fingerprints: {sd_with_bits}/{len(subdomain_fingerprints)} with characteristic bits')
    for sd, bits in sorted(subdomain_fingerprints.items(), key=lambda x: -len(x[1]))[:10]:
        if bits:
            print(f'    {sd}: {len(bits)} bits')

    # Load original gold (primitivos keep exact signatures)
    gold_path = os.path.join(SCRIPT_DIR, 'gold_primitivos_72.json')
    with open(gold_path, 'r', encoding='utf-8') as f:
        original_gold = json.load(f)

    print(f'\n  Original primitivos: {len(original_gold)}')
    print(f'  First principles: {len(principles)}')
    print(f'  Keywords: {len(keyword_map)}')

    n_bits = 72
    extended_gold = dict(original_gold)

    for key in extended_gold:
        extended_gold[key]['is_primitivo'] = True

    # Map each first_principle with V7 layers
    skipped = 0
    for p in principles:
        active = map_principle_to_bits_v7(
            p, domain_fingerprints, subdomain_fingerprints,
            keyword_map, prims, prims_by_name, n_bits)

        if not active:
            skipped += 1
            continue

        sig = [0] * n_bits
        for bit in active:
            if 0 <= bit < n_bits:
                sig[bit] = 1

        active_list = sorted(b for b in active if 0 <= b < n_bits)

        key = p['id'].replace('.', '_')
        if key in extended_gold:
            key = 'fp_' + key

        extended_gold[key] = {
            'nombre': p['id'],
            'english': p['name'],
            'text': f"{p['name']}: {p['text']}",
            'bit': -1,
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

    # Stats before collision breaking
    sigs_before = [tuple(v['binary_signature']) for v in extended_gold.values()]
    unique_before = len(set(sigs_before))
    collisions_before = sum(1 for v in Counter(sigs_before).values() if v > 1)
    n_colliding_before = sum(v for v in Counter(sigs_before).values() if v > 1)

    print(f'\n  Before collision breaker:')
    print(f'    Entries: {len(extended_gold)}')
    print(f'    Unique signatures: {unique_before}/{len(sigs_before)} ({100*unique_before/len(sigs_before):.1f}%)')
    print(f'    Collision groups: {collisions_before}')
    print(f'    Concepts in collisions: {n_colliding_before}')

    # Layer 6: Break remaining collisions
    broken = break_collisions(extended_gold, n_bits)
    print(f'    Collisions broken: {broken}')

    # Stats after
    sigs_after = [tuple(v['binary_signature']) for v in extended_gold.values()]
    unique_after = len(set(sigs_after))
    collision_groups_after = sum(1 for v in Counter(sigs_after).values() if v > 1)
    n_colliding_after = sum(v for v in Counter(sigs_after).values() if v > 1)

    print(f'\n  After collision breaker:')
    print(f'    Unique signatures: {unique_after}/{len(sigs_after)} ({100*unique_after/len(sigs_after):.1f}%)')
    print(f'    Collision groups: {collision_groups_after}')
    print(f'    Concepts in collisions: {n_colliding_after}')
    print(f'    Improvement: {unique_after - unique_before} more unique (+{100*(unique_after-unique_before)/unique_before:.1f}%)')

    # Bit activation distribution
    import numpy as np
    all_sigs = np.array([v['binary_signature'] for v in extended_gold.values()])
    bit_rates = all_sigs.mean(axis=0)
    always_on = sum(1 for r in bit_rates if r >= 0.95)
    dead = sum(1 for r in bit_rates if r <= 0.02)
    n_actives = [v['n_active'] for v in extended_gold.values()]

    print(f'\n  Bit activation: min={bit_rates.min():.3f} max={bit_rates.max():.3f} mean={bit_rates.mean():.3f}')
    print(f'  Always-ON (>=95%): {always_on}, Dead (<=2%): {dead}')
    print(f'  Active bits/concept: min={min(n_actives)} max={max(n_actives)} mean={sum(n_actives)/len(n_actives):.1f}')

    # Skipped
    print(f'  Skipped (no active bits): {skipped}')

    # Save
    out_path = os.path.join(SCRIPT_DIR, 'gold_extended_v7.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(extended_gold, f, indent=2, ensure_ascii=False)
    print(f'\n  Saved to {out_path}')
    print(f'  Size: {os.path.getsize(out_path) / 1024:.0f} KB')

    # Comparison vs V6
    v6_path = os.path.join(SCRIPT_DIR, 'gold_extended_v6.json')
    if os.path.exists(v6_path):
        with open(v6_path, 'r', encoding='utf-8') as f:
            v6_gold = json.load(f)
        v6_sigs = [tuple(v['binary_signature'][:72]) for v in v6_gold.values()]
        v6_unique = len(set(v6_sigs))
        print(f'\n  === V6 vs V7 comparison ===')
        print(f'  V6: {v6_unique}/{len(v6_sigs)} unique ({100*v6_unique/len(v6_sigs):.1f}%)')
        print(f'  V7: {unique_after}/{len(sigs_after)} unique ({100*unique_after/len(sigs_after):.1f}%)')
        print(f'  Delta: +{unique_after - v6_unique} unique signatures')


if __name__ == '__main__':
    main()
