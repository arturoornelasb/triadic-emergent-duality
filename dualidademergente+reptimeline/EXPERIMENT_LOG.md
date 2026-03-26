# Experiment Log — Dualidad Emergente: Triadic Neural Training

Central registry of all training runs, decisions, and findings.

---

## Run Summary

| Run | Date | Bits | Concepts | Accuracy | Unique | Coherence | PPL | Dead Bits | Time | Key Change |
|-----|------|------|----------|----------|--------|-----------|-----|-----------|------|------------|
| v1 | 2026-03-22 | 65 | 65 | ~90%? | ? | ? | 2,777 | ? | ~5h | Baseline training |
| v2 | 2026-03-22 | 65 | 262 | 95.8% | 3.8% | ? | 6,735 | 23 | 4.9h | 262 domain anchors (bad targets) |
| v3 | 2026-03-22 | 65 | 65 | 90.9% | 89.2% | 0.653 | 5,388 | 47 | 5.8h | 65 primitivos directos (fixed targets) |
| v4 | 2026-03-23 | 72 | 72 | 92.5% | 100% | 0.876 | 5,608 | 52 | 5.8h | Circle expanded: 7 new primitivos |
| **v5_frozen** | **2026-03-23** | **72** | **72** | **90.8%** | **100%** | **0.818** | **31.95** | **68** | **4.3h** | **freeze_base=True (forgetting FIXED)** |
| **v6** | **2026-03-25** | **72** | **2,166** | **80.9%** | **21.4%** | **0.643** | **31.95** | **37** | **12.3h** | **Extended corpus (first-principles, 14 sciences), 100K steps** |

### Key Metrics Explained
- **Accuracy**: Best test bit accuracy (how many bits the model gets right)
- **Unique**: % of concepts with unique learned signatures
- **Coherence**: Mean dual coherence across all ejes_duales (PrimitiveOverlay metric)
- **PPL**: Perplexity on general text (baseline GPT-2 Medium = 31.95)
- **Dead Bits**: Bits that are always ON or always OFF (not discriminative)

---

## Detailed Run Log

### V1 — Baseline (2026-03-22)
- **Config**: GPT-2 Medium (355M) + Linear(1024, 65) triadic head
- **Training**: 50K steps, lr=3e-4, alpha=0.05, batch=4x2=8
- **GPU**: RTX 4060 Ti 16GB
- **Architecture**: Used `triadic_proj` (Sequential) — later changed to `triadic_head` (Linear)
- **Result**: Baseline training, no formal analysis archived
- **PPL**: 2,777 (severe degradation)
- **Archive**: `checkpoints/gpt2_triadic_65/` (no formal archive)

### V2 — 262 Domain Anchors (2026-03-22)
- **Change**: 262 anchor concepts from 8 domains instead of 65 primitivos
- **Gold file**: `gold_primes_65.json`
- **Result**: 95.8% accuracy — MODEL was correct, TARGETS were wrong
- **Root cause**: Only 10 unique signatures in 262 targets (3.8%)
- **Lesson**: High accuracy with bad targets = memorization, not learning
- **PPL**: 6,735 (worst of all runs)
- **Archive**: `runs/v2/`
- **Docs**: `runs/v2/NEXT_STEPS.md`

### V3 — 65 Primitivos Directos (2026-03-22)
- **Change**: Each concept gets its own unique target (bit_own + transitive deps)
- **Gold file**: `gold_primitivos_65.json` (65 concepts, 65 unique signatures)
- **Result**: 90.9% accuracy, 89.2% unique learned signatures
- **Key finding**: 3 collapsed dual pairs (placer/dolor 0.286, vida/muerte 0.175, mover/quietud 0.396)
- **PPL**: 5,388 (still severe degradation)
- **Archive**: `runs/v3/`
- **Docs**: `runs/v3/ANALYSIS.md`

### V4 — 72-bit Circle Expansion (2026-03-23)
- **Change**: Added 7 new primitivos to strengthen collapsed pairs:
  - atracción (capa 3), decaimiento (capa 4), aversión (capa 4)
  - cooperación (capa 4), pérdida (capa 4), atención (capa 5), intención (capa 5)
- **Gold file**: `gold_primitivos_72.json` (72 concepts, 72 bits)
- **Result**: 92.5% accuracy, 100% unique, coherence 0.876 (+0.223 vs v3)
- **Key finding**: P2 REFUTED — adding training diversity fixes collapsed pairs even without changing their targets
- **Insight**: Resolution depends on anchor field DENSITY, not bits per concept
- **PPL**: 5,608 (still degraded)
- **Archive**: `runs/v4/`
- **Docs**: `runs/v4/ANALYSIS.md`

### V5_frozen — Freeze Base (2026-03-23)
- **Change**: `--freeze-base` — only train triadic head (73,728 params vs 355M)
- **Gold file**: `gold_primitivos_72.json`
- **Trainable params**: 73,728 (0.02% of total)
- **Result**: 90.8% accuracy, 100% unique, coherence 0.818
- **Critical fix**: PPL = 31.95 (IDENTICAL to GPT-2 baseline) — forgetting SOLVED
- **Trade-offs**:
  - Accuracy: -1.7% (92.5% → 90.8%) — acceptable
  - Dead bits: 52 → 68 — head uses fewer bits
  - Entropy: 0.324 → 0.039 — less diversity in bit usage
- **Improvements over V4**:
  - Per-domain accuracy: +22% (0.59 → 0.72) — more faithful to targets
  - Regla de tres: 0.886 → 0.996 cosine — near-perfect relational structure
  - vida/muerte: 0.667 → 0.941, receptivo/creador_obs: 0.773 → 1.000
- **Regressions**:
  - libertad/control: 0.921 → 0.684
  - temporal_obs/eterno_obs: 0.875 → 0.571
- **Reconciler findings**: Bits 8 (eje_profundidad, 99%) and 11 (posición_temporal, 96%) collapsed to always-ON
- **Archive**: `runs/v5_frozen/`
- **Plots**: `runs/v5_frozen/plots/` (swimlane, phase_dashboard, churn_heatmap, layer_emergence)

---

## Key Discoveries

### 1. Field Density > Individual Targets (V4)
Adding 7 new primitivos improved collapsed pairs (placer/dolor 0.29→0.97) even though their gold targets didn't change. The mechanism: more diverse training examples teach the model what good differentiation looks like. **Implication**: path forward is more concepts, not more bits.

### 2. Catastrophic Forgetting Fixed (V5)
ALL runs v1-v4 showed PPL >2700 (baseline 32). Training on 72 definitions × 50K steps causes the model to forget general language. Solution: freeze GPT-2, only train the triadic head. Cost: -1.7% accuracy. Benefit: model can generate text again.

### 3. Regla de Tres Improves with Frozen Base (V5)
Counter-intuitively, freezing the base improved relational structure (cosine 0.886→0.996). The head-only training finds better proportional relationships between dual pairs, possibly because it can't "cheat" by using the full model to memorize individual patterns.

### 4. Layer Emergence Order (V5 timeline)
- Layer 2 (Línea) emerges FIRST (~step 10,000)
- Layers 3/4/6 emerge together (~step 27,500)
- Layer 1 (Punto) paradoxically late — basic concepts take long to differentiate
- Layer 5 (Volumen/Vida) takes longest, 2 primitives never activate

### 5. Near-Collapses (V5 audit)
Several non-dual concept pairs are dangerously similar:
- placer/atracción: Jaccard 0.909 (should be distinct: capa 5 vs capa 3)
- verdad/vida, libertad/vida: Jaccard 0.880 (different domains, same signatures)
- más/menos: Jaccard 0.844 (conceptual opposites, model can't distinguish)

---

## Algebraic Layer Theory

6 algebras map to 6 capas:
1. Boolean {0,1} — vacío, información, uno
2. Fuzzy {0,+} — fuerza, más, menos, unión, separación, ...
3. Ordinal {<,=,>} — mover, orden, caos, creación, destrucción, ...
4. Modal {◇,□} — puede, debe, verdad, mentira, bien, mal, ...
5. Trivalent {-,0,+} — vida, muerte, placer, dolor, consciente, ...
6. Probabilistic {0,?} — temporal_obs, eterno_obs, receptivo, creador_obs

14 dualidades as operators: 5 TRANSITION (inter-capa), 7 INTERNAL (intra-capa), 2 SKIP.
Verification: 12/14 match (86%). D6→D14 proportionality chain passes.
Capa 6 missing internal operator — top candidate: Autopoiesis.

---

## Pipeline

```bash
# Train
python train.py --bits 72 --gold-file gold_primitivos_72.json \
  --run-name gpt2_triadic_72_v6 --freeze-base

# Analyze
python explore.py --run-name gpt2_triadic_72_v6 \
  --gold-file gold_primitivos_72.json --bits 72 --timeline
python audit_learned_vs_target.py --gold-file gold_primitivos_72.json
python audit_all_duals.py
python eval_perplexity.py --runs v6

# Archive & compare
python archive_run.py v6
python compare_runs.py v5_frozen v6
```

---

## Next Steps (V6)

**Phase 2: Densify anchor field with first_principles**
- Map 3,596 first_principles to 72-bit signatures
- Add as training data (NOT new primitivos)
- Expected: better near-collapse resolution (placer/atracción etc.)
- Keep freeze_base=True

**Phase 3: Alpha schedule (if per-domain accuracy still low)**
- alpha_start=0.2 → alpha_end=0.05 over training
- First impose structure, then refine precision

---

## File Index

| File | Purpose |
|------|---------|
| `model/train.py` | Training script |
| `model/explore.py` | Post-training exploration + timeline + plots |
| `model/audit_learned_vs_target.py` | Learned vs gold comparison |
| `model/audit_all_duals.py` | Comprehensive dual pair analysis |
| `model/eval_perplexity.py` | Language model perplexity evaluation |
| `model/archive_run.py` | Archive a run to runs/ |
| `model/compare_runs.py` | Compare two archived runs |
| `model/generate_gold_primitivos.py` | Generate gold targets from primitivos.json |
| `data/primitivos.json` | 72 primitivos definition (capas, deps, duals) |
| `data/ALGEBRAIC_LAYERS.md` | Algebraic layer documentation |
| `scripts/verify_algebraic_layers.py` | Algebraic verification (86% match) |
| `scripts/find_algebraic_gaps.py` | Gap analysis + capa 6 candidates |
| `scripts/algebraic_regla_de_tres.py` | Proportionality + predictions |
| `runs/{version}/manifest.json` | Per-run metadata |
| `runs/{version}/ANALYSIS.md` | Per-run human analysis |
