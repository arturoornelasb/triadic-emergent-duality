"""
Parse first_principles markdown files into structured JSON.

Input:  C:\research\first_principles\{domain}\{subdomain}\first_principles.md
Output: model/parsed_principles.json

Each principle entry:
  {id, domain, subdomain, type, number, name, text, depends_on}
"""

import json
import os
import re
import sys

FIRST_PRINCIPLES_ROOT = r'C:\research\first_principles'

# Pattern: ### TYPE N: Name  OR  #### AXIOM N.M: Name  OR  ### TYPE CODE --- Name
HEADER_RE = re.compile(
    r'^#{3,4}\s+'
    r'(AXIOM SYSTEM|AXIOM|LAW|POSTULATE|PRINCIPLE|THEOREM|CONVENTION|DEFINITION|RULE|HYPOTHESIS|CONJECTURE|LEMMA|COROLLARY|PROPERTY|CRITERION|FRAMEWORK|CONCEPT|PROPOSITION|CONSTRAINT|STANDARD|IDENTITY|INEQUALITY|FORMULA)\s+'
    r'([\w.]+?)(?::\s*|\s+---\s+)(.+)',
    re.IGNORECASE
)

# Field patterns — handle both "- **Field:** text" and "**Field:**\ntext" formats
PLAIN_RE = re.compile(r'^\s*-?\s*\*\*Plain Language:\*\*\s*(.*)', re.IGNORECASE)
DEPENDS_RE = re.compile(r'^\s*-?\s*\*\*Depends On:\*\*\s*(.*)', re.IGNORECASE)
# Any bold field marker (to detect end of multiline content)
FIELD_RE = re.compile(r'^\s*-?\s*\*\*\w+', re.IGNORECASE)


def first_sentence(text):
    """Extract first sentence, capped at ~60 words."""
    text = text.strip()
    # Split on sentence-ending punctuation followed by space or end
    m = re.match(r'(.+?[.!?])(?:\s|$)', text)
    if m:
        sent = m.group(1)
    else:
        sent = text
    # Cap length
    words = sent.split()
    if len(words) > 60:
        sent = ' '.join(words[:60]) + '.'
    return sent.strip()


def parse_file(filepath, domain, subdomain):
    """Parse a single first_principles.md file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    principles = []
    current = None
    reading_field = None  # 'plain' or 'depends' for multiline

    def save_current():
        if current and current.get('_plain'):
            current['text'] = first_sentence(current['_plain'])
        if current:
            for k in ('_plain', '_depends_raw'):
                if k in current:
                    if k == '_depends_raw':
                        current['depends_on'] = current[k]
                    del current[k]
            if current.get('text'):
                principles.append(current)

    for line in lines:
        line_stripped = line.rstrip('\n')

        # Check for principle header
        m = HEADER_RE.match(line_stripped)
        if m:
            save_current()
            reading_field = None

            ptype = m.group(1).upper()
            number = m.group(2)
            name = m.group(3).strip()

            # Skip AXIOM SYSTEM headers (we'll capture sub-axioms)
            if ptype == 'AXIOM SYSTEM':
                current = None
                continue

            pid = f"{domain}.{subdomain}.{ptype}_{number}".lower()
            current = {
                'id': pid,
                'domain': domain,
                'subdomain': subdomain,
                'type': ptype,
                'number': number,
                'name': name,
                'text': '',
                'depends_on': '',
                '_plain': '',
                '_depends_raw': '',
            }
            continue

        if current is None:
            continue

        # Check for Plain Language field
        pm = PLAIN_RE.match(line_stripped)
        if pm:
            txt = pm.group(1).strip()
            current['_plain'] = txt
            reading_field = 'plain' if not txt else None
            continue

        # Check for Depends On field
        dm = DEPENDS_RE.match(line_stripped)
        if dm:
            txt = dm.group(1).strip()
            current['_depends_raw'] = txt
            reading_field = 'depends' if not txt else None
            continue

        # Any other bold field marker ends multiline reading
        if FIELD_RE.match(line_stripped) or line_stripped.startswith('###'):
            reading_field = None
            continue

        # Separator lines end multiline
        if line_stripped.strip() == '---' or line_stripped.strip() == '--':
            reading_field = None
            continue

        # Multiline continuation or first line after empty field marker
        content = line_stripped.strip()
        if not content:
            continue

        if reading_field == 'plain':
            if current['_plain']:
                current['_plain'] += ' ' + content
            else:
                current['_plain'] = content
            reading_field = None  # Only take first paragraph
            continue

        if reading_field == 'depends':
            if current['_depends_raw']:
                current['_depends_raw'] += ' ' + content
            else:
                current['_depends_raw'] = content
            reading_field = None
            continue

        # Regular content continuation for plain language
        if current.get('_plain') and not FIELD_RE.match(line_stripped):
            if reading_field is None and not line_stripped.startswith('#'):
                pass  # Don't append random content

    save_current()
    return principles


def parse_all(root=FIRST_PRINCIPLES_ROOT):
    """Parse all first_principles.md files."""
    all_principles = []
    domain_dirs = sorted(d for d in os.listdir(root)
                         if os.path.isdir(os.path.join(root, d))
                         and d[0].isdigit())

    for domain_dir in domain_dirs:
        domain_path = os.path.join(root, domain_dir)
        subdomain_dirs = sorted(d for d in os.listdir(domain_path)
                                if os.path.isdir(os.path.join(domain_path, d)))

        for sub_dir in subdomain_dirs:
            fp_path = os.path.join(domain_path, sub_dir, 'first_principles.md')
            if not os.path.exists(fp_path):
                continue

            principles = parse_file(fp_path, domain_dir, sub_dir)
            all_principles.extend(principles)

    return all_principles


def main():
    print('Parsing first_principles...')
    principles = parse_all()
    print(f'  Total principles parsed: {len(principles)}')

    # Stats
    domains = {}
    types = {}
    for p in principles:
        domains[p['domain']] = domains.get(p['domain'], 0) + 1
        types[p['type']] = types.get(p['type'], 0) + 1

    print(f'\n  Domains ({len(domains)}):')
    for d in sorted(domains.keys()):
        print(f'    {d}: {domains[d]}')

    print(f'\n  Types ({len(types)}):')
    for t in sorted(types.keys(), key=lambda x: -types[x]):
        print(f'    {t}: {types[t]}')

    # Text length stats
    lengths = [len(p['text'].split()) for p in principles]
    print(f'\n  Text length (words): min={min(lengths)}, max={max(lengths)}, '
          f'mean={sum(lengths)/len(lengths):.1f}')

    # Check for empty texts
    empty = [p['id'] for p in principles if not p['text'].strip()]
    if empty:
        print(f'\n  WARNING: {len(empty)} principles with empty text')

    # Save
    out_path = os.path.join(os.path.dirname(__file__), 'parsed_principles.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(principles, f, indent=2, ensure_ascii=False)
    print(f'\n  Saved to {out_path}')

    # Show examples
    print('\n  Examples:')
    for p in principles[:3]:
        print(f'    {p["id"]}: "{p["text"][:80]}..."')


if __name__ == '__main__':
    main()
