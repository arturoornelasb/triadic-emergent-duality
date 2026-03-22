"""
Training loop: GPT-2 + Triadic Head for 65 primitivos (v3).

V3 changes from v2:
  - Trains directly with 65 primitivos (not 262 domain anchors)
  - Target = own bit ON + transitive deps ON (100% unique, 0 collisions)
  - Uses English word + definition for GPT-2 context (Option D)
  - Regla de tres quads use dual pairs from the circle

Blueprint from triadic-microgpt Run 15 + Danza D-A14:
  L_total = L_lang + alpha * (L_tri + sup_weight * L_sup + sub_weight * L_sub)

Features:
  - iFSQ activation (distributes activations, prevents dead bits)
  - Simple triadic head (single linear, like blueprint)
  - InfoNCE alignment (better for pre-trained GPT-2 embeddings)
  - Supervised anchor loss (L_sup) — direct MSE each step
  - Subsumption loss (L_sub) — enforces dependency hierarchy
  - Evaluation during training: anchor accuracy, subsumption, dead bits, entropy
  - Best model selection by test accuracy
  - Regla de tres (analogy) evaluation
  - Optimizer state in checkpoints for training resume
  - GPU optimizations: TF32, cuDNN benchmark, torch.compile

Usage:
    python train.py                                     # Default v2 settings
    python train.py --model gpt2-medium --steps 50000
    python train.py --resume checkpoints/gpt2_triadic_65_v2/step_25000.pt

Requires: torch, transformers, datasets (all pre-installed in triadic-microgpt conda env).
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import csv
import time
import json
import math
import random
import argparse

import shutil

import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from transformers import GPT2Tokenizer

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))
sys.path.insert(0, SCRIPT_DIR)

from gpt2_triadic import GPT2Triadic

# V3: word + definition needs more tokens than single-word anchors
MAX_CONCEPT_TOKENS = 20


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
    print('[1/6] Loading corpus...')

    if args.corpus and os.path.exists(args.corpus):
        print(f'  Source: {args.corpus}')
        with open(args.corpus, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        texts = [text]

    elif args.corpus_dir and os.path.isdir(args.corpus_dir):
        print(f'  Source: {args.corpus_dir}/')
        texts = []
        for fname in sorted(os.listdir(args.corpus_dir)):
            if fname.endswith('.txt'):
                fpath = os.path.join(args.corpus_dir, fname)
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    texts.append(f.read())
                print(f'    {fname}: {len(texts[-1]):,} chars')

    else:
        print('  Source: wikitext-103 (HuggingFace datasets)')
        try:
            from datasets import load_dataset
            ds = load_dataset('wikitext', 'wikitext-103-raw-v1', split='train')
            texts = [t for t in ds['text'] if len(t.strip()) > 50]
            if args.max_docs and len(texts) > args.max_docs:
                random.seed(42)
                random.shuffle(texts)
                texts = texts[:args.max_docs]
            print(f'  Documents: {len(texts):,}')
        except Exception as e:
            print(f'  ERROR: Could not load wikitext. {e}')
            sys.exit(1)

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
    return all_tokens


# ######################################################################
#  SECTION 2: ANCHOR & SUBSUMPTION LOADING
# ######################################################################

def load_anchors(tokenizer, n_bits, device, test_pct=0.2):
    """Load gold anchors, split train/test for evaluation.

    Returns: (train_t, train_tgt, train_words, test_t, test_tgt, test_words)
    """
    gold_path = os.path.join(SCRIPT_DIR, 'gold_primitivos_65.json')
    if not os.path.exists(gold_path):
        print('  No gold_primitivos_65.json found. Run generate_gold_primitivos.py first.')
        return None

    with open(gold_path, 'r', encoding='utf-8') as f:
        gold_data = json.load(f)

    max_tok = MAX_CONCEPT_TOKENS
    all_items = []
    for concept, data in gold_data.items():
        sig = data['binary_signature'][:n_bits]
        while len(sig) < n_bits:
            sig.append(0)
        target = [2.0 * b - 1.0 for b in sig]
        text = data.get('text', concept.replace('_', ' '))
        ids = tokenizer.encode(' ' + text)[:max_tok]
        while len(ids) < max_tok:
            ids.append(tokenizer.eos_token_id)
        all_items.append((concept, ids, target))

    random.seed(42)
    random.shuffle(all_items)
    n_test = max(1, int(len(all_items) * test_pct))

    test_items = all_items[:n_test]
    train_items = all_items[n_test:]

    def to_tensors(items):
        words = [it[0] for it in items]
        ids_t = torch.tensor([it[1] for it in items], dtype=torch.long, device=device)
        tgt_t = torch.tensor([it[2] for it in items], dtype=torch.float32, device=device)
        return ids_t, tgt_t, words

    train_t, train_tgt, train_words = to_tensors(train_items)
    test_t, test_tgt, test_words = to_tensors(test_items)

    print(f'  Primitivos: {len(train_items)} train, {len(test_items)} test, {n_bits} bits, {max_tok} max tokens')
    return (train_t, train_tgt, train_words, test_t, test_tgt, test_words, gold_data)


def build_subsumption_pairs(gold_data, tokenizer, device, test_pct=0.2):
    """Build hypernym-hyponym pairs, split train/test."""
    items = list(gold_data.items())
    max_tok = MAX_CONCEPT_TOKENS

    pairs = []
    for i, (w_a, d_a) in enumerate(items):
        bits_a = set(j for j, v in enumerate(d_a['binary_signature']) if v == 1)
        for j, (w_b, d_b) in enumerate(items):
            if i == j:
                continue
            bits_b = set(k for k, v in enumerate(d_b['binary_signature']) if v == 1)
            if bits_a and bits_a < bits_b:
                pairs.append((w_a, w_b))

    if not pairs:
        print('  Subsumption: 0 pairs found')
        return None

    random.seed(42)
    random.shuffle(pairs)
    n_test = max(1, int(len(pairs) * test_pct))

    def to_tensors(pair_list):
        h_ids, y_ids = [], []
        for hyper, hypo in pair_list:
            h_text = gold_data[hyper].get('text', hyper.replace('_', ' '))
            y_text = gold_data[hypo].get('text', hypo.replace('_', ' '))
            h = tokenizer.encode(' ' + h_text)[:max_tok]
            y = tokenizer.encode(' ' + y_text)[:max_tok]
            while len(h) < max_tok:
                h.append(tokenizer.eos_token_id)
            while len(y) < max_tok:
                y.append(tokenizer.eos_token_id)
            h_ids.append(h)
            y_ids.append(y)
        return (torch.tensor(h_ids, dtype=torch.long, device=device),
                torch.tensor(y_ids, dtype=torch.long, device=device))

    test_h, test_y = to_tensors(pairs[:n_test])
    train_h, train_y = to_tensors(pairs[n_test:])

    print(f'  Subsumption: {len(pairs)-n_test} train, {n_test} test pairs')
    return (train_h, train_y, test_h, test_y)


# ######################################################################
#  SECTION 3: LOSS FUNCTIONS
# ######################################################################

def supervised_anchor_loss(model, word_tensors, target_vectors, n_sample=32):
    """L_sup: MSE between model projections and gold anchor targets."""
    N = word_tensors.shape[0]
    if N == 0:
        return torch.tensor(0.0, device=word_tensors.device)
    if N > n_sample:
        idx = torch.randperm(N, device=word_tensors.device)[:n_sample]
        w_batch, t_batch = word_tensors[idx], target_vectors[idx]
    else:
        w_batch, t_batch = word_tensors, target_vectors

    _, triadic_proj = model(w_batch)
    pred = triadic_proj.mean(dim=1)
    return F.mse_loss(pred, t_batch)


def subsumption_loss(model, hyper_t, hypo_t, n_sample=32):
    """L_sub: relu(hypernym_01 - hyponym_01).mean()"""
    N = hyper_t.shape[0]
    if N == 0:
        return torch.tensor(0.0, device=hyper_t.device)
    if N > n_sample:
        idx = torch.randperm(N, device=hyper_t.device)[:n_sample]
        h_batch, y_batch = hyper_t[idx], hypo_t[idx]
    else:
        h_batch, y_batch = hyper_t, hypo_t

    _, h_proj = model(h_batch)
    _, y_proj = model(y_batch)
    h_01 = (h_proj.mean(dim=1) + 1) / 2
    y_01 = (y_proj.mean(dim=1) + 1) / 2
    return F.relu(h_01 - y_01).mean()


# ######################################################################
#  SECTION 4: EVALUATION
# ######################################################################

@torch.no_grad()
def evaluate_anchors(model, word_tensors, target_vectors, valid_words):
    """Per-anchor bit accuracy, dead bits, entropy."""
    model.eval()
    N = word_tensors.shape[0]
    if N == 0:
        model.train()
        return {}

    _, proj = model(word_tensors)
    pred = proj.mean(dim=1)

    pred_bits = (pred > 0).float()
    target_bits = (target_vectors > 0).float()
    per_concept_acc = (pred_bits == target_bits).float().mean(dim=1)
    mean_bit_acc = per_concept_acc.mean().item()

    results_per_word = []
    for i in range(N):
        results_per_word.append({
            'word': valid_words[i],
            'bit_accuracy': per_concept_acc[i].item(),
        })
    results_per_word.sort(key=lambda x: x['bit_accuracy'])

    # Dead bits & entropy
    all_pred = pred.cpu().numpy()
    bit_means = (all_pred > 0).mean(axis=0)
    eps = 1e-7
    ent = -(bit_means * np.log2(bit_means + eps) +
            (1 - bit_means) * np.log2(1 - bit_means + eps))
    dead_bits = int((ent < 0.3).sum())

    model.train()
    return {
        'mean_bit_accuracy': mean_bit_acc,
        'dead_bits': dead_bits,
        'mean_entropy': float(ent.mean()),
        'worst_5': results_per_word[:5],
        'best_5': results_per_word[-5:],
    }


@torch.no_grad()
def evaluate_subsumption(model, hyper_t, hypo_t):
    """Binary subsumption satisfaction rate."""
    model.eval()
    N = hyper_t.shape[0]
    if N == 0:
        model.train()
        return 0.0

    _, h_proj = model(hyper_t)
    _, y_proj = model(hypo_t)
    h_bits = (h_proj.mean(dim=1) > 0).float()
    y_bits = (y_proj.mean(dim=1) > 0).float()

    violations = (h_bits * (1 - y_bits)).sum(dim=1)
    satisfied = (violations == 0).float().sum().item()

    model.train()
    return satisfied / N


# Regla de tres analogy quads using dual pairs from the 65 primitivos
REGLA_DE_TRES_QUADS = [
    ('good', 'evil', 'truth', 'lie'),                                       # moral ~ epistemic
    ('creation', 'destruction', 'life', 'death'),                           # generative ~ vital
    ('freedom', 'control', 'individual', 'collective'),                     # autonomy ~ social
    ('pleasure', 'pain', 'conscious', 'absent'),                            # hedonic ~ awareness
    ('union', 'separation', 'order', 'chaos'),                              # connection ~ structure
    ('move', 'stillness', 'mortal_observer', 'eternal_observer'),           # kinetic ~ temporal
    ('receptive', 'creator_observer', 'truth', 'lie'),                      # passive/active ~ epistemic
    ('creation', 'destruction', 'union', 'separation'),                     # making ~ connecting
]


@torch.no_grad()
def evaluate_regla_de_tres(model, tokenizer, gold_data, device):
    """A:B = C:D analogy evaluation."""
    model.eval()
    results = []

    def get_proj(word):
        text = gold_data.get(word, {}).get('text', word.replace('_', ' '))
        ids = tokenizer.encode(' ' + text)[:MAX_CONCEPT_TOKENS]
        if not ids:
            return None
        while len(ids) < MAX_CONCEPT_TOKENS:
            ids.append(tokenizer.eos_token_id)
        x = torch.tensor([ids], dtype=torch.long, device=device)
        _, proj = model(x)
        return proj[0].mean(dim=0)

    for a_word, b_word, c_word, d_word in REGLA_DE_TRES_QUADS:
        if not all(w in gold_data for w in [a_word, b_word, c_word, d_word]):
            continue

        pa, pb, pc, pd = get_proj(a_word), get_proj(b_word), get_proj(c_word), get_proj(d_word)
        if any(p is None for p in [pa, pb, pc, pd]):
            continue

        predicted_d = pc + (pb - pa)
        cos = F.cosine_similarity(predicted_d.unsqueeze(0), pd.unsqueeze(0)).item()
        pred_bits = (predicted_d > 0).long()
        actual_bits = (pd > 0).long()
        bit_match = (pred_bits == actual_bits).float().mean().item()

        results.append({
            'quad': f'{a_word}:{b_word}={c_word}:{d_word}',
            'cosine': round(cos, 4),
            'bit_accuracy': round(bit_match, 4),
        })

    model.train()
    return results


# ######################################################################
#  SECTION 5: TRAINING LOOP
# ######################################################################

def train(args):
    """Main training function."""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # GPU optimizations
    if device.type == 'cuda':
        torch.set_float32_matmul_precision('high')
        torch.backends.cudnn.benchmark = True

    print()
    print('=' * 70)
    print('  GPT-2 TRIADIC v3 — Training with 65 primitivos directly')
    print('=' * 70)
    print(f'  Device: {device}')
    if device.type == 'cuda':
        print(f'  GPU: {torch.cuda.get_device_name(0)}')
        mem_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f'  VRAM: {mem_gb:.1f} GB')
        print(f'  TF32 matmul: ON | cuDNN benchmark: ON')
    print(f'  Model: {args.model}')
    print(f'  Head: {args.head_mode} | Activation: {args.activation}')
    print()

    # --- Tokenizer ---
    print('[0/6] Loading tokenizer...')
    tokenizer = GPT2Tokenizer.from_pretrained(args.model)
    tokenizer.pad_token = tokenizer.eos_token

    # --- Corpus ---
    all_tokens = load_corpus(args, tokenizer)
    if len(all_tokens) < args.block * 2:
        print('ERROR: Corpus too small.')
        sys.exit(1)

    # --- Model ---
    print()
    print(f'[2/6] Initializing model: {args.model} + triadic head ({args.bits} bits)...')
    model = GPT2Triadic(
        model_name=args.model,
        n_triadic_bits=args.bits,
        freeze_base=args.freeze_base,
        dropout=args.dropout,
        head_mode=args.head_mode,
        activation=args.activation,
    ).to(device)

    trainable = model.num_params()
    total_params = model.num_params_total()
    print(f'  Total params: {total_params:,}')
    print(f'  Trainable:    {trainable:,} ({trainable/total_params*100:.1f}%)')

    if args.grad_checkpoint:
        model.gpt2.gradient_checkpointing_enable()
        print('  Gradient checkpointing: ON')

    # torch.compile
    if device.type == 'cuda' and not args.no_compile:
        try:
            import triton  # noqa: F401
            model = torch.compile(model)
            print('  torch.compile: ON')
        except ImportError:
            print('  torch.compile: SKIPPED (triton not available)')

    # --- Anchors & Subsumption ---
    print()
    print('[3/6] Loading anchors & subsumption pairs...')
    anchor_data = None
    sub_data = None
    gold_data = None

    if not args.no_supervision:
        anchor_data = load_anchors(tokenizer, args.bits, device)
        if anchor_data:
            train_t, train_tgt, train_words, test_t, test_tgt, test_words, gold_data = anchor_data
            sub_data = build_subsumption_pairs(gold_data, tokenizer, device)
    else:
        print('  Supervision OFF (--no-supervision)')

    has_sup = anchor_data is not None
    has_sub = sub_data is not None

    # --- DataLoader ---
    print()
    print('[4/6] Preparing data...')
    dataset = TextDataset(all_tokens, args.block)
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True,
                            drop_last=True, num_workers=0)
    print(f'  Dataset: {len(dataset):,} chunks of {args.block} tokens')

    # --- Optimizer ---
    optimizer = torch.optim.AdamW(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=args.lr, weight_decay=0.01, betas=(0.9, 0.95)
    )

    # --- Resume ---
    start_step = 0
    if args.resume and os.path.exists(args.resume):
        print(f'\n[*] Resuming from {args.resume}...')
        ckpt = torch.load(args.resume, map_location=device, weights_only=False)
        model.load_state_dict(ckpt['model_state_dict'])
        if 'optimizer_state_dict' in ckpt:
            optimizer.load_state_dict(ckpt['optimizer_state_dict'])
        start_step = ckpt.get('step', 0)
        print(f'  Resumed at step {start_step}')

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

    # --- Save run configuration for reproducibility ---
    gold_file = 'gold_primitivos_65.json'
    gold_src = os.path.join(SCRIPT_DIR, gold_file)
    if start_step == 0:
        # Copy gold targets into checkpoint dir (frozen snapshot)
        if os.path.exists(gold_src):
            shutil.copy2(gold_src, os.path.join(ckpt_dir, gold_file))
            print(f'  Gold targets snapshot: {ckpt_dir}/{gold_file}')

        run_config = {
            'run_name': args.run_name,
            'date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'gold_file': gold_file,
            'n_concepts': len(gold_data) if gold_data else 0,
            'n_train': train_t.shape[0] if has_sup else 0,
            'n_test': test_t.shape[0] if has_sup else 0,
            'has_supervision': has_sup,
            'has_subsumption': has_sub,
            'args': {k: v for k, v in vars(args).items()},
        }
        config_path = os.path.join(ckpt_dir, 'run_config.json')
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(run_config, f, indent=2, ensure_ascii=False)
        print(f'  Run config: {config_path}')

    # --- CSV logging (full 12 columns like danza) ---
    csv_path = os.path.join(ckpt_dir, 'training_log.csv')
    if start_step > 0 and os.path.exists(csv_path):
        csv_file = open(csv_path, 'a', newline='')
    else:
        csv_file = open(csv_path, 'w', newline='')
    csv_writer = csv.writer(csv_file)
    if start_step == 0 or not os.path.exists(csv_path):
        csv_writer.writerow(['step', 'loss', 'lang_loss', 'tri_loss', 'sup_loss', 'sub_loss',
                             'bit_acc_train', 'bit_acc_test', 'sub_train', 'sub_test',
                             'dead_bits', 'entropy'])

    # --- Training ---
    print()
    print(f'[5/6] Training for {args.steps} steps (from step {start_step})...')
    eff_batch = args.batch_size * args.accum_steps
    print(f'  Batch: {args.batch_size} x {args.accum_steps} accum = {eff_batch} effective | Block: {args.block} | LR: {args.lr}')
    print(f'  Triadic warmup: step {triadic_warmup} ({args.triadic_warmup_pct*100:.0f}%)')
    print(f'  Alpha: {args.alpha} | Align: {args.align_mode}(w={args.align_weight})')
    print(f'  Supervision: L_sup(w={args.sup_weight}), L_sub(w={args.sub_weight})')
    print(f'  Eval every: {args.eval_every} steps')
    print(f'  Precision: {args.dtype}')
    print('-' * 70)

    model.train()
    start_time = time.time()
    step = start_step
    best_bit_acc = 0.0
    data_iter = iter(dataloader)
    optimizer.zero_grad(set_to_none=True)

    while step < args.steps:
        try:
            x, y = next(data_iter)
        except StopIteration:
            data_iter = iter(dataloader)
            x, y = next(data_iter)

        x, y = x.to(device), y.to(device)

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
            sup_loss_val = 0.0
            sub_loss_val = 0.0

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
                tri_loss_val = tri_loss.item()

                l_sup = torch.tensor(0.0, device=device)
                if has_sup:
                    l_sup = supervised_anchor_loss(model, train_t, train_tgt, n_sample=32)
                    sup_loss_val = l_sup.item()

                l_sub = torch.tensor(0.0, device=device)
                if has_sub:
                    l_sub = subsumption_loss(model, sub_data[0], sub_data[1], n_sample=32)
                    sub_loss_val = l_sub.item()

                total_loss = lang_loss + current_alpha * (
                    tri_loss + args.sup_weight * l_sup + args.sub_weight * l_sub)

            # Scale loss for gradient accumulation
            total_loss = total_loss / args.accum_steps

        # Backward (accumulate gradients)
        scaler.scale(total_loss).backward()

        # Optimizer step only every accum_steps
        accum_idx = (step - start_step) % args.accum_steps
        if accum_idx == args.accum_steps - 1:
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            scaler.step(optimizer)
            scaler.update()
            optimizer.zero_grad(set_to_none=True)

        # Print progress
        if step % args.print_every == 0 or step == args.steps - 1:
            elapsed = time.time() - start_time
            sps = (step - start_step + 1) / elapsed if elapsed > 0 else 0
            remaining = (args.steps - step - 1) / sps if sps > 0 else 0
            pct = (step + 1) / args.steps * 100
            bar_len = 30
            filled = int(bar_len * (step + 1) / args.steps)
            bar = '#' * filled + '-' * (bar_len - filled)
            eta_str = f"{remaining/60:.1f}m" if remaining >= 60 else f"{remaining:.0f}s"

            msg = f'  [{bar}] {pct:5.1f}% | step {step+1}/{args.steps} | loss {lang_loss.item():.4f}'
            if step >= triadic_warmup:
                msg += f' | tri {tri_loss_val:.3f} sup {sup_loss_val:.3f} sub {sub_loss_val:.3f}'
            msg += f' | {sps:.1f} stp/s | ETA {eta_str}'
            print(msg)

        # --- Evaluation ---
        if (step % args.eval_every == 0 and step > 0) or step == args.steps - 1:
            eval_train = {}
            eval_test = {}
            sub_rate_train = 0.0
            sub_rate_test = 0.0

            if has_sup:
                eval_train = evaluate_anchors(model, train_t, train_tgt, train_words)
                eval_test = evaluate_anchors(model, test_t, test_tgt, test_words)
            if has_sub:
                sub_rate_train = evaluate_subsumption(model, sub_data[0], sub_data[1])
                sub_rate_test = evaluate_subsumption(model, sub_data[2], sub_data[3])

            ba_train = eval_train.get('mean_bit_accuracy', 0)
            ba_test = eval_test.get('mean_bit_accuracy', 0)
            dead = eval_train.get('dead_bits', args.bits)
            ent = eval_train.get('mean_entropy', 0)

            print(f'  --- Eval @ step {step+1} ---')
            print(f'  Bit accuracy:  train={ba_train:.1%}  test={ba_test:.1%}')
            print(f'  Subsumption:   train={sub_rate_train:.1%}  test={sub_rate_test:.1%}')
            print(f'  Dead bits: {dead}/{args.bits}  Entropy: {ent:.3f}')

            if eval_test.get('worst_5'):
                ws = [f"{w['word']}({w['bit_accuracy']:.0%})" for w in eval_test['worst_5'][:3]]
                print(f'  Worst test: {", ".join(ws)}')
            if eval_test.get('best_5'):
                bs = [f"{w['word']}({w['bit_accuracy']:.0%})" for w in eval_test['best_5'][-3:]]
                print(f'  Best test:  {", ".join(bs)}')

            # Free VRAM after eval to prevent OOM spikes
            if device.type == 'cuda':
                torch.cuda.empty_cache()

            # CSV
            csv_writer.writerow([
                step + 1, total_loss.item(), lang_loss.item(),
                tri_loss_val, sup_loss_val, sub_loss_val,
                ba_train, ba_test, sub_rate_train, sub_rate_test,
                dead, ent,
            ])
            csv_file.flush()

            # Best model by test accuracy
            if ba_test > best_bit_acc:
                best_bit_acc = ba_test
                best_path = os.path.join(ckpt_dir, 'best.pt')
                torch.save({
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'config': {
                        'run_name': args.run_name,
                        'gold_file': gold_file,
                        'model_name': args.model,
                        'n_triadic_bits': args.bits,
                        'freeze_base': args.freeze_base,
                        'head_mode': args.head_mode,
                        'activation': args.activation,
                        'lr': args.lr,
                        'alpha': args.alpha,
                    },
                    'step': step + 1,
                    'bit_accuracy_test': ba_test,
                    'sub_rate_test': sub_rate_test,
                }, best_path)
                print(f'  ** New best: {ba_test:.1%} -> saved {best_path}')

        # Checkpoint
        if (step + 1) % args.save_every == 0:
            ckpt_path = os.path.join(ckpt_dir, f'step_{step+1}.pt')
            torch.save({
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'config': {
                    'run_name': args.run_name,
                    'gold_file': gold_file,
                    'model_name': args.model,
                    'n_triadic_bits': args.bits,
                    'freeze_base': args.freeze_base,
                    'head_mode': args.head_mode,
                    'activation': args.activation,
                    'lr': args.lr,
                    'alpha': args.alpha,
                },
                'step': step + 1,
                'loss': lang_loss.item(),
            }, ckpt_path)
            print(f'  >>> Saved: {ckpt_path}')

        step += 1

    csv_file.close()

    # --- Post-training: Regla de tres ---
    print()
    print('[6/6] Post-training evaluation...')
    if gold_data:
        r3_results = evaluate_regla_de_tres(model, tokenizer, gold_data, device)
        if r3_results:
            print('  Regla de tres (A:B = C:D):')
            for r in r3_results:
                print(f"    {r['quad']:<45} cos={r['cosine']:+.3f}  bits={r['bit_accuracy']:.1%}")
            mean_cos = sum(r['cosine'] for r in r3_results) / len(r3_results)
            mean_bits = sum(r['bit_accuracy'] for r in r3_results) / len(r3_results)
            print(f'  Mean: cosine={mean_cos:+.3f}  bit_accuracy={mean_bits:.1%}')

    # --- Final report ---
    elapsed = time.time() - start_time
    print()
    print('-' * 70)
    print(f'  Training complete!')
    print(f'  Time: {elapsed:.0f}s ({elapsed/60:.1f} min)')
    print(f'  Final loss: {lang_loss.item():.4f}')
    print(f'  Best test accuracy: {best_bit_acc:.1%}')
    print(f'  Speed: {(args.steps - start_step)/elapsed:.1f} steps/s')
    print(f'  Checkpoints: {ckpt_dir}')
    print('=' * 70)

    # Save final results JSON (complete metadata for archival)
    results_path = os.path.join(ckpt_dir, 'results.json')
    results = {
        'run_name': args.run_name,
        'date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'model': args.model,
        'bits': args.bits,
        'head_mode': args.head_mode,
        'activation': args.activation,
        'steps': args.steps,
        'lr': args.lr,
        'alpha': args.alpha,
        'batch_size': args.batch_size,
        'accum_steps': args.accum_steps,
        'effective_batch': args.batch_size * args.accum_steps,
        'gold_file': gold_file,
        'n_concepts': len(gold_data) if gold_data else 0,
        'best_bit_accuracy_test': best_bit_acc,
        'final_loss': lang_loss.item(),
        'elapsed_s': elapsed,
        'elapsed_h': round(elapsed / 3600, 2),
    }
    if gold_data:
        results['regla_de_tres'] = r3_results
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f'  Results: {results_path}')


# ######################################################################
#  SECTION 6: ENTRY POINT
# ######################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train GPT-2 + Triadic Head v3')

    # Model
    parser.add_argument('--model', default='gpt2-medium',
                        choices=['gpt2', 'gpt2-medium', 'gpt2-large'])
    parser.add_argument('--freeze-base', action='store_true')
    parser.add_argument('--bits', type=int, default=65)
    parser.add_argument('--dropout', type=float, default=0.1)
    parser.add_argument('--head-mode', default='simple', choices=['simple', 'deep'],
                        help='Triadic head: simple (1 layer, blueprint) or deep (2 layer MLP)')
    parser.add_argument('--activation', default='ifsq', choices=['tanh', 'ifsq'],
                        help='Triadic activation: ifsq (prevents dead bits) or tanh')
    parser.add_argument('--grad-checkpoint', action='store_true', default=True,
                        help='Gradient checkpointing (saves ~30%% VRAM, ON by default)')
    parser.add_argument('--no-grad-checkpoint', dest='grad_checkpoint', action='store_false')
    parser.add_argument('--no-compile', action='store_true')

    # Data
    parser.add_argument('--corpus', type=str, default=None)
    parser.add_argument('--corpus-dir', type=str, default=None)
    parser.add_argument('--max-docs', type=int, default=100000)
    parser.add_argument('--block', type=int, default=256)

    # Training
    parser.add_argument('--steps', type=int, default=50000)
    parser.add_argument('--batch-size', type=int, default=4)
    parser.add_argument('--accum-steps', type=int, default=2,
                        help='Gradient accumulation steps (effective batch = batch_size * accum)')
    parser.add_argument('--lr', type=float, default=3e-4)
    parser.add_argument('--alpha', type=float, default=0.05,
                        help='Triadic loss weight (>0.05 causes collapse)')
    parser.add_argument('--entropy-weight', type=float, default=1.0)
    parser.add_argument('--align-weight', type=float, default=5.0)
    parser.add_argument('--align-mode', default='infonce', choices=['mse', 'infonce'])
    parser.add_argument('--sup-weight', type=float, default=2.0)
    parser.add_argument('--sub-weight', type=float, default=5.0)
    parser.add_argument('--triadic-warmup-pct', type=float, default=0.50)
    parser.add_argument('--no-supervision', action='store_true')
    parser.add_argument('--resume', type=str, default=None,
                        help='Resume from checkpoint path')

    # Output
    parser.add_argument('--run-name', default='gpt2_triadic_65_v3')
    parser.add_argument('--print-every', type=int, default=50)
    parser.add_argument('--eval-every', type=int, default=1000)
    parser.add_argument('--save-every', type=int, default=2500)
    parser.add_argument('--dtype', default='bfloat16',
                        choices=['float32', 'float16', 'bfloat16'])

    args = parser.parse_args()
    train(args)
