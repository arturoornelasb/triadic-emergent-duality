"""Evaluate perplexity: base GPT-2 Medium vs all training runs.

Computes language model perplexity on a fixed evaluation corpus for:
  1. Base GPT-2 Medium (no fine-tuning)
  2. Each training run checkpoint (v1, v2, v3, v4)

Perplexity = exp(mean cross-entropy loss) on held-out text.
Lower = better language modeling. If fine-tuning degraded the LM,
perplexity will be higher than baseline.

Usage:
    python eval_perplexity.py
    python eval_perplexity.py --runs v3 v4        # only specific runs
    python eval_perplexity.py --stride 256        # faster, less precise
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json
import math
import argparse
import torch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.normpath(os.path.join(
    SCRIPT_DIR, '..', 'internal', 'results'))
CKPT_DIR = os.path.join(SCRIPT_DIR, 'checkpoints')

# All known runs: (display_name, checkpoint_dir_name, n_bits)
KNOWN_RUNS = [
    ('v1', 'gpt2_triadic_65', 65),
    ('v2', 'gpt2_triadic_65_v2', 65),
    ('v3', 'gpt2_triadic_65_v3', 65),
    ('v4', 'gpt2_triadic_72_v4', 72),
    ('v5_frozen', 'gpt2_triadic_72_v5_frozen', 72),
    ('v6', 'gpt2_triadic_72_v6', 72),
]


# ######################################################################
#  EVALUATION CORPUS
# ######################################################################

# Fixed, diverse evaluation text (~2500 tokens).
# Mix of science, philosophy, narrative, and technical prose.
# NOT in training data (GPT-2 was trained on WebText up to 2019).

EVAL_TEXTS = [
    # Science (post-2019 style)
    """The discovery of high-temperature superconductors at ambient pressure
would transform energy infrastructure fundamentally. Current transmission
lines lose approximately five percent of electricity to resistance, a
staggering waste at continental scale. Superconducting cables carrying
current without loss would reshape the economics of renewable energy,
making it practical to transmit solar power from deserts to distant cities.
The physics of Cooper pair formation in these materials remains poorly
understood, though recent advances in computational chemistry using density
functional theory have narrowed the search space considerably.""",

    # Philosophy
    """The hard problem of consciousness resists reduction to neural correlates.
When we observe a red apple, photons of specific wavelengths trigger cone
cells in the retina, generating electrical signals that propagate through
the lateral geniculate nucleus to the visual cortex. This causal chain is
well understood. What remains mysterious is why this physical process gives
rise to the subjective experience of redness — the quale that no amount of
third-person description seems to capture. Functionalist accounts argue
that consciousness is what the brain does, not what it is made of, but
this sidesteps rather than solves the explanatory gap.""",

    # Narrative
    """The old lighthouse keeper climbed the spiral staircase for the last time,
each step echoing against stone walls worn smooth by a century of footfalls.
At the top, the Fresnel lens caught the evening light and scattered it into
prismatic arcs across the curved glass. He had tended this light for thirty
years, through storms that bent the iron railing and fog so thick it
swallowed the beam within a hundred meters. Tomorrow the automated system
would take over, its LED array and GPS synchronization replacing the
careful ritual of cleaning, aligning, and igniting that had given his
nights their rhythm and purpose.""",

    # Technical / mathematical
    """In category theory, a natural transformation between two functors
provides a systematic way to transform one construction into another while
respecting the structure of all objects involved. Given functors F and G
from category C to category D, a natural transformation alpha assigns to
each object X in C a morphism alpha_X from F(X) to G(X) such that for
every morphism f from X to Y in C, the diagram commutes. This coherence
condition ensures that the transformation is not merely a collection of
unrelated maps but a genuinely structural relationship between the two
ways of viewing C inside D.""",

    # Biology / systems
    """Cellular autophagy serves as both housekeeping mechanism and survival
strategy. Under normal conditions, cells continuously degrade and recycle
damaged organelles and misfolded proteins through lysosomal pathways. When
nutrients become scarce, autophagy intensifies dramatically, breaking down
non-essential components to provide amino acids and energy for critical
functions. This self-eating process, far from being destructive, enables
cellular resilience. Defects in autophagy have been linked to
neurodegeneration, cancer, and accelerated aging, suggesting that the
ability to dismantle and rebuild oneself is fundamental to biological
persistence.""",
]


# ######################################################################
#  PERPLEXITY COMPUTATION
# ######################################################################

def compute_perplexity(model, tokenizer, texts, stride=512, max_length=1024,
                       device='cpu'):
    """Compute perplexity using sliding window over texts.

    Uses the standard approach: split text into overlapping windows,
    compute cross-entropy loss on each, average, exponentiate.
    """
    model.eval()

    total_loss = 0.0
    total_tokens = 0

    for text in texts:
        encodings = tokenizer(text, return_tensors='pt')
        input_ids = encodings['input_ids'][0]
        seq_len = input_ids.size(0)

        # Sliding window
        prev_end = 0
        for begin in range(0, seq_len, stride):
            end = min(begin + max_length, seq_len)
            input_chunk = input_ids[begin:end].unsqueeze(0).to(device)

            target_len = end - prev_end  # Only count new tokens
            target_chunk = input_chunk.clone()

            # Mask already-seen tokens (overlap region)
            if begin > 0:
                target_chunk[0, :begin - prev_end + (end - begin - target_len)] = -100

            with torch.no_grad():
                # Handle both GPT2Triadic (returns tuple) and plain GPT2LMHeadModel
                result = model(input_chunk, labels=target_chunk)
                if isinstance(result, tuple):
                    outputs = result[0]  # GPT2Triadic returns (outputs, triadic)
                else:
                    outputs = result

                # Cross-entropy loss (averaged over non-masked tokens)
                loss = outputs.loss

            # Count valid tokens
            valid = (target_chunk != -100).sum().item()
            total_loss += loss.item() * valid
            total_tokens += valid

            prev_end = end
            if end >= seq_len:
                break

    avg_loss = total_loss / total_tokens if total_tokens > 0 else 0
    perplexity = math.exp(avg_loss) if avg_loss < 100 else float('inf')

    return {
        'perplexity': round(perplexity, 2),
        'avg_loss': round(avg_loss, 4),
        'total_tokens': total_tokens,
    }


# ######################################################################
#  MODEL LOADING
# ######################################################################

def load_baseline(device='cpu'):
    """Load base GPT-2 Medium (no fine-tuning)."""
    from transformers import GPT2LMHeadModel, GPT2Tokenizer

    print('  Loading base GPT-2 Medium...')
    model = GPT2LMHeadModel.from_pretrained('gpt2-medium')
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')
    model.to(device)
    model.eval()
    return model, tokenizer


def load_checkpoint(ckpt_path, device='cpu'):
    """Load a fine-tuned GPT2Triadic checkpoint."""
    from gpt2_triadic import GPT2Triadic
    from transformers import GPT2Tokenizer

    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    cfg = ckpt.get('config', {})

    model = GPT2Triadic(
        model_name=cfg.get('model_name', 'gpt2-medium'),
        n_triadic_bits=cfg.get('n_triadic_bits', 65),
        freeze_base=cfg.get('freeze_base', False),
        head_mode=cfg.get('head_mode', 'simple'),
        activation=cfg.get('activation', 'ifsq'),
    )
    # strict=False: older runs may have different triadic head names
    # (e.g. v1 uses triadic_proj instead of triadic_head).
    # We only need GPT-2 LM weights for perplexity — triadic head is irrelevant.
    model.load_state_dict(ckpt['model_state_dict'], strict=False)
    model.to(device)
    model.eval()

    tokenizer = GPT2Tokenizer.from_pretrained(
        cfg.get('model_name', 'gpt2-medium'))

    info = {
        'step': ckpt.get('step', 0),
        'bit_accuracy': ckpt.get('bit_accuracy_test', 0),
        'n_bits': cfg.get('n_triadic_bits', 65),
        'head_mode': cfg.get('head_mode', 'simple'),
        'activation': cfg.get('activation', 'ifsq'),
        'alpha': cfg.get('alpha', 0),
    }

    return model, tokenizer, info


# ######################################################################
#  MAIN
# ######################################################################

def main():
    parser = argparse.ArgumentParser(description='Evaluate perplexity')
    parser.add_argument('--runs', nargs='*', default=None,
                        help='Specific runs to evaluate (e.g. v3 v4)')
    parser.add_argument('--stride', type=int, default=512,
                        help='Sliding window stride (default: 512, lower=slower but more precise)')
    parser.add_argument('--device', default=None,
                        help='Device (default: auto-detect cuda/cpu)')
    parser.add_argument('--skip-baseline', action='store_true',
                        help='Skip base GPT-2 evaluation')
    args = parser.parse_args()

    device = args.device
    if device is None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'

    os.makedirs(RESULTS_DIR, exist_ok=True)

    print('=' * 70)
    print('  PERPLEXITY EVALUATION')
    print('  Base GPT-2 Medium vs Fine-tuned Runs')
    print('=' * 70)
    print()
    print('  Device:  %s' % device)
    print('  Stride:  %d' % args.stride)
    print('  Corpus:  %d passages, ~%d chars' % (
        len(EVAL_TEXTS), sum(len(t) for t in EVAL_TEXTS)))

    results = {}

    # ---- Baseline ----
    if not args.skip_baseline:
        print()
        print('=' * 70)
        print('  BASELINE: GPT-2 Medium (no fine-tuning)')
        print('=' * 70)
        model, tokenizer = load_baseline(device)
        baseline = compute_perplexity(model, tokenizer, EVAL_TEXTS,
                                      stride=args.stride, device=device)
        results['baseline'] = {
            'model': 'gpt2-medium',
            'perplexity': baseline['perplexity'],
            'avg_loss': baseline['avg_loss'],
            'total_tokens': baseline['total_tokens'],
        }
        print('  Perplexity: %.2f' % baseline['perplexity'])
        print('  Avg loss:   %.4f' % baseline['avg_loss'])
        print('  Tokens:     %d' % baseline['total_tokens'])
        del model
        if device == 'cuda':
            torch.cuda.empty_cache()

    # ---- Fine-tuned runs ----
    runs_to_eval = KNOWN_RUNS
    if args.runs:
        runs_to_eval = [(n, d, b) for n, d, b in KNOWN_RUNS if n in args.runs]

    for run_name, ckpt_dir, n_bits in runs_to_eval:
        best_path = os.path.join(CKPT_DIR, ckpt_dir, 'best.pt')
        if not os.path.exists(best_path):
            print()
            print('  SKIP: %s — best.pt not found at %s' % (run_name, best_path))
            continue

        print()
        print('=' * 70)
        print('  RUN: %s (%s, %d bits)' % (run_name, ckpt_dir, n_bits))
        print('=' * 70)

        model, tokenizer, info = load_checkpoint(best_path, device)
        print('  Loaded: step=%s  bit_acc=%.4f  alpha=%s  head=%s  act=%s' % (
            info['step'], info['bit_accuracy'], info['alpha'],
            info['head_mode'], info['activation']))

        run_result = compute_perplexity(model, tokenizer, EVAL_TEXTS,
                                        stride=args.stride, device=device)

        # Compute delta vs baseline
        delta_pct = None
        if 'baseline' in results:
            base_ppl = results['baseline']['perplexity']
            delta_pct = ((run_result['perplexity'] - base_ppl) / base_ppl) * 100

        results[run_name] = {
            'checkpoint': ckpt_dir,
            'n_bits': n_bits,
            'step': info['step'],
            'bit_accuracy': info['bit_accuracy'],
            'alpha': info['alpha'],
            'perplexity': run_result['perplexity'],
            'avg_loss': run_result['avg_loss'],
            'total_tokens': run_result['total_tokens'],
            'delta_vs_baseline_pct': round(delta_pct, 2) if delta_pct is not None else None,
        }

        print('  Perplexity: %.2f' % run_result['perplexity'])
        print('  Avg loss:   %.4f' % run_result['avg_loss'])
        if delta_pct is not None:
            status = 'OK' if abs(delta_pct) < 15 else ('WARNING' if abs(delta_pct) < 30 else 'DEGRADED')
            print('  vs baseline: %+.1f%%  %s' % (delta_pct, status))

        del model
        if device == 'cuda':
            torch.cuda.empty_cache()

    # ---- Summary table ----
    print()
    print('=' * 70)
    print('  SUMMARY')
    print('=' * 70)
    print()
    print('  %-12s %8s %8s %10s %10s %8s' % (
        'Run', 'Bits', 'PPL', 'Avg Loss', 'Delta %', 'Status'))
    print('  ' + '-' * 60)

    if 'baseline' in results:
        r = results['baseline']
        print('  %-12s %8s %8.2f %10.4f %10s %8s' % (
            'baseline', '-', r['perplexity'], r['avg_loss'], '-', 'REF'))

    for run_name, _, _ in runs_to_eval:
        if run_name not in results:
            continue
        r = results[run_name]
        delta = r.get('delta_vs_baseline_pct')
        delta_str = '%+.1f%%' % delta if delta is not None else '-'
        if delta is not None:
            status = 'OK' if abs(delta) < 15 else ('WARN' if abs(delta) < 30 else 'BAD')
        else:
            status = '-'
        print('  %-12s %8d %8.2f %10.4f %10s %8s' % (
            run_name, r['n_bits'], r['perplexity'], r['avg_loss'],
            delta_str, status))

    print()

    # Health assessment
    if 'baseline' in results:
        base_ppl = results['baseline']['perplexity']
        all_deltas = [
            r.get('delta_vs_baseline_pct', 0)
            for name, r in results.items()
            if name != 'baseline' and r.get('delta_vs_baseline_pct') is not None
        ]
        if all_deltas:
            max_delta = max(abs(d) for d in all_deltas)
            if max_delta < 10:
                print('  VERDICT: Language model intact — fine-tuning had minimal impact on perplexity.')
            elif max_delta < 20:
                print('  VERDICT: Minor degradation — alpha=0.05 is working but some LM capacity was traded.')
            elif max_delta < 30:
                print('  VERDICT: Moderate degradation — consider reducing alpha or using freeze_base=True.')
            else:
                print('  VERDICT: Significant degradation — the triadic loss is hurting language modeling.')

    # ---- Save results ----
    out_path = os.path.join(RESULTS_DIR, 'perplexity_eval.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print()
    print('  Results saved: %s' % out_path)
    print('=' * 70)


if __name__ == '__main__':
    main()
