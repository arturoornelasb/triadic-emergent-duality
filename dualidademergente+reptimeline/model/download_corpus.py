"""
Download multi-domain corpus for training.

Downloads wikitext-103 or Wikipedia articles filtered by the 8 domains
of the 7x7 System: Physics, Chemistry, Biology, Mathematics, Philosophy,
Linguistics, Psychology, Music.

Usage:
    python download_corpus.py                     # wikitext-103 (default)
    python download_corpus.py --source wikipedia  # Wikipedia by category
    python download_corpus.py --output corpus/    # Custom output dir

Requires: datasets (pip install datasets)
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import time
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Wikipedia category keywords per domain
DOMAIN_KEYWORDS = {
    'Physics': [
        'physics', 'quantum', 'thermodynamics', 'electromagnetism', 'relativity',
        'mechanics', 'optics', 'nuclear', 'particle physics', 'gravity',
        'energy', 'force', 'momentum', 'wave', 'entropy', 'conservation law',
    ],
    'Chemistry': [
        'chemistry', 'chemical', 'molecule', 'reaction', 'element', 'compound',
        'acid', 'organic chemistry', 'inorganic', 'polymer', 'catalysis',
        'electrochemistry', 'biochemistry', 'periodic table',
    ],
    'Biology': [
        'biology', 'cell', 'DNA', 'evolution', 'ecology', 'genetics',
        'organism', 'species', 'anatomy', 'physiology', 'microbiology',
        'botany', 'zoology', 'neuroscience', 'immunology', 'taxonomy',
    ],
    'Mathematics': [
        'mathematics', 'algebra', 'geometry', 'calculus', 'topology',
        'number theory', 'statistics', 'probability', 'theorem', 'proof',
        'set theory', 'logic', 'combinatorics', 'analysis',
    ],
    'Philosophy': [
        'philosophy', 'ethics', 'metaphysics', 'epistemology', 'logic',
        'aesthetics', 'existentialism', 'phenomenology', 'ontology',
        'consciousness', 'free will', 'morality', 'justice',
    ],
    'Linguistics': [
        'linguistics', 'language', 'grammar', 'syntax', 'phonology',
        'semantics', 'pragmatics', 'morphology', 'sociolinguistics',
        'psycholinguistics', 'etymology', 'writing system',
    ],
    'Psychology': [
        'psychology', 'cognition', 'behavior', 'perception', 'memory',
        'emotion', 'personality', 'neuroscience', 'clinical psychology',
        'developmental psychology', 'social psychology',
    ],
    'Music': [
        'music', 'musical', 'harmony', 'melody', 'rhythm', 'composition',
        'symphony', 'opera', 'jazz', 'classical music', 'music theory',
        'instrument', 'sonata', 'fugue', 'counterpoint',
    ],
}


def download_wikitext(output_dir, max_docs=None):
    """Download wikitext-103 dataset."""
    from datasets import load_dataset

    print('Downloading wikitext-103...')
    ds = load_dataset('wikitext', 'wikitext-103-raw-v1', split='train')

    texts = [t for t in ds['text'] if len(t.strip()) > 100]
    print(f'  Total documents: {len(texts):,}')

    if max_docs and len(texts) > max_docs:
        import random
        random.seed(42)
        random.shuffle(texts)
        texts = texts[:max_docs]
        print(f'  Sampled: {max_docs:,}')

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, 'wikitext103.txt')
    with open(out_path, 'w', encoding='utf-8') as f:
        for text in texts:
            f.write(text.strip() + '\n\n')

    total_chars = sum(len(t) for t in texts)
    print(f'  Saved: {out_path} ({total_chars:,} chars)')
    return out_path


def download_wikipedia_filtered(output_dir, max_per_domain=2000):
    """Download Wikipedia articles filtered by domain keywords."""
    from datasets import load_dataset

    print('Downloading Wikipedia (this may take a while)...')
    ds = load_dataset('wikipedia', '20220301.en', split='train', streaming=True)

    os.makedirs(output_dir, exist_ok=True)
    domain_counts = {d: 0 for d in DOMAIN_KEYWORDS}
    domain_files = {}
    for d in DOMAIN_KEYWORDS:
        fpath = os.path.join(output_dir, f'{d.lower()}.txt')
        domain_files[d] = open(fpath, 'w', encoding='utf-8')

    total = 0
    matched = 0
    t0 = time.time()

    for article in ds:
        title = article['title'].lower()
        text = article['text']
        total += 1

        if len(text) < 200:
            continue

        for domain, keywords in DOMAIN_KEYWORDS.items():
            if domain_counts[domain] >= max_per_domain:
                continue
            if any(kw.lower() in title for kw in keywords):
                domain_files[domain].write(text.strip() + '\n\n<|endoftext|>\n\n')
                domain_counts[domain] += 1
                matched += 1
                break

        if total % 100000 == 0:
            elapsed = time.time() - t0
            print(f'  Scanned {total:,} articles ({matched} matched, {elapsed:.0f}s)')
            print(f'    Per domain: {dict(domain_counts)}')

        if all(c >= max_per_domain for c in domain_counts.values()):
            break

    for f in domain_files.values():
        f.close()

    print()
    print(f'  Total scanned: {total:,}')
    print(f'  Total matched: {matched:,}')
    for d, c in sorted(domain_counts.items()):
        print(f'    {d:<16} {c:>6}')

    # Also create a combined file
    combined_path = os.path.join(output_dir, 'combined.txt')
    with open(combined_path, 'w', encoding='utf-8') as out:
        for d in sorted(DOMAIN_KEYWORDS.keys()):
            fpath = os.path.join(output_dir, f'{d.lower()}.txt')
            with open(fpath, 'r', encoding='utf-8') as inp:
                out.write(inp.read())

    print(f'  Combined: {combined_path}')
    return combined_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download multi-domain corpus')
    parser.add_argument('--source', default='wikitext',
                        choices=['wikitext', 'wikipedia'],
                        help='Corpus source (default: wikitext)')
    parser.add_argument('--output', default=os.path.join(SCRIPT_DIR, 'corpus'),
                        help='Output directory')
    parser.add_argument('--max-docs', type=int, default=100000,
                        help='Max documents for wikitext')
    parser.add_argument('--max-per-domain', type=int, default=2000,
                        help='Max articles per domain for wikipedia')
    args = parser.parse_args()

    if args.source == 'wikitext':
        download_wikitext(args.output, args.max_docs)
    else:
        download_wikipedia_filtered(args.output, args.max_per_domain)
