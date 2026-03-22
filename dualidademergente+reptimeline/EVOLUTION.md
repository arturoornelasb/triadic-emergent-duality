# Evolution: triadic-microgpt → dualidademergente+reptimeline

This project is the logical evolution of [triadic-microgpt](../../triadic-microgpt/).
It takes the core architecture and training methodology developed across 26+ experiments
and scales it to a pre-trained GPT-2 Medium backbone with 65 semantic primitives from
the dualidad_emergente philosophical framework.

## Lineage

```
triadic-microgpt (Mar 4-20, 2026)
  │
  ├── Run 1-9:   Architecture discovery (1M → 40M params)
  ├── Run 10-15: Loss formulation (alignment, entropy, contrastive)
  ├── Run 15:    Production model (40M, self-supervised, "strong align")
  ├── D-A5:      Supervised anchors (54 v1 anchors, 79.4% accuracy)
  ├── D-A14:     Best model (158 v2 anchors, 93%, 98.3% subsumption)
  ├── D-A16:     iFSQ activation (93.2%, eliminates dead bits)
  ├── D-A17:     GPT-2 355M (97.7% bits BUT 1.7% sub — algebra destroyed)
  ├── D-A19:     GPT-2 355M fix (76.9% sub, 100% R3 — algebra restored)
  │
  └──→ dualidademergente+reptimeline (Mar 21+, 2026)
        │
        ├── GPT-2 Medium backbone (355M pre-trained params)
        ├── 65-bit triadic head (65 primitivos from La Danza Cósmica)
        ├── 262 supervised anchors (from gold_primes_65.json)
        ├── Full loss suite (lang + tri + sup + sub)
        ├── reptimeline integration (8 neural probes)
        └── Statistical hardening (BH-FDR, bootstrap, power analysis)
```

## Architecture Comparison

| Dimension | triadic-microgpt (XL) | dualidademergente |
|---|---|---|
| **Backbone** | Custom TriadicGPT (from scratch) | GPT-2 Medium (pre-trained HuggingFace) |
| **Parameters** | ~42M total | ~355M total |
| **Layers** | 12 | 24 |
| **Hidden dim** | 512 | 1024 |
| **Attention heads** | 8 | 16 |
| **Vocab** | 4,096 (custom BPE) | 50,257 (GPT-2 tokenizer) |
| **Triadic bits** | 63-64 | 65 |
| **Triadic head** | Linear(512→64), no bias | Linear(1024→65), no bias |
| **Head params** | ~32K | ~66K |
| **Pre-trained** | No (TinyStories from scratch) | Yes (WebText, 8M pages) |
| **Training data** | TinyStories (~470M tokens) | WikiText-103 (~100M tokens) |
| **Training time** | ~76 min (50K steps, RTX 5060 Ti) | ~5h estimated (50K steps) |

### Why GPT-2 Medium?

D-A19 proved that 355M-scale models CAN learn algebraic structure when the loss
formulation is correct. The pre-trained backbone provides:

1. **Rich embeddings** — 1024D vectors trained on 8M web pages encode deep semantic
   relationships. InfoNCE alignment leverages these tight clusters to teach the triadic
   head what "similar" means.

2. **Faster convergence** — The backbone already understands language. We only need to
   train a 66K-parameter projection head on top.

3. **Better generalization** — GPT-2's vocabulary (50,257 BPE tokens) covers any
   concept, not just the 4,096 in triadic-microgpt's custom tokenizer.

### Why 65 bits (not 63)?

triadic-microgpt uses 63 bits (one per primitivo in La Danza Cósmica's 7x7 system,
minus 2 for the framework's special overflow slots). Our system uses 65 bits because
the dualidad_emergente framework includes 2 additional primitives (`proporcion` at
bit 63 and `quietud` at bit 64) that extend the original 63-bit system.

## Training Configuration

Every hyperparameter was ported from triadic-microgpt's optimal configuration,
validated across experiments D-A14, D-A16, and D-A19.

### Loss Formula

```
L_total = L_lang + alpha * (L_tri + sup_weight * L_sup + sub_weight * L_sub)
```

| Loss | triadic-microgpt | dualidademergente | Source |
|---|---|---|---|
| **L_lang** | Cross-entropy (next token) | Same | Standard |
| **L_tri** (4 components) | diversity + contrastive + entropy + alignment | Same | Run 15 |
| **L_sup** | MSE(projection, gold_target) | Same | D-A14 |
| **L_sub** | relu(hyper_01 - hypo_01).mean() | Same | D-A19 (differentiable) |
| **alpha** | 0.05 | 0.05 | Pareto frontier (Run 16 showed alpha>0.1 destroys ordering) |
| **sup_weight** | 2.0 | 2.0 | D-A14 |
| **sub_weight** | 5.0 | 5.0 | D-A14 |
| **align_weight** | 5.0 | 5.0 | Run 15 |
| **entropy_weight** | 1.0 | 1.0 | Run 15 |
| **Alignment mode** | InfoNCE (for rich embeddings) | InfoNCE | Experiment 10b/c |

### Loss-Embedding Interaction (Key Finding from Experiment 10)

The alignment loss MUST match the embedding quality:

| Embedding Quality | Best Alignment Loss | Why |
|---|---|---|
| Rich (GPT-2 768D+, WebText) | **InfoNCE** | Clear pos/neg structure enables contrastive learning |
| Weak (from-scratch 512D) | **MSE** | Dense local gradients work without cluster structure |

This is why dualidademergente uses InfoNCE (not MSE) — GPT-2 Medium's 1024D embeddings
are rich, so InfoNCE closes 48% of the gap to oracle PCA (Experiment 10b/c).

### Optimizer & Schedule

| Parameter | triadic-microgpt | dualidademergente | Source |
|---|---|---|---|
| **Optimizer** | AdamW | AdamW | — |
| **Learning rate** | 3e-4 | 3e-4 | — |
| **Weight decay** | 0.01 | 0.01 | — |
| **Betas** | (0.9, 0.95) | (0.9, 0.95) | — |
| **LR warmup** | Linear, min(500, steps/10) | Same | — |
| **LR decay** | Cosine → 0.1 * base_lr | Same | — |
| **Grad clip** | 1.0 (norm) | 1.0 (norm) | — |
| **Triadic warmup** | 25-50% of steps | 50% | Conservative default |
| **Alpha warmup** | Linear over 20% post-triadic | Same | — |

### GPU Optimizations

| Optimization | triadic-microgpt | dualidademergente | Notes |
|---|---|---|---|
| **TF32 matmul** | Yes | Yes | `torch.set_float32_matmul_precision('high')` |
| **cuDNN benchmark** | Yes | Yes | `torch.backends.cudnn.benchmark = True` |
| **torch.compile** | Yes (if Triton) | Yes (if Triton) | ~15-20% speedup |
| **Mixed precision** | bfloat16 | bfloat16 | GradScaler only for float16 |
| **Gradient checkpointing** | Optional | Optional | `--grad-checkpoint` flag |

### Activation Function

| Activation | triadic-microgpt | dualidademergente | Notes |
|---|---|---|---|
| **tanh** | D-A14 (best model) | Available (`--activation tanh`) | Concentrates near 0, causes dead bits |
| **iFSQ** | D-A16 (tied best) | Default (`--activation ifsq`) | `2*sigmoid(1.6*x)-1`, uniform distribution |

iFSQ (Tencent, 2025) distributes activations more uniformly across [-1, +1],
reducing dead bits from ~26/63 to near zero. D-A16 matched D-A14's accuracy with
iFSQ, making it the preferred default.

## Supervision

### Anchor Concepts

| Aspect | triadic-microgpt | dualidademergente |
|---|---|---|
| **Source** | gold_primes_63.json (158 v2 anchors) | gold_primes_65.json (262 anchors) |
| **Primitives** | 63 (La Danza, 7x7 minus 2) | 65 (La Danza + proporcion + quietud) |
| **Split** | 80/20 train/test | 80/20 train/test |
| **Generation** | WordNet + manual factorization | anchors.py from reference_domains.json |

### Subsumption Pairs

If concept A's gold bits are a strict subset of concept B's, then A subsumes B.
The subsumption loss enforces this hierarchy differentiably:

```python
h_01 = (tanh_output + 1) / 2    # Map [-1,+1] → [0,1]
y_01 = (tanh_output + 1) / 2
loss = relu(h_01 - y_01).mean()  # Penalize hypernym > hyponym
```

**Critical lesson from D-A17/D-A19**: The subsumption loss MUST be differentiable.
D-A17 used `(x > 0).float()` which kills gradients, making the loss a no-op.
D-A19 fixed this with the `(x + 1) / 2` mapping. Our implementation uses the
D-A19-correct version from the start.

## Evaluation Suite

### During Training (every N steps)

| Metric | triadic-microgpt | dualidademergente |
|---|---|---|
| **Bit accuracy** (train/test) | Yes | Yes |
| **Subsumption** (train/test) | Yes | Yes |
| **Dead bits** (entropy < 0.3) | Yes | Yes |
| **Mean bit entropy** | Yes | Yes |
| **Regla de tres** (analogy) | At final step | At eval steps |
| **CSV columns** | 12-16 | 12 |

### Post-Training (neural probes via reptimeline)

dualidademergente adds 8 neural probes that triadic-microgpt does not have:

| Probe | Question | Status |
|---|---|---|
| Q1 | Layer order emergence | Spearman rho(capa, median_step) |
| Q2 | Dual coherence | 13 dual pairs, BH-FDR |
| Q3 | DAG recovery | Precision/Recall/F1/SHD |
| Q4 | Triadic 3-way dependencies | S/C/E/A classification |
| Q5 | Phase transitions | Criticality analysis |
| Q6 | Unsupervised discovery | BitDiscovery + AutoLabeler |
| Q7 | Causal verification | Intervention effects |
| Q8 | Cross-architecture | SAE / VQ-VAE comparison |

These probes use the [reptimeline](../../reptimeline/) library to extract
representation timelines from training checkpoints and analyze emergence patterns.

## Statistical Hardening

dualidademergente adds a full statistical toolkit that triadic-microgpt lacks:

| Module | Purpose |
|---|---|
| `stats/bh_fdr.py` | Benjamini-Hochberg FDR + Holm-Bonferroni |
| `stats/bootstrap.py` | Bootstrap confidence intervals |
| `stats/permutation.py` | Permutation tests |
| `stats/effect_size.py` | Cohen's d, selectivity ratio |
| `stats/power_analysis.py` | Simulation-based power analysis |
| `stats/registry.py` | Central p-value registry with program-wide correction |

Every p-value from the neural probes is registered and corrected for multiple testing.

## What dualidademergente Inherits vs. Adds

### Inherited (from triadic-microgpt)

- Full 4-component triadic loss (diversity + contrastive + entropy + alignment)
- Supervised anchor loss (L_sup via MSE)
- Differentiable subsumption loss (L_sub, D-A19 version)
- iFSQ activation
- InfoNCE alignment (for rich embeddings)
- Cosine LR schedule with warmup
- AdamW optimizer (0.9, 0.95)
- GPU optimizations (TF32, cuDNN, torch.compile, bfloat16)
- Regla de tres analogy evaluation
- Best-model selection by test accuracy
- PrimeMapper and BitwiseValidator (triadic algebra)

### Added (new in dualidademergente)

- **GPT-2 Medium backbone** (355M pre-trained, vs 42M from scratch)
- **65-bit system** (vs 63-64 bits)
- **262 anchors** (vs 158)
- **reptimeline integration** (TriadicExtractor → ConceptSnapshot → probes)
- **8 neural probes** (Q1-Q8, structured as falsifiable questions)
- **Statistical hardening** (FDR, bootstrap CI, power analysis)
- **Internal audits** (I1-I5: p-value recalculation, null baselines, sensitivity)
- **Epistemic framework** (every positive result reported with its confounder)

## Lessons Applied from triadic-microgpt Failures

| Failure | Lesson | How Applied |
|---|---|---|
| **Run 12**: entropy reg caused collapse | Coherence loss is toxic, remove it | Our triadic_loss has NO coherence component |
| **Run 16**: alpha=0.2 lost ordering | alpha must be ≤0.05 | Default alpha=0.05, with gradual warmup |
| **D-A15**: gradient decoupling = random | Cannot decouple triadic from language gradients | Joint training, no gradient surgery |
| **D-A17**: 355M destroyed algebra | Need full 4-component loss + differentiable sub | All 4 components active, differentiable sub |
| **D-A17**: ternary zeros collapsed | 355M pushes all bits to ±1 | iFSQ distributes more uniformly |
| **Exp 10a**: MSE fails with rich embeddings | Loss must match embedding quality | InfoNCE for GPT-2 (rich) |

## Known Limitations

1. **Scale-algebra tradeoff**: D-A19 showed 76.9% subsumption at 355M vs 98.3% at 40M.
   Larger models may need explicit sparsity targets to preserve algebraic structure.
   Our v2 does not include a sparsity target loss — this is a known gap from D-A19
   that may be needed if subsumption rates are low.

2. **No ternary quantization**: triadic-microgpt's D-A13/D-A19 experiments used
   ternary {-1, 0, +1} with FSQ quantization. Our system uses continuous [-1, +1]
   via iFSQ (no hard quantization during training). The algebraic operations
   (PrimeMapper, BitwiseValidator) still work on binarized outputs (threshold > 0).

3. **Training time**: GPT-2 Medium takes ~5h for 50K steps vs ~76 min for 40M.
   The pre-trained backbone compensates with faster convergence.

## Experiment Timeline

| Phase | triadic-microgpt | dualidademergente |
|---|---|---|
| Architecture discovery | Runs 1-9 (Mar 4-5) | — (inherited) |
| Loss formulation | Runs 10-18 (Mar 5-8) | — (inherited) |
| Supervised anchors | D-A5, D-A14 (Mar 18-19) | v1 (20K steps, Mar 21) |
| iFSQ activation | D-A16 (Mar 19) | — (inherited) |
| GPT-2 scaling | D-A13, D-A17, D-A19 (Mar 18-20) | **v2 training** (Mar 21+) |
| Statistical hardening | — | I1-I5 (Mar 21) |
| Neural probes | — | Q1-Q8 (Mar 21+) |

## Hardware

All experiments on the same machine:
- **GPU**: NVIDIA RTX 5060 Ti 16GB (Blackwell)
- **CPU**: AMD Ryzen 7 5800XT
- **RAM**: 64GB DDR4
- **Conda env**: `triadic-microgpt` (PyTorch 2.12.0.dev+cu128)
