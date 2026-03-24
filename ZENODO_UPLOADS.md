# Zenodo Upload Guide — 4 Papers

Upload each paper manually at https://zenodo.org/uploads/new
Upload ONLY the PDF. Set type as Publication → Preprint.

After all 4 have DOIs, come back and add `related_identifiers` to link them.

---

## Paper 1: Triadic Engine (Foundation)

**File to upload:** `Triadic-Neurosymbolic-Engine/paper/PrimeFactorization_NeurosymbolicBridge_OrnelasBrand_2026.pdf`

> NOTE: This paper already has a Zenodo DOI from a previous version. Go to the existing record and click "New version" instead of creating a new upload.

- **Upload type:** Publication → Preprint
- **Title:** Prime Factorization as a Neurosymbolic Bridge: Projecting Continuous Embeddings into Discrete Algebraic Space for Deterministic Verification
- **Authors:** Ornelas Brand, J. Arturo — Independent Researcher — arturoornelas62@gmail.com
- **Description/Abstract:** We propose a method for bridging continuous neural embeddings and discrete symbolic reasoning by mapping dense vectors to composite prime integers via Locality Sensitive Hashing (LSH), effectively enabling exact set operations on LSH signatures via unique factorization. Each LSH hyperplane is assigned a unique prime; a concept's integer is the product of primes for its active hyperplanes. This encoding yields three algebraic operations impossible under cosine similarity or Hamming distance: (1) logical subsumption via divisibility, (2) concept composition via LCM, and (3) abductive gap analysis via GCD factorization. We benchmark on a 107-word vocabulary across a series of 9 experiments, achieving 28.4x faster pairwise verification than cosine similarity, and provide honest analysis of limitations.
- **License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)
- **Publication date:** 2026-03-24
- **Language:** English
- **Keywords:** neurosymbolic AI, prime factorization, LSH, discrete reasoning, algebraic verification, embeddings, explainable AI
- **Related identifiers (add AFTER all 4 papers have DOIs):**
  - `https://github.com/arturoornelasb/Triadic-Neurosymbolic-Engine` — isSupplementedBy — Software
  - Paper 2 DOI — isReferencedBy — Publication/Preprint
  - Paper 3 DOI — isReferencedBy — Publication/Preprint
  - Paper 4 DOI — isReferencedBy — Publication/Preprint

---

## Paper 2: TriadicGPT / MicroGPT (End-to-End Learning)

**File to upload:** `triadic-microgpt/paper/triadic_microgpt.pdf`

- **Upload type:** Publication → Preprint
- **Title:** End-to-End Prime Factorization in a Generative Language Model: Emergent Algebraic Semantics from Joint Training
- **Authors:** Ornelas Brand, J. Arturo — Independent Researcher — arturoornelas62@gmail.com
- **Description/Abstract:** We present TriadicGPT, a 40M-parameter GPT language model augmented with a triadic projection head that produces discrete prime-factor signatures alongside standard next-token predictions. Unlike the post-hoc approach of the Triadic-Neurosymbolic-Engine, which projects frozen sentence embeddings into prime composites, TriadicGPT learns triadic representations end-to-end through a dual-objective training loss combining language modeling with a novel embedding alignment objective. Across 29+ training runs and systematic ablation studies, we demonstrate eight principal findings: (1) the triadic head adds negligible cost to language quality (+1.7% perplexity); (2) semantic ordering emerges gradually with scale, crossing zero around 20M parameters; (3) a bits sweep reveals an optimal regime at k=32-64; (4) attaching the triadic head to pre-trained GPT-2 with InfoNCE alignment closes 48% of the gap to the Engine's post-hoc PCA projection; (5) a differentiable subsumption loss recovers 100% held-out subsumption at k=64; (6) an iFSQ activation resolves the subsumption-language tradeoff entirely; (7) compositional analysis reveals that the bit space functions as a computational substrate with sub-linear error accumulation; and (8) a discovery loop expanding from 50 hand-labeled anchors to 158 improves holdout accuracy from 87% to 93%. TriadicGPT achieves 98% analogy verification (50/51 analogies), 100% signature uniqueness, and reproducible semantic ordering (+0.038 +/- 0.005 gap, n=3, 95% CI positive).
- **License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)
- **Publication date:** 2026-03-24
- **Language:** English
- **Keywords:** neurosymbolic AI, prime factorization, language model, algebraic semantics, discrete representations, triadic projection, subsumption, iFSQ, GPT, embedding alignment
- **Related identifiers (add AFTER all 4 papers have DOIs):**
  - `https://github.com/arturoornelasb/triadic-microgpt` — isSupplementedBy — Software
  - Paper 1 DOI — references — Publication/Preprint
  - Paper 3 DOI — isReferencedBy — Publication/Preprint

---

## Paper 3: reptimeline (Observability)

**File to upload:** `reptimeline/paper/reptimeline.pdf`

- **Upload type:** Publication → Preprint
- **Title:** reptimeline: Tracking Discrete Representation Evolution During Neural Network Training
- **Authors:** Ornelas Brand, J. Arturo — Independent Researcher — arturoornelas62@gmail.com
- **Description/Abstract:** We present reptimeline, a Python library for tracking how discrete representations evolve during neural network training. Unlike scalar logging tools (WandB, TensorBoard) that report aggregate metrics, reptimeline tracks per-code lifecycle events: when concepts become distinguishable (births), when representations collapse (deaths), when relationships form between concept pairs (connections), and where phase transitions occur in training dynamics. The library additionally discovers what each code element encodes — anti-correlated pairs, dependency chains, and three-way AND-gate interactions — without requiring prior ontological knowledge. We validate reptimeline on three architecturally distinct backends: a 32-bit binary autoencoder on MNIST (decoder determinism verified: 100%), sparse autoencoder features on Pythia-70M (8/16 features with finite KL selectivity, mean 26.8x L2 ratio with bootstrap 95% CI, plus 8 features with zero cross-activation attributable to SAE sparsity), and a 63-bit neurosymbolic projection head (crystallization event invisible to loss curves). reptimeline is the only tool that combines lifecycle tracking, bottom-up feature discovery, auto-labeling, and causal verification in a single backend-agnostic package.
- **License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)
- **Publication date:** 2026-03-24
- **Language:** English
- **Keywords:** representation learning, discrete representations, interpretability, lifecycle tracking, phase transitions, training dynamics, sparse autoencoder, VQ-VAE
- **Related identifiers (add AFTER all 4 papers have DOIs):**
  - `https://github.com/arturoornelasb/reptimeline` — isSupplementedBy — Software
  - Paper 2 DOI — references — Publication/Preprint

---

## Paper 4: Emergent Duality (Ontological Theory)

**File to upload:** `dualidad_emergente/paper/triadic_duality.pdf`

- **Upload type:** Publication → Preprint
- **Title:** Emergent Duality: 14 Fundamental Dualities Across 6 Algebraic Layers, Validated by Domain Analysis and Neurosymbolic Learning
- **Authors:** Ornelas Brand, J. Arturo — Independent Researcher — arturoornelas62@gmail.com
- **Description/Abstract:** We present a formal ontological framework in which conceptual complexity emerges from 14 fundamental dualities organized across 6 algebraic layers (Boolean, Fuzzy, Ordinal, Modal, Trivalent, Probabilistic). The framework is grounded in 72 semantic primitives connected by a directed acyclic graph (DAG) of 133+ dependency edges. We validate the framework through three independent methodologies: (1) domain analysis across 9 disciplines using the Information Domain Validity Score (IDVS), achieving IDVS = 1.000 for all 8 positive domains against a null baseline (p95 = 0.896, permutation p = 0.0001); (2) Bayesian model comparison yielding a Bayes factor of 121.4 (decisive) for the proposed ordering over reversed alternatives; and (3) neurosymbolic learning via a GPT-2 Medium model augmented with a 72-bit triadic head, which learns the primitive structure at 90.8% bit accuracy while preserving general language ability (PPL = 31.95, identical to baseline). The learned representations exhibit near-perfect relational structure (Regla de Tres cosine = 0.996) and show a significant phase transition during training (p = 0.0004). We report both confirmatory and null results transparently.
- **License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)
- **Publication date:** 2026-03-24
- **Language:** English
- **Keywords:** ontology, semantic primitives, emergence, duality, neurosymbolic AI, algebraic structure, domain validation, Bayesian model comparison
- **Related identifiers (add AFTER all 4 papers have DOIs):**
  - `https://github.com/arturoornelasb/triadic-emergent-duality` — isSupplementedBy — Software
  - Paper 1 DOI — references — Publication/Preprint
  - Paper 2 DOI — references — Publication/Preprint
  - Paper 3 DOI — references — Publication/Preprint

---

## After All 4 Are Published

1. Go back to each record and add the `related_identifiers` linking to the other 3 DOIs
2. Update each repo's README with the Zenodo DOI badge
3. Update BibTeX citations in each paper with real DOIs
4. Update pyproject.toml `project.urls` with `Paper = "https://doi.org/10.5281/zenodo.XXXXXXX"`
5. Tag and publish triadic-head and reptimeline to PyPI

## Order of Upload

1. **Engine** first (update existing record — this is the foundation everything references)
2. **MicroGPT** second (references Engine)
3. **reptimeline** third (references MicroGPT)
4. **Emergent Duality** last (references all three)
