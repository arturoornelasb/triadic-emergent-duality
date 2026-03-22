# Dualidad Emergente

Research framework proposing that conceptual complexity emerges from 7 fundamental dualities in a strict logical order. Combines philosophical formalization (poset theory, category theory, modal logic) with empirical validation across 9 disciplines and a neurosymbolic language model (GPT-2 Medium + 65-bit triadic head).

**Author:** J. Arturo Ornelas Brand

## Core thesis

Seven dualities emerge in necessary sequence, each presupposing all previous ones:

| # | Duality | Domain |
|---|---------|--------|
| D1 | Existir / No-existir | Ontology |
| D2 | Aqui / No-aqui | Space |
| D3 | Antes / Despues | Time |
| D4 | Posible / Imposible | Modal logic (hinge) |
| D5 | Ser / No-ser | Identity |
| D6 | Movimiento / Quietud | Physics |
| D7 | Orden / Caos | Information |

D1-D3 form the **scenario** (minimal conditions for reality). D4 is the **hinge** dividing static from dynamic. D5-D7 are the **dynamic** layer. Documents 04-12 extend the framework with 7 additional dualities (D8-D14).

## Repository structure

```
01-37_*.md                          # 37 theory documents (~44,000 words)
circulo_emergencia_dualidades_*.md  # Origin session: 7 dualities discovery
plan_expansion_circulo_emergencia.md # Research roadmap for D8-D14
refs_bibliography.md                # 120+ references across 13 categories

data/
  primitivos.json             # 65 semantic primitives (6 layers, 13 dual axes)
  dualidad_primitivo_map.json # 14 dualities -> anchor primitives mapping
  reference_domains.json      # 9 domains, 585 D/A/N classifications
  evaluator_templates/        # 9 domain-specific evaluation rubrics (JSON)
  interrater/                 # Inter-rater reliability data (CSV)

scripts/                      # 32 validation & analysis scripts
  test1-7_*.py                # Core structure tests (branch independence,
                              #   betweenness, autosimilarity, bit order,
                              #   holographic, abstraction zeros, poset)
  test8-16_*.py               # Domain validations (music, chemistry,
                              #   biology, math, philosophy, physics,
                              #   linguistics, psychology, astrology control)
  meta_analysis_*.py          # Statistical meta-analyses
  domain_validity_score.py    # IDVS metric (Inter-rater Domain Validity Score)
  interrater_*.py             # Blind rater agreement statistics
  weakness_analysis.py        # Identifies refutable claims
  integration_audit.py        # System coherence check

dualidademergente+reptimeline/
  model/
    gpt2_triadic.py           # GPT-2 Medium + 65-bit triadic head
    triadic.py                # Neurosymbolic bridge (primes <-> bits)
    triadic_extractor.py      # reptimeline integration for probes
    train.py                  # Training pipeline
    anchors.py                # Anchor loading utilities
    download_corpus.py        # Corpus download script
    gold_primes_65.json       # 262 supervised anchors
  neural/                     # 8 neural probes (Q1-Q8, stdlib only)
    q1_probe_layer_order.py   # Do bits activate in layer order?
    q2_probe_duals.py         # Are dual pairs coherent?
    q3_probe_dag.py           # Does the primitivos DAG emerge?
    q4_probe_triadic.py       # 3-way dependencies present?
    q5_probe_phases.py        # Phase transitions?
    q6_probe_unsupervised.py  # Unsupervised structure discovery?
    q7_probe_causal.py        # Causal interventions?
    q8_probe_crossarch.py     # Universality across architectures?
    interpret.py              # Consolidator for all probe results
  stats/                      # Statistical hardening (stdlib only)
    bh_fdr.py                 # Benjamini-Hochberg FDR + Holm-Bonferroni
    bootstrap.py              # Bootstrap confidence intervals
    permutation.py            # Permutation tests
    effect_size.py            # Cohen's d, selectivity ratio
    power_analysis.py         # Simulation-based power analysis
    registry.py               # Central p-value registry
  internal/                   # Self-auditing analyses (i1-i5)
    i1_recalc_pvalues.py      # FDR correction of all reported p-values
    i2_null_baseline_idvs.py  # Permutation null for IDVS threshold
    i3_sensitivity.py         # Perturbation robustness analysis
    i4_bayesian_orders.py     # Bayes factor comparison of orderings
    i5_discrepancia_65_63.py  # 65-vs-63 bit discrepancy
```

## Tech stack

- **Python 3.8+** — scripts, stats toolkit, internal analyses, and neural probes use stdlib only
- **PyTorch** + **NumPy** — model training and extraction
- **Hugging Face Transformers** — GPT-2 Medium pre-trained backbone
- **reptimeline** — checkpoint-level representation extraction for neural probes
- GPU: tested on NVIDIA RTX 5060 Ti 16 GB (TF32, cuDNN, gradient checkpointing)

## Installation

```bash
git clone https://github.com/arturoornelasb/dualidad-emergente.git
cd dualidad-emergente
```

### Validation scripts (no dependencies beyond stdlib)

All 32 scripts in `scripts/`, the `stats/` toolkit, `internal/` analyses, and `neural/` probes run on Python stdlib only:

```bash
# Core structure tests
python scripts/test1_branch_independence.py
python scripts/test7_poset_extraction.py

# Domain validations
python scripts/test8_music_validation.py
python scripts/test14_astrology_control.py   # negative control

# Metrics and meta-analysis
python scripts/domain_validity_score.py
python scripts/meta_analysis_8domains.py

# Self-auditing (robustness checks)
python dualidademergente+reptimeline/internal/i1_recalc_pvalues.py
python dualidademergente+reptimeline/internal/i2_null_baseline_idvs.py
```

### Neural model training (requires PyTorch)

```bash
pip install torch numpy transformers reptimeline

# Download corpus
python dualidademergente+reptimeline/model/download_corpus.py

# Train GPT-2 Medium + 65-bit triadic head
python dualidademergente+reptimeline/model/train.py --model gpt2-medium --steps 50000

# Resume from checkpoint
python dualidademergente+reptimeline/model/train.py --resume checkpoints/gpt2_triadic_65_v2/step_25000.pt

# Run neural probes (requires trained checkpoints)
python dualidademergente+reptimeline/neural/q1_probe_layer_order.py --checkpoints <dir>
python dualidademergente+reptimeline/neural/interpret.py   # consolidate all results
```

## Key results

- **20/21** necessity proofs for the 7-duality sequence rated NECESSARY or STRONG
- **5/8** domains exceed the p95 null threshold (chemistry, biology, music, linguistics, psychology)
- **8/8** permutation tests on anchor consistency survive Holm-Bonferroni correction
- Bayesian ordering: BF = 121.4 (decisive) vs reversed order; BF = 1.1 vs Hegelian dialectic
- Holographic density ratio: 3.13x over random baseline
- Abstraction-zeros hypothesis: **refuted** (r = -0.470; abstraction is additive, not subtractive)
- DAG confirmed but **not a lattice** (63 primitives, 97 Hasse edges, max depth 8)

## Training architecture

```
L_total = L_lang + alpha * (L_tri + sup_weight * L_sup + sub_weight * L_sub)
```

| Component | Description |
|-----------|-------------|
| L_lang | Standard GPT-2 next-token cross-entropy |
| L_tri | 4-component triadic loss (diversity, contrastive, entropy, alignment) |
| L_sup | Supervised anchor MSE (262 gold anchors) |
| L_sub | Differentiable subsumption (enforces dependency hierarchy) |

Key hyperparameters: alpha=0.05, sup_weight=2.0, sub_weight=5.0, iFSQ activation.

## Documents

| Docs | Topic |
|------|-------|
| 01-03 | Formal definitions, critical sequence (21 necessity proofs), philosophical precedents |
| 04-06 | Dualities 8-14, mathematical formalization (poset/category/modal/topological), black hole analogy |
| 07-10 | Emergence theory, cross-disciplinary validation, TriadicGPT connection, synthesis & publication plan |
| 11-13 | Bifurcations D8-D14, empirical DAG extraction, complete test results |
| 14-28 | Domain validations (music, chemistry, biology, math, philosophy, physics, linguistics, psychology) + proportionality hypothesis + astrology negative control |
| 29-37 | Bit entropy metrics, inter-rater reliability, weakness analysis, composition algebra, integration audit |

## License

All rights reserved. Contact the author for permissions.
