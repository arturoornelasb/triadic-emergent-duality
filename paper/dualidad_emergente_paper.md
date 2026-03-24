# Emergent Duality: 14 Fundamental Dualities Across 6 Algebraic Layers, Validated by Domain Analysis and Neurosymbolic Learning

**J. Arturo Ornelas Brand**
Independent Researcher — arturoornelas62@gmail.com

---

## Abstract

We present a formal ontological framework in which conceptual complexity emerges from 14 fundamental dualities organized across 6 algebraic layers (Boolean, Fuzzy, Ordinal, Modal, Trivalent, Probabilistic). The framework is grounded in 72 semantic primitives connected by a directed acyclic graph (DAG) of 133+ dependency edges. We validate the framework through three independent methodologies: (1) domain analysis across 9 disciplines using the Information Domain Validity Score (IDVS), achieving IDVS = 1.000 for all 8 positive domains against a null baseline (p95 = 0.896, permutation p = 0.0001); (2) Bayesian model comparison yielding a Bayes factor of 121.4 (decisive) for the proposed ordering over reversed alternatives; and (3) neurosymbolic learning via a GPT-2 Medium model augmented with a 72-bit triadic head, which learns the primitive structure at 90.8% bit accuracy while preserving general language ability (PPL = 31.95, identical to baseline). The learned representations exhibit near-perfect relational structure (Regla de Tres cosine = 0.996) and show a significant phase transition during training (p = 0.0004). We report both confirmatory and null results transparently: layer ordering in neural representations is not significant (p = 0.71), and only 5 of 13 dual axes show significant learned anti-correlation after FDR correction.

**Keywords:** ontology, semantic primitives, emergence, duality, neurosymbolic AI, algebraic structure, domain validation

---

## 1. Introduction

The search for universal semantic primitives — irreducible conceptual atoms from which all meaning is composed — spans philosophy (Leibniz's *characteristica universalis*), linguistics (Wierzbicka's Natural Semantic Metalanguage), and computational semantics (ConceptNet, FrameNet). Existing approaches either lack formal algebraic structure or fail to demonstrate empirical universality across domains.

We propose that conceptual complexity emerges through a specific sequence of **dualities** — paired oppositions that each require all previous dualities as prerequisites. This emergence follows an algebraic chain:

$$\text{Boolean} \to \text{Fuzzy} \to \text{Ordinal} \to \text{Modal} \to \text{Trivalent} \to \text{Probabilistic}$$

Each algebra introduces operators that the previous one cannot express: degree from existence, comparison from degree, possibility from order, valuation from possibility, observation from valuation.

The contribution of this work is threefold:

1. **Formalization**: 72 semantic primitives organized in a DAG across 6 algebraic layers, with 14 dual axes and formal dependency rules.
2. **Empirical validation**: cross-domain analysis (8 disciplines + 1 negative control) using a novel metric (IDVS) with statistical hardening (permutation tests, FDR correction, Bayesian model comparison, null baselines).
3. **Neural validation**: a neurosymbolic model (GPT-2 Medium + triadic head) that learns the proposed structure from natural language, demonstrating that the algebraic relationships are recoverable from distributional semantics.

---

## 2. The Framework

### 2.1 Semantic Primitives

We define 72 semantic primitives distributed across 6 layers:

| Layer | Algebra | Primitives | Examples |
|-------|---------|------------|----------|
| 1. Point (0D) | Boolean {0,1} | 3 | vacío, información, uno |
| 2. Line (1D) | Fuzzy {0,+} | 8 | fuerza, contención, unión, separación |
| 3. Time (1D+t) | Ordinal {<,=,>} | 13 | mover, orden, caos, creación, destrucción |
| 4. Plane (2D) | Modal {◇,□} | 21 | bien, mal, verdad, mentira, libertad, control |
| 5. Volume (3D) | Trivalent {−,0,+} | 23 | vida, muerte, placer, dolor, consciente |
| 6. Observer (3D+) | Probabilistic {0,?} | 4 | temporal_obs, eterno_obs, receptivo, creador_obs |

Each primitive is assigned a unique prime number, a bit position, a layer, a set of dependencies (parents in the DAG), and a natural-language definition. The complete specification is in `data/primitivos.json`.

### 2.2 The Dependency DAG

Primitives are connected by a DAG with 133+ directed edges encoding the relation "X requires Y to exist." Key structural properties:

- **Layer monotonicity**: all dependencies of a layer-*n* primitive lie in layers ≤ *n*.
- **3 roots**: vacío (bit 0), información (bit 1), uno (bit 44) — all layer 1.
- **Transitive closure**: the maximum ancestor set size is 22 (for creador_obs, layer 6).

### 2.3 The 14 Dualities

The 14 dualities emerge in a specific order, each anchored by 2-4 primitives:

| # | Duality | Anchors | Layer |
|---|---------|---------|-------|
| D1 | Existir/No-existir | vacío, información, uno | 1 |
| D2 | Aquí/No-aquí | eje_profundidad, eje_vertical, eje_lateral | 2-4 |
| D3 | Antes/Después | posición_temporal, flujo_temporal | 3 |
| D4 | Posible/Imposible | puede, debe, tal_vez | 4 |
| D5 | Identidad/Diferencia | muchos, tipo_de, todo, algunos | 2-4 |
| D6 | Movimiento/Quietud | mover, hacer, quietud | 3 |
| D7 | Orden/Caos | orden, caos, bien, mal, verdad, mentira | 3-4 |
| D8 | Uno/Muchos | uno, muchos | 1-2 |
| D9 | Dentro/Fuera | contención, unión, separación | 2 |
| D10 | Parte/Todo | parte_de, todo, algunos | 2-4 |
| D11 | Vida/Muerte | vida, muerte, placer, dolor | 5 |
| D12 | Causa/Efecto | porque, si_entonces | 3 |
| D13 | Semejante/Diferente | tipo_de | 4 |
| D14 | Sujeto/Objeto | consciente, ausente, temporal_obs, eterno_obs, receptivo, creador_obs | 5-6 |

### 2.4 Algebraic Layer Chain

Each layer operates with a distinct algebra. The key insight is that each transition is **irreversible**: you cannot define the operators of layer *n* without having the operators of layer *n−1*. This is formalized in `data/ALGEBRAIC_LAYERS.md` and verified computationally at 86% match (12/14 dualities correctly predicted by their algebra assignment).

---

## 3. Domain Validation

### 3.1 The IDVS Metric

We define the **Information Domain Validity Score** for a domain *d* as:

$$\text{IDVS}(d) = \text{coverage}(d) \times \text{monotonicity}(d)$$

where:
- **Coverage** = 1 − (nulls in layers 1–4) / (total primitives in layers 1–4). A domain that classifies foundational primitives as N ("does not apply") is penalized.
- **Monotonicity** = 1 − (violations / total edges). A violation occurs when a child primitive has a higher state than its parent (D > A > N).

### 3.2 Classification Protocol

Each of 72 primitives is classified in each domain as:
- **D** (Direct): the primitive operates directly in this domain.
- **A** (Analogical): the primitive applies by metaphor or analogy.
- **N** (Null): the primitive does not apply.

### 3.3 Results

All 8 positive domains achieve IDVS = 1.000 after D-A-N reclassification based on domain-specific fundamental principles:

| Domain | Type | IDVS | Coverage | Monotonicity | Permutation p |
|--------|------|------|----------|--------------|---------------|
| Music | Positive | 1.000 | 1.000 | 1.000 | 0.0001 |
| Chemistry | Positive | 1.000 | 1.000 | 1.000 | 0.0001 |
| Biology | Positive | 1.000 | 1.000 | 1.000 | 0.0001 |
| Mathematics | Positive | 1.000 | 1.000 | 1.000 | 0.0001 |
| Philosophy | Positive | 1.000 | 1.000 | 1.000 | 0.0001 |
| Physics | Positive | 1.000 | 1.000 | 1.000 | 0.0001 |
| Linguistics | Positive | 1.000 | 1.000 | 1.000 | 0.0001 |
| Psychology | Positive | 1.000 | 1.000 | 1.000 | 0.0001 |
| **Astrology** | **Negative** | **0.479** | 0.650 | 0.737 | 0.0001 |

### 3.4 Null Baseline (I2)

To calibrate the IDVS threshold, we computed 10,000 random D-A-N assignments preserving the marginal distribution of each domain. The null distribution yields:
- Mean max IDVS: 0.861
- **p95**: 0.896 (→ threshold set at 0.90)
- **p99**: 0.955

All 8 positive domains (IDVS = 1.000) exceed p99. Astrology (0.479) falls far below the null mean.

### 3.5 Sensitivity Analysis (I3)

Three structural perturbation modes:

| Perturbation | Target | Mean ΔIDVS | Large disruptions |
|-------------|--------|------------|-------------------|
| Remove edge | DAG topology | −0.003 | 3.4% |
| Move layer | Layer assignment | 0.000 | 0.0% |
| Flip D-A-N | Classification logic | −0.060 | 71.4% |

**Robustness gradient**: Topology > Layering > Logic. The DAG structure is the most robust component; the D-A-N classifications are the most sensitive.

### 3.6 Bayesian Model Comparison (I4)

We compared 4 orderings of the 14 dualities using triangularity of the dependency matrix as the test statistic:

| Model | Triangularity | BF vs. Reversed |
|-------|---------------|-----------------|
| **Proposed** | **0.539** | **121.4** (decisive) |
| Hegel | 0.528 | — |
| Peirce | 0.484 | — |
| Reversed | 0.143 | 1.0 |

Against 1,000 random orderings (μ = 0.338), the proposed ordering is significant (p = 0.005).

---

## 4. Neural Validation

### 4.1 Architecture

We augment GPT-2 Medium (355M parameters) with a **triadic head**: a single linear projection from the 1024-dimensional hidden state to a 72-bit semantic vector. The activation function is iFSQ (2·sigmoid(1.6x) − 1), which distributes activations uniformly across [−1, +1].

**Total trainable parameters (v5_frozen)**: 73,728 (0.02% of model). The GPT-2 backbone is frozen.

### 4.2 Training

| Component | Configuration |
|-----------|---------------|
| Loss | L_lang + 0.05·(L_tri + 2·L_sup + 5·L_sub) |
| L_tri | diversity + InfoNCE + entropy + alignment |
| L_sup | MSE(projection, gold_target) |
| L_sub | relu(hypernym_01 − hyponym_01).mean() |
| Optimizer | AdamW (3e-4, β = 0.9/0.95) |
| Schedule | Cosine decay, 50% triadic warmup |
| Data | WikiText-103 (~100M tokens) |
| Steps | 50,000 |
| Hardware | NVIDIA RTX 4060 Ti 16GB |

### 4.3 Training Run Summary

| Run | Bits | Accuracy | Unique | Coherence | PPL | Key Change |
|-----|------|----------|--------|-----------|-----|------------|
| v1 | 65 | ~90% | ? | ? | 2,777 | Baseline |
| v2 | 65 | 95.8% | 3.8% | ? | 6,735 | Bad targets (262 domain anchors) |
| v3 | 65 | 90.9% | 89.2% | 0.653 | 5,388 | Fixed: 65 direct primitives |
| v4 | 72 | 92.5% | 100% | 0.876 | 5,608 | +7 primitives for collapsed pairs |
| **v5** | **72** | **90.8%** | **100%** | **0.818** | **31.95** | **Frozen base (forgetting solved)** |

### 4.4 Key Finding: Field Density > Individual Targets

V4 added 7 new primitives (atracción, aversión, decaimiento, cooperación, pérdida, atención, intención) to differentiate collapsed dual pairs (Jaccard > 0.80). The result was surprising: collapsed pairs resolved even though their individual gold targets did not change. The mechanism is **field density** — more diverse training examples teach the model what good differentiation looks like.

### 4.5 Key Finding: Catastrophic Forgetting Solved

All runs v1–v4 showed catastrophic language degradation (PPL > 2,700 vs. baseline 31.95). V5 froze the GPT-2 backbone, training only the 73K-parameter triadic head. Result: PPL = 31.95 (identical to baseline) at a cost of only −1.7% accuracy.

### 4.6 Relational Structure (Regla de Tres)

The model preserves proportional relationships between dual pairs:

| Analogy | Cosine | Bit Acc |
|---------|--------|---------|
| good:evil = truth:lie | 0.998 | 1.000 |
| creation:destruction = life:death | 0.998 | 1.000 |
| freedom:control = individual:collective | 0.995 | 0.986 |
| pleasure:pain = conscious:absent | 0.996 | 1.000 |
| union:separation = order:chaos | 0.997 | 1.000 |
| creation:destruction = union:separation | 0.997 | 1.000 |

Mean cosine: **0.996** — near-perfect relational structure.

### 4.7 Neural Probes

8 falsifiable questions were tested using reptimeline checkpoint analysis:

| Probe | Question | Result | p-value |
|-------|----------|--------|---------|
| Q1 | Layer order in representations? | **Null** | 0.713 |
| Q2 | Dual anti-correlation? | **5/13 significant** | < 0.018 (BH) |
| Q3 | DAG recovery? | **Above random** | 0.001 |
| Q5 | Phase transition? | **Yes, step 6000** | 0.0004 |
| Q4 | Triadic dependencies? | Null | 1.000 |
| Q6 | Unsupervised discovery? | Null | 1.000 |
| Q7 | Causal verification? | Null | 1.000 |

**Interpretation**: The model learns *relational* structure (analogies, some dual axes, DAG edges) but does not recover *ordinal* structure (layer ordering, ternary dependencies). This is consistent with the frozen-base design: the head projects semantics into bit space without restructuring the backbone's internal representations.

---

## 5. Discussion

### 5.1 What the Framework Claims

The Emergent Duality framework makes two testable claims:

1. **Structural claim**: 72 primitives connected by a specific DAG can classify concepts across any knowledge domain using a ternary (D/A/N) code.
2. **Ordering claim**: the 14 dualities emerge in a specific sequence dictated by algebraic dependency.

### 5.2 Evidence For

- **Structural claim**: supported. 8/8 positive domains achieve IDVS = 1.000, all exceeding the p99 null threshold (0.955). The negative control correctly fails. Permutation tests yield p = 0.0001 for all domains after Holm-Bonferroni correction.
- **Ordering claim**: partially supported. Bayesian comparison yields BF = 121.4 (decisive) against reversed ordering, but only weak evidence against Hegel (BF = 1.14) and Peirce (BF = 1.95). The neural model does not recover layer ordering (Q1, p = 0.71).

### 5.3 Honest Limitations

1. **Self-evaluated classifications**: All D-A-N assignments were made by the framework author. Inter-rater data exists for only 1/9 domains (Mathematics). The permutation tests validate internal consistency but not external agreement.
2. **Underpowered rank correlations**: With n = 7 (circle) or n = 14 (combined), Spearman correlations cannot achieve significance at α = 0.05 even for moderate effects.
3. **IDVS = 1.000 for all positives**: After reclassification (v1.1), all positive domains achieve perfect scores. This may reflect overfitting to the metric rather than genuine universality. The I2 null baseline mitigates but does not eliminate this concern.
4. **Neural probes**: 5/8 probes returned null results. The model learns surface relational structure but not deep algebraic properties.
5. **Scale-algebra tradeoff**: Larger models (355M) show lower subsumption rates (76.9%) than smaller ones (40M, 98.3%). The frozen-base approach trades some algebraic fidelity for language preservation.

---

## 6. Related Work

- **Wierzbicka (1996)**: Natural Semantic Metalanguage proposes ~65 universal primitives but lacks formal algebraic structure or computational validation.
- **ConceptNet (Speer et al., 2017)**: Large-scale knowledge graph with 34 relation types but no emergence hierarchy.
- **FrameNet (Baker et al., 1998)**: Frame-based semantics covering ~1,200 frames but domain-specific rather than universal.
- **Category theory approaches (Coecke et al., 2010)**: DisCoCat and related formalisms provide compositional semantics but do not address emergence ordering.

Our framework differs in proposing (a) a specific algebraic chain governing emergence, (b) empirical validation across 9 domains, and (c) neurosymbolic learnability from natural language.

---

## 7. Conclusion

We have presented a formal ontological framework of 14 fundamental dualities emerging across 6 algebraic layers, grounded in 72 semantic primitives. The framework achieves perfect IDVS scores across 8 disciplines while correctly rejecting a negative control, with statistical hardening via permutation tests, null baselines, and Bayesian model comparison. A neurosymbolic model (GPT-2 + triadic head) learns the proposed structure at 90.8% accuracy without degrading language ability, exhibiting near-perfect relational preservation (cosine 0.996).

The main open question is external validation: independent human evaluators must confirm the D-A-N classifications before universality claims can be considered robust. We release all data, scripts, and model code to enable replication.

---

## Appendix A: Notation

| Symbol | Meaning |
|--------|---------|
| D, A, N | Direct, Analogical, Null classification states |
| IDVS | Information Domain Validity Score |
| BF | Bayes Factor |
| PPL | Perplexity |
| iFSQ | Improved Finite Scalar Quantization |
| BH-FDR | Benjamini-Hochberg False Discovery Rate |
| SHD | Structural Hamming Distance |
| DAG | Directed Acyclic Graph |

## Appendix B: Pending Results

<!-- UPDATE THIS SECTION when the current test completes -->

**[PLACEHOLDER — V6 results]**

A v6 training run is currently executing. Update this section with:
- Accuracy, coherence, PPL
- Dual pair coherence (all 14 axes)
- Comparison table vs v5_frozen
- Any new neural probe results

---

## References

1. Wierzbicka, A. (1996). *Semantics: Primes and Universals*. Oxford University Press.
2. Speer, R., Chin, J., & Havasi, C. (2017). ConceptNet 5.5. *AAAI*.
3. Baker, C. F., Fillmore, C. J., & Lowe, J. B. (1998). The Berkeley FrameNet Project. *COLING-ACL*.
4. Coecke, B., Sadrzadeh, M., & Clark, S. (2010). Mathematical Foundations for a Compositional Distributional Model of Meaning. *Linguistic Analysis*.
5. Radford, A., Wu, J., Child, R., et al. (2019). Language Models are Unsupervised Multitask Learners. *OpenAI Technical Report*.
6. Benjamini, Y. & Hochberg, Y. (1995). Controlling the False Discovery Rate. *JRSS-B*.
7. Mentzer, F., et al. (2025). Finite Scalar Quantization: VQ-VAE Made Simple. *ICLR 2024*.
