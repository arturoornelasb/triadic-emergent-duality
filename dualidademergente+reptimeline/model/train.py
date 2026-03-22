"""
Training loop: GPT-2 + Triadic Head for 65 primitivos.

Loads a pre-trained GPT-2, adds a triadic projection head, and trains
on multi-domain text with triadic losses + gold prime distillation.

Adapted from triadic-microgpt/src/torch_train.py for this repo.

Usage:
    python train.py                                  # Default: gpt2-medium, fine-tune all
    python train.py --model gpt2 --freeze-base       # GPT-2 small, frozen base
    python train.py --model gpt2-medium --steps 20000
    python train.py --corpus path/to/corpus.txt      # Custom corpus

Requires: torch, transformers, datasets (all pre-installed).
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import csv
import time
import json
import math
import argparse

import torch
from torch.utils.data import Dataset, DataLoader
from transformers import GPT2Tokenizer

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from gpt2_triadic import GPT2Triadic
from triadic import PrimeMapper, BitwiseMapper


# ######################################################################
#  SECTION 0: DATASET
# ######################################################################

class TextDataset(Dataset):
    """Chunked text dataset for LM training."""

    def __init__(self, tokens, block_size):
        self.tokens = tokens
        self.block_size = block_size

    def __len__(self):
        return max(0, len(self.tokens) - self.block_size - 1)

    def __getitem__(self, idx):
        chunk = self.tokens[idx:idx + self.block_size + 1]
        x = torch.tensor(chunk[:-1], dtype=torch.long)
        y = torch.tensor(chunk[1:], dtype=torch.long)
        return x, y


# ######################################################################
#  SECTION 1: CORPUS LOADING
# ######################################################################

def load_corpus(args, tokenizer):
    """Load and tokenize a multi-domain corpus."""
    print('[1/4] Loading corpus...')

    if args.corpus and os.path.exists(args.corpus):
        # Custom corpus file
        print(f'  Source: {args.corpus}')
        with open(args.corpus, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        texts = [text]

    elif args.corpus_dir and os.path.isdir(args.corpus_dir):
        # Directory of text files
        print(f'  Source: {args.corpus_dir}/')
        texts = []
        for fname in sorted(os.listdir(args.corpus_dir)):
            if fname.endswith('.txt'):
                fpath = os.path.join(args.corpus_dir, fname)
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    texts.append(f.read())
                print(f'    {fname}: {len(texts[-1]):,} chars')

    else:
        # Default: download wikitext-103 via HuggingFace datasets
        print('  Source: wikitext-103 (HuggingFace datasets)')
        try:
            from datasets import load_dataset
            ds = load_dataset('wikitext', 'wikitext-103-raw-v1', split='train')
            texts = [t for t in ds['text'] if len(t.strip()) > 50]
            if args.max_docs and len(texts) > args.max_docs:
                import random
                random.seed(42)
                random.shuffle(texts)
                texts = texts[:args.max_docs]
            print(f'  Documents: {len(texts):,}')
        except Exception as e:
            print(f'  ERROR: Could not load wikitext. {e}')
            print('  Provide --corpus <file> or --corpus-dir <dir>')
            sys.exit(1)

    # Tokenize
    print('  Tokenizing...')
    t0 = time.time()
    all_tokens = []
    total_chars = 0
    for i, text in enumerate(texts):
        total_chars += len(text)
        ids = tokenizer.encode(text)
        all_tokens.extend(ids)
        if (i + 1) % 10000 == 0:
            print(f'    {i+1}/{len(texts)} docs ({len(all_tokens):,} tokens)')

    tok_time = time.time() - t0
    print(f'  Total: {len(all_tokens):,} tokens ({total_chars:,} chars, {tok_time:.1f}s)')
    if len(all_tokens) > 0:
        print(f'  Compression: {total_chars / len(all_tokens):.1f} chars/token')

    return all_tokens


# ######################################################################
#  SECTION 2: GOLD PRIMES LOADING
# ######################################################################

def load_gold_primes(tokenizer, n_bits):
    """Load gold primes for distillation."""
    gold_path = os.path.join(SCRIPT_DIR, 'gold_primes_65.json')
    if not os.path.exists(gold_path):
        print('  No gold_primes_65.json found. Run anchors.py first.')
        return []

    with open(gold_path, 'r', encoding='utf-8') as f:
        gold_data = json.load(f)

    sequences = []
    for concept, data in gold_data.items():
        sig = data['binary_signature'][:n_bits]
        # Pad if needed
        while len(sig) < n_bits:
            sig.append(0)

        # Tokenize concept (with and without leading space)
        for prefix in [' ', '']:
            ids = tokenizer.encode(prefix + concept.replace('_', ' '))
            sequences.append((ids, sig))

    print(f'  Gold primes: {len(sequences)} token sequences from {len(gold_data)} concepts')
    return sequences


# ######################################################################
#  SECTION 3: TRAINING LOOP
# ######################################################################

def train(args):
    """Main training function."""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    print()
    print('=' * 70)
    print('  GPT-2 TRIADIC — Training for 65 primitivos')
    print('=' * 70)
    print(f'  Device: {device}')
    if device.type == 'cuda':
        print(f'  GPU: {torch.cuda.get_device_name(0)}')
        mem_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f'  VRAM: {mem_gb:.1f} GB')
    print(f'  Model: {args.model}')
    print(f'  Freeze base: {args.freeze_base}')
    print()

    # --- Tokenizer ---
    print('[0/4] Loading tokenizer...')
    tokenizer = GPT2Tokenizer.from_pretrained(args.model)
    tokenizer.pad_token = tokenizer.eos_token
    print(f'  Vocab: {tokenizer.vocab_size}')

    # --- Corpus ---
    all_tokens = load_corpus(args, tokenizer)

    if len(all_tokens) < args.block * 2:
        print('ERROR: Corpus too small for training.')
        sys.exit(1)

    # --- Model ---
    print()
    print(f'[2/4] Initializing model: {args.model} + triadic head ({args.bits} bits)...')
    model = GPT2Triadic(
        model_name=args.model,
        n_triadic_bits=args.bits,
        freeze_base=args.freeze_base,
        dropout=args.dropout,
    ).to(device)

    trainable = model.num_params()
    total = model.num_params_total()
    print(f'  Total params: {total:,}')
    print(f'  Trainable:    {trainable:,} ({trainable/total*100:.1f}%)')

    # Gradient checkpointing for large models
    if args.grad_checkpoint:
        model.gpt2.gradient_checkpointing_enable()
        print('  Gradient checkpointing: ON')

    # --- Gold primes ---
    print()
    print('[3/4] Loading gold primes...')
    gold_sequences = []
    if not args.no_distill:
        gold_sequences = load_gold_primes(tokenizer, args.bits)

    # --- DataLoader ---
    dataset = TextDataset(all_tokens, args.block)
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True,
                            drop_last=True, num_workers=0)

    # --- Optimizer ---
    optimizer = torch.optim.AdamW(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=args.lr, weight_decay=0.01, betas=(0.9, 0.95)
    )

    # --- Mixed precision ---
    amp_dtype = {'float32': torch.float32, 'float16': torch.float16,
                 'bfloat16': torch.bfloat16}[args.dtype]
    use_amp = device.type == 'cuda' and amp_dtype != torch.float32
    use_scaler = use_amp and amp_dtype == torch.float16
    scaler = torch.amp.GradScaler('cuda', enabled=use_scaler)

    triadic_warmup = int(args.steps * args.triadic_warmup_pct)

    # --- Checkpoint dir ---
    ckpt_dir = os.path.join(SCRIPT_DIR, 'checkpoints', args.run_name)
    os.makedirs(ckpt_dir, exist_ok=True)

    # --- CSV logging ---
    csv_path = os.path.join(ckpt_dir, 'training_log.csv')
    csv_file = open(csv_path, 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['step', 'lang_loss', 'tri_loss', 'dist_loss', 'lr', 'elapsed_s'])

    # --- Training ---
    print()
    print(f'[4/4] Training for {args.steps} steps...')
    print(f'  Batch size: {args.batch_size}')
    print(f'  Block size: {args.block}')
    print(f'  Triadic warmup: step {triadic_warmup}')
    print(f'  Alpha: {args.alpha}')
    print(f'  Align weight: {args.align_weight}')
    print(f'  Entropy weight: {args.entropy_weight}')
    print(f'  Distillation: {"ON" if gold_sequences else "OFF"}')
    print(f'  Mixed precision: {args.dtype}')
    print('-' * 70)

    model.train()
    start_time = time.time()
    step = 0
    best_loss = float('inf')
    data_iter = iter(dataloader)

    while step < args.steps:
        # Get batch
        try:
            x, y = next(data_iter)
        except StopIteration:
            data_iter = iter(dataloader)
            x, y = next(data_iter)

        x, y = x.to(device), y.to(device)
        B, T = x.shape

        # Cosine LR with warmup
        warmup_steps = min(500, args.steps // 10)
        if step < warmup_steps:
            lr_t = args.lr * (step + 1) / warmup_steps
        else:
            progress = (step - warmup_steps) / max(args.steps - warmup_steps, 1)
            lr_t = args.lr * max(0.1, 0.5 * (1.0 + math.cos(math.pi * progress)))
        for pg in optimizer.param_groups:
            pg['lr'] = lr_t

        # Forward
        with torch.amp.autocast('cuda', dtype=amp_dtype, enabled=use_amp):
            outputs, triadic_proj = model(x, labels=y)
            lang_loss = outputs.loss

            total_loss = lang_loss
            tri_loss_val = 0.0
            dist_loss_val = 0.0

            if step >= triadic_warmup:
                alpha_warmup_steps = int(args.steps * 0.2)
                alpha_factor = min(1.0, (step - triadic_warmup + 1) / alpha_warmup_steps)
                current_alpha = args.alpha * alpha_factor

                tri_loss = model.triadic_loss(
                    triadic_proj,
                    entropy_weight=args.entropy_weight,
                    input_ids=x,
                    align_weight=args.align_weight,
                    align_mode=args.align_mode,
                )
                total_loss = lang_loss + current_alpha * tri_loss
                tri_loss_val = tri_loss.item()

                # Distillation
                if gold_sequences:
                    b_mask = torch.zeros((B, T), dtype=torch.bool, device=device)
                    targets_proj = torch.zeros((B, T, args.bits), dtype=torch.float32, device=device)

                    x_list = x.tolist()
                    match_found = False

                    for b_idx in range(B):
                        seq = x_list[b_idx]
                        for target_ids, bits in gold_sequences:
                            n_tok = len(target_ids)
                            for i in range(T - n_tok + 1):
                                if seq[i:i+n_tok] == target_ids:
                                    b_mask[b_idx, i + n_tok - 1] = True
                                    targets_proj[b_idx, i + n_tok - 1] = torch.tensor(
                                        bits, dtype=torch.float32, device=device)
                                    match_found = True

                    if match_found:
                        dist_loss = model.distillation_loss(triadic_proj, targets_proj, b_mask)
                        dist_alpha = current_alpha * args.dist_weight
                        total_loss = total_loss + dist_alpha * dist_loss
                        dist_loss_val = dist_loss.item()

        # Backward
        optimizer.zero_grad(set_to_none=True)
        scaler.scale(total_loss).backward()
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(optimizer)
        scaler.update()

        # Log
        elapsed = time.time() - start_time
        csv_writer.writerow([step + 1, f'{lang_loss.item():.6f}', f'{tri_loss_val:.6f}',
                             f'{dist_loss_val:.6f}', f'{lr_t:.8f}', f'{elapsed:.1f}'])

        if step % args.print_every == 0 or step == args.steps - 1:
            sps = (step + 1) / elapsed if elapsed > 0 else 0
            remaining = (args.steps - step - 1) / sps if sps > 0 else 0
            pct = (step + 1) / args.steps * 100

            bar_len = 30
            filled = int(bar_len * (step + 1) / args.steps)
            bar = '#' * filled + '-' * (bar_len - filled)

            eta_str = f"{remaining/60:.1f}m" if remaining >= 60 else f"{remaining:.0f}s"

            msg = f'  [{bar}] {pct:5.1f}%'
            msg += f' | step {step+1}/{args.steps}'
            msg += f' | loss {lang_loss.item():.4f}'
            if step >= triadic_warmup:
                msg += f' | tri {tri_loss_val:.4f}'
                if gold_sequences:
                    msg += f' | dist {dist_loss_val:.4f}'
            msg += f' | {sps:.1f} stp/s | ETA {eta_str}'
            print(msg)

        # Checkpoint
        if (step + 1) % args.save_every == 0 or step == args.steps - 1:
            ckpt_path = os.path.join(ckpt_dir, f'step_{step+1}.pt')
            torch.save({
                'model_state_dict': model.state_dict(),
                'config': {
                    'model_name': args.model,
                    'n_triadic_bits': args.bits,
                    'freeze_base': args.freeze_base,
                },
                'step': step + 1,
                'loss': lang_loss.item(),
            }, ckpt_path)

            if lang_loss.item() < best_loss:
                best_loss = lang_loss.item()
                best_path = os.path.join(ckpt_dir, 'best.pt')
                torch.save({
                    'model_state_dict': model.state_dict(),
                    'config': {
                        'model_name': args.model,
                        'n_triadic_bits': args.bits,
                        'freeze_base': args.freeze_base,
                    },
                    'step': step + 1,
                    'loss': best_loss,
                }, best_path)

            print(f'  >>> Saved: {ckpt_path}')

        step += 1

    csv_file.close()

    # --- Final report ---
    elapsed = time.time() - start_time
    print()
    print('-' * 70)
    print(f'  Training complete!')
    print(f'  Time: {elapsed:.0f}s ({elapsed/60:.1f} min)')
    print(f'  Final loss: {lang_loss.item():.4f}')
    print(f'  Speed: {args.steps/elapsed:.1f} steps/s')
    print(f'  Checkpoints: {ckpt_dir}')
    print(f'  Training log: {csv_path}')
    print('=' * 70)


# ######################################################################
#  SECTION 4: ENTRY POINT
# ######################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train GPT-2 + Triadic Head')

    # Model
    parser.add_argument('--model', default='gpt2-medium',
                        choices=['gpt2', 'gpt2-medium', 'gpt2-large'],
                        help='Pre-trained GPT-2 variant (default: gpt2-medium)')
    parser.add_argument('--freeze-base', action='store_true',
                        help='Freeze GPT-2 weights, train only triadic head')
    parser.add_argument('--bits', type=int, default=65, help='Triadic bits (default: 65)')
    parser.add_argument('--dropout', type=float, default=0.1, help='Triadic head dropout')
    parser.add_argument('--grad-checkpoint', action='store_true',
                        help='Gradient checkpointing (saves VRAM)')

    # Data
    parser.add_argument('--corpus', type=str, default=None, help='Path to corpus .txt file')
    parser.add_argument('--corpus-dir', type=str, default=None, help='Directory of .txt files')
    parser.add_argument('--max-docs', type=int, default=100000, help='Max documents to load')
    parser.add_argument('--block', type=int, default=256, help='Context window size')

    # Training
    parser.add_argument('--steps', type=int, default=20000, help='Training steps')
    parser.add_argument('--batch-size', type=int, default=8, help='Batch size')
    parser.add_argument('--lr', type=float, default=1e-4, help='Learning rate')
    parser.add_argument('--alpha', type=float, default=0.05, help='Triadic loss weight')
    parser.add_argument('--entropy-weight', type=float, default=1.0, help='Entropy regularization')
    parser.add_argument('--align-weight', type=float, default=5.0, help='Embedding alignment weight')
    parser.add_argument('--align-mode', default='mse', choices=['mse', 'infonce'],
                        help='Alignment mode')
    parser.add_argument('--dist-weight', type=float, default=1.0, help='Distillation weight')
    parser.add_argument('--triadic-warmup-pct', type=float, default=0.25,
                        help='Fraction of steps before activating triadic loss')
    parser.add_argument('--no-distill', action='store_true', help='Skip gold prime distillation')

    # Output
    parser.add_argument('--run-name', default='gpt2_triadic_65', help='Run name for checkpoints')
    parser.add_argument('--print-every', type=int, default=50, help='Print frequency')
    parser.add_argument('--save-every', type=int, default=2000, help='Save frequency')
    parser.add_argument('--dtype', default='bfloat16',
                        choices=['float32', 'float16', 'bfloat16'],
                        help='Mixed precision (default: bfloat16)')

    args = parser.parse_args()
    train(args)
