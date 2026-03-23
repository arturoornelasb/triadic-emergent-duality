# Dualidad Emergente

Research framework proposing that conceptual complexity emerges from 14 fundamental dualities organized in 6 algebraic layers. Combines philosophical formalization (poset theory, category theory, modal logic) with empirical validation across 9 disciplines and a neurosymbolic language model (GPT-2 Medium + 72-bit triadic head).

**Author:** J. Arturo Ornelas Brand

## Core thesis

14 dualities emerge across 6 algebraic layers, each presupposing all previous ones:

| Layer | Algebra | Dualities |
|-------|---------|-----------|
| 1. Punto | Boolean {0,1} | D1 Existir/No-existir |
| 2. Linea | Fuzzy {0,+} | D2 Aqui/No-aqui, D3 Antes/Despues |
| 3. Plano | Ordinal {<,=,>} | D5 Movimiento/Quietud, D6 Orden/Caos, D7 Creacion/Destruccion |
| 4. Volumen | Modal {diamond,box} | D4 Posible/Imposible, D8 Verdad/Mentira, D9 Bien/Mal |
| 5. Vida | Trivalent {-,0,+} | D10 Vida/Muerte, D11 Placer/Dolor, D12 Libertad/Control |
| 6. Observador | Probabilistic {0,?} | D13 Temporal/Eterno, D14 Receptivo/Creador |

72 semantic primitives span these 6 layers. See `data/ALGEBRAIC_LAYERS.md` for full algebraic formalization.

## Repository structure

```
README.md                           # This file
ROADMAP.md                          # Research roadmap
requirements.txt                    # Python dependencies

docs/
  teoria/                           # 24 theory documents (~44,000 words)
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

See `dualidademergente+reptimeline/EXPERIMENT_LOG.md` for detailed run log and key discoveries.

## Tech stack

- **Python 3.10+** — scripts, stats toolkit, internal analyses, and neural probes use stdlib only
- **PyTorch** + **NumPy** — model training and extraction
- **Hugging Face Transformers** — GPT-2 Medium pre-trained backbone
- **reptimeline** — multi-checkpoint timeline analysis + visualizations
- GPU: tested on NVIDIA RTX 4060 Ti 16 GB

## Installation

```bash
git clone https://github.com/arturoornelasb/dualidad-emergente.git
cd dualidad-emergente
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

- **20/21** necessity proofs for the 7-duality sequence rated NECESSARY or STRONG
- **5/8** domains exceed the p95 null threshold (chemistry, biology, music, linguistics, psychology)
- **8/8** permutation tests survive Holm-Bonferroni correction
- Bayesian ordering: BF = 121.4 (decisive) vs reversed order
- Algebraic layer mapping: **86% match** across 6 algebras (12/14 dualities)
- V5 frozen: **PPL 31.95** (identical to GPT-2 baseline — forgetting solved)
- Regla de tres: **cosine 0.996** (near-perfect relational structure)
- 100% unique learned signatures across 72 primitivos

## Documents

| Location | Topic |
|----------|-------|
| `docs/teoria/01-13` | Formal definitions, critical sequence, philosophical precedents, bifurcations |
| `docs/validaciones/14-28` | Domain validations: music, chemistry, biology, math, philosophy, physics, linguistics, psychology |
| `docs/teoria/29-37` | Bit entropy metrics, composition algebra, weakness analysis |
| `docs/validaciones/36` | Inter-rater reliability |
| `data/ALGEBRAIC_LAYERS.md` | Algebraic layer formalization |
| `EXPERIMENT_LOG.md` | Neural training experiment registry |

## License

All rights reserved. Contact the author for permissions.
