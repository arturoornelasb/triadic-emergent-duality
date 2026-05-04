# Triadic Emergent Duality

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19375167.svg)](https://doi.org/10.5281/zenodo.19375167) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19374914.svg)](https://doi.org/10.5281/zenodo.19374914)
[![HF V5](https://img.shields.io/badge/%F0%9F%A4%97-triadic--gpt2--medium--v5-yellow)](https://huggingface.co/arturoornelasb/triadic-gpt2-medium-v5) [![HF V6](https://img.shields.io/badge/%F0%9F%A4%97-triadic--gpt2--medium--v6-yellow)](https://huggingface.co/arturoornelasb/triadic-gpt2-medium-v6) [![HF V8](https://img.shields.io/badge/%F0%9F%A4%97-triadic--gpt2--medium--v8-yellow)](https://huggingface.co/arturoornelasb/triadic-gpt2-medium-v8) [![HF V9](https://img.shields.io/badge/%F0%9F%A4%97-triadic--gptneo--125m--v9-yellow)](https://huggingface.co/arturoornelasb/triadic-gptneo-125m-v9)

Research framework proposing that conceptual complexity emerges from 14+ candidate dualities organized in 6 algebraic layers. Combines philosophical formalization (poset theory, category theory, modal logic) with empirical evaluation across 8 disciplines + 3 negative controls and a neurosymbolic language model (GPT-2 Medium + 72-bit triadic head).

**Author:** J. Arturo Ornelas Brand — Independent Researcher — arturoornelas62@gmail.com

## Core thesis

14 dualities emerge across 6 algebraic layers, each presupposing all previous ones:

| Layer | Algebra | Dualities |
|-------|---------|-----------|
| 1. Point (0D) | Boolean {0,1} | D1 Exist/Not-exist, D8 One/Many |
| 2. Line (1D) | Fuzzy {0,+} | D6 Movement/Stillness, D9 Inside/Outside, D10 Part/Whole |
| 3. Time (1D+t) | Ordinal {<,=,>} | D3 Before/After, D7 Order/Chaos, D12 Cause/Effect |
| 4. Plane (2D) | Modal {diamond,box} | D2 Here/Not-here, D4 Possible/Impossible, D5 Identity/Difference, D13 Similar/Different |
| 5. Volume (3D) | Trivalent {-,0,+} | D11 Life/Death, D14 Subject/Object |
| 6. Observer (3D+) | Probabilistic {0,?} | D14 Subject/Object (observer recursion) |

72 semantic primitives span these 6 layers. See `data/ALGEBRAIC_LAYERS.md` for full algebraic formalization and `data/dualidad_primitivo_map.json` for canonical duality definitions.

## Repository structure

```
README.md                           # This file
ROADMAP.md                          # Research roadmap
requirements.txt                    # Python dependencies

docs/
  teoria/                           # 23 theory documents (~44,000 words)
    01_definiciones.md - 13_tests_empiricos_completos.md
    29_metrica_universal_bits.md - 37_analisis_debilidades.md
    circulo_emergencia_dualidades_20mar2026.md
    plan_expansion_circulo_emergencia.md
  validaciones/                     # 16 domain validation documents
    14_validacion_musical.md - 28_validacion_psicologia.md
    36_validacion_inter_evaluador.md
  refs_bibliography.md              # 120+ references across 13 categories

data/
  primitivos.json                   # 72 semantic primitives (6 layers, 14 dual axes)
  ALGEBRAIC_LAYERS.md               # Algebraic layer documentation
  EXPANSION_v1.1.md                 # Expansion from 65 to 72 primitivos
  dualidad_primitivo_map.json       # 14 dualities -> anchor primitives mapping
  reference_domains.json            # 9 domains, 585 D/A/N classifications
  evaluator_templates/              # 9 domain-specific evaluation rubrics (JSON)
  interrater/                       # Inter-rater reliability data (CSV)
  adjacent_possible_paper/          # Supplementary data for companion paper (Zipf + MA~omega)

scripts/                            # 35 validation & analysis scripts
  test1-7_*.py                      # Core structure tests
  test8-16_*.py                     # Domain validations (9 domains)
  verify_algebraic_layers.py        # Algebraic layer verification (86% match)
  find_algebraic_gaps.py            # Gap analysis + capa 6 candidates
  algebraic_regla_de_tres.py        # Proportionality chain verification
  meta_analysis_*.py                # Statistical meta-analyses
  domain_validity_score.py          # IDVS metric
  interrater_*.py                   # Blind rater agreement statistics

dualidademergente+reptimeline/      # Neural training & analysis
  EXPERIMENT_LOG.md                 # Central experiment registry (v1-v5)
  model/
    gpt2_triadic.py                 # GPT-2 Medium + N-bit triadic head
    triadic.py                      # Neurosymbolic bridge (primes <-> bits)
    triadic_extractor.py            # reptimeline integration
    train.py                        # Training pipeline (supports --freeze-base)
    explore.py                      # Post-training analysis + timeline + plots
    eval_perplexity.py              # Cross-run perplexity evaluation
    audit_all_duals.py              # All 14 dual pairs + near-collapse detection
    audit_learned_vs_target.py      # Learned vs gold comparison
    archive_run.py                  # Archive a run to runs/
    compare_runs.py                 # Compare two archived runs
    gold_primitivos_72.json         # 72 supervised targets (current)
    archive/                        # Deprecated files (v2 artifacts)
  neural/                           # 8 neural probes (Q1-Q8)
  stats/                            # Statistical hardening (stdlib only)
  internal/                         # Self-auditing analyses (i1-i5)
  runs/                             # Archived training runs
    v2/, v3/, v4/, v5_frozen/       # Each with results, manifests, plots
```

## Training runs

| Run | Bits | Accuracy | Unique | Coherence | PPL | Key Change |
|-----|------|----------|--------|-----------|-----|------------|
| v1 | 65 | ~90% | ? | ? | 2,777 | Baseline |
| v2 | 65 | 95.8% | 3.8% | ? | 6,735 | 262 domain anchors (bad targets) |
| v3 | 65 | 90.9% | 89.2% | 0.653 | 5,388 | 65 primitivos directos |
| v4 | 72 | 92.5% | 100% | 0.876 | 5,608 | Circle expanded +7 primitivos |
| **v5_frozen** | **72** | **90.8%** | **100%** | **0.818** | **31.95** | **freeze_base (forgetting FIXED)** |
| **v6** | **72** | **80.9%** | **21.4%** | **0.643** | **31.95** | **2,166 concepts (extended corpus), 48 active bits** |

See `dualidademergente+reptimeline/EXPERIMENT_LOG.md` for detailed run log and key discoveries.

## Tech stack

- **Python 3.10+** — scripts, stats toolkit, internal analyses, and neural probes use stdlib only
- **PyTorch** + **NumPy** — model training and extraction
- **Hugging Face Transformers** — GPT-2 Medium pre-trained backbone
- **reptimeline** — multi-checkpoint timeline analysis + visualizations
- GPU: tested on NVIDIA RTX 4060 Ti 16 GB

## Installation

```bash
git clone https://github.com/arturoornelasb/triadic-emergent-duality.git
cd triadic-emergent-duality
pip install -r requirements.txt
```

For GPU support, install PyTorch with CUDA first:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu124
```

### Validation scripts (no dependencies beyond stdlib)

```bash
python scripts/test1_branch_independence.py
python scripts/test8_music_validation.py
python scripts/verify_algebraic_layers.py
python scripts/algebraic_regla_de_tres.py
```

### Neural model training (requires PyTorch + GPU)

```bash
cd dualidademergente+reptimeline/model

# Download corpus
python download_corpus.py

# Train (freeze_base recommended)
python train.py --bits 72 --gold-file gold_primitivos_72.json \
  --run-name gpt2_triadic_72_v6 --freeze-base

# Full analysis pipeline
python explore.py --run-name <name> --gold-file gold_primitivos_72.json \
  --bits 72 --timeline
python eval_perplexity.py --runs <version>
python audit_all_duals.py
python audit_learned_vs_target.py --gold-file gold_primitivos_72.json

# Archive & compare
python archive_run.py <version>
python compare_runs.py v5_frozen <version>
```

## Key results

### Ontological validation
- **8/8** positive domains at IDVS = 1.000 (all pass I2 null baseline, p95 = 0.931)
- **8/8** permutation tests survive Holm-Bonferroni correction (p = 0.0001 each)
- Negative control (Astrology) correctly rejected: IDVS = 0.479
- Bayesian ordering: BF = **121.4** (decisive) vs reversed order
- Algebraic layer mapping: **86% match** across 6 algebras (12/14 dualities)
- Sensitivity: topology most robust, classification logic most fragile

### Neural validation (v5_frozen)
- GPT-2 Medium (355M) + 72-bit triadic head (73K trainable params)
- **PPL 31.95** — identical to GPT-2 baseline (catastrophic forgetting solved)
- **90.8% bit accuracy**, 100% unique learned signatures
- Regla de tres: **cosine 0.997** (near-perfect relational structure preservation, 8 quadruples)
- 5/13 dual axes show significant anti-correlation (BH-FDR corrected)
- Phase transition at step 6000 (p = 0.0004)
- DAG recovery: F1 above random (p = 0.001), precision limited by dead bits

### Neural validation (v6 — extended corpus)
- Same architecture, **2,166 concepts** (72 primitives + 2,094 from first-principles corpus across 14 sciences)
- **PPL 31.95** — backbone still intact after 100K steps
- **80.9% bit accuracy** on 2,166 concepts, **95.2% subsumption accuracy**
- **48/72 active bits** (vs 4 in v5) — field density forces bit utilization
- Regla de tres: **cosine 0.998** (relational structure improves with more data)
- Phase transition at step 55,000 (warmup boundary), **inverted layer emergence** (L6 before L1)
- 501 discovered dependencies, 1,714 triadic dependencies

### Algebraic and inter-rater probes (v8 / v9)
- **Q13 algebraic Markov blanket** — PASS 100% (500K pairs, 0 violations) on both v8 and v9; verifies FTA-guaranteed gcd(μ₁,μ₂)=1 over learned codes (implementation correctness, not emergent property)
- **Q13 MI probe** — v8 NEGATIVE / v9 MIXED; T2 layer-hierarchy ratio non-adj/adj < 0.8 passes (0.50 / 0.67), T4 non-edge partial correlation fails (~49%)
- **Q18 quaternionic product** — VERIFIED on v8 (closure, associativity, inverses, ij=k, non-commutativity, layer recovery, 14 dual products)
- **Q32 model vs human inter-rater** — Cohen's κ ∈ [-0.082, 0.111] across 8 domains (Philosophy highest, Chemistry lowest); the trained model does NOT recover expert D-A-N classifications and does not substitute for K2 human-vs-human validation
- **D15 formal proposal** — `docs/teoria/37_operador_capa6_D15.md` proposes Collapse/Superposition as the layer-6 internal operator, closing the symmetric pattern 1,1,2,2,1,1 (not yet empirically validated)

## Documents

| Location | Topic |
|----------|-------|
| `docs/teoria/01-13` | Formal definitions, critical sequence, philosophical precedents, bifurcations |
| `docs/validaciones/14-28` | Domain validations: music, chemistry, biology, math, philosophy, physics, linguistics, psychology |
| `docs/teoria/29-37` | Bit entropy metrics, composition algebra, weakness analysis |
| `docs/validaciones/36` | Inter-rater reliability |
| `data/ALGEBRAIC_LAYERS.md` | Algebraic layer formalization |
| `EXPERIMENT_LOG.md` | Neural training experiment registry |

## Pre-trained Weights

| Model | HuggingFace | Files |
|-------|-------------|-------|
| V5_frozen GPT-2 Medium (355M) | [arturoornelasb/triadic-gpt2-medium-v5](https://huggingface.co/arturoornelasb/triadic-gpt2-medium-v5) | best.pt, run_config.json, gold_primitivos_72.json, results.json, training_log.csv |
| V6 GPT-2 Medium (355M) | [arturoornelasb/triadic-gpt2-medium-v6](https://huggingface.co/arturoornelasb/triadic-gpt2-medium-v6) | best.pt, run_config.json, gold_extended_v6.json, results.json, training_log.csv |
| V8 GPT-2 Medium (345M) | [arturoornelasb/triadic-gpt2-medium-v8](https://huggingface.co/arturoornelasb/triadic-gpt2-medium-v8) | best.pt, step_30000.pt (X-ray base), run_config.json, gold |
| V9 GPT-Neo 125M | [arturoornelasb/triadic-gptneo-125m-v9](https://huggingface.co/arturoornelasb/triadic-gptneo-125m-v9) | best.pt, step_5000.pt (X-ray base), run_config.json, gold |

V5 and V6 ship the production-milestone weights (frozen-base, 72-bit head). V8 and V9 also include base checkpoints (`step_*`) for reproducing the telescopic X-ray analysis (cascade detection).

## Companion Papers

This project is part of a family of papers. The first four have DOIs on Zenodo; additional companions are in preparation:

### Triadic Neurosymbolic Engine

- **Paper:** Ornelas Brand, J. A. (2026). *Triadic Neurosymbolic Engine: Prime Factorization as a Neurosymbolic Bridge: Projecting Continuous Embeddings into Discrete Algebraic Space for Deterministic Verification.* Zenodo. [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19205805.svg)](https://doi.org/10.5281/zenodo.19205805)
- **Repository:** [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18748671.svg)](https://doi.org/10.5281/zenodo.18748671)

### reptimeline

- **Paper:** Ornelas Brand, J. A. (2026). *reptimeline: Tracking Discrete Representation Evolution During Neural Network Training.* Zenodo. [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19208672.svg)](https://doi.org/10.5281/zenodo.19208672)
- **Repository:** [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19208628.svg)](https://doi.org/10.5281/zenodo.19208628)

### triadic-microgpt

- **Paper:** Ornelas Brand, J. A. (2026). *End-to-End Prime Factorization in a Generative Language Model: Emergent Algebraic Semantics from Joint Training.* Zenodo. [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19206545.svg)](https://doi.org/10.5281/zenodo.19206545)
- **Repository:** [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19207845.svg)](https://doi.org/10.5281/zenodo.19207845)

### Duality Synthesis in Quaternionic Logic

- **Paper:** Ornelas Brand, J. A. (2026). *Duality Synthesis in Quaternionic Logic: How Opposites Generate Truth.* Zenodo. [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19561634.svg)](https://doi.org/10.5281/zenodo.19561634)
- Defines synthesis $a \oplus \bar{a} = \mathrm{lcm}(\Phi(a),\Phi(\bar{a}))$ on the prime algebra; verifies the quaternionic product axioms exercised in Q18.
- **Source/PDF:** [`data/adjacent_possible_paper/duality_synthesis.tex`](data/adjacent_possible_paper/duality_synthesis.tex)

### Pre-Logical States and the Birth of Information

- **Paper:** Ornelas Brand, J. A. (2026). *Pre-Logical States and the Birth of Information: How Reasoning Operates Before Truth Exists.* Zenodo. [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19561722.svg)](https://doi.org/10.5281/zenodo.19561722)
- Formalizes pre-logical states in the quaternionic framework, connecting collapse to Friston's free energy minimization.
- **Source/PDF:** [`data/adjacent_possible_paper/pre_logical_states.tex`](data/adjacent_possible_paper/pre_logical_states.tex)

### The Adjacent Possible Has a Lattice (in preparation)

- **Paper:** Ornelas Brand, J. A. (2026). *The Adjacent Possible Has a Lattice: Formalizing Kauffman's Concept via Prime Product Spaces.* Manuscript in preparation.
- **Supplementary data:** [`data/adjacent_possible_paper/`](data/adjacent_possible_paper/) -- Zipf simulation on the prime lattice and MA~omega numerical correlation analysis (12 files, see internal README).

## License

Business Source License 1.1 (BUSL-1.1). See [LICENSE](LICENSE), [TERMS.md](TERMS.md), and [COMMERCIAL.md](COMMERCIAL.md) for details.

Contact: arturoornelas62@gmail.com
