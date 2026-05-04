# Roadmap: Triadic Emergent Duality

Status snapshot as of 2026-03-25. Items reflect actual repository state.

---

## Technical

### Done (no work required)

- [x] 23 theory documents (~44,000 words) covering formal definitions, philosophical precedents, and empirical tests
- [x] 32 validation scripts across 9 domains
- [x] GPT-2 Medium + 72-bit triadic head trained (v5_frozen: PPL 31.95, 90.8% accuracy, 100% unique)
- [x] V6 extended corpus training (2,166 concepts, 80.9% accuracy, 48 active bits, PPL 31.95)
- [x] reptimeline deep analysis on v6 (20 checkpoints, phase dashboard, swimlane, churn heatmap, layer emergence)
- [x] `requirements.txt` with pinned dependencies
- [x] `LICENSE` file (BUSL-1.1 with consortium model)
- [x] TERMS.md and COMMERCIAL.md for contribution obligations
- [x] reptimeline integration for training dynamics analysis
- [x] Paper compiled (LaTeX, 9 pages) with v6 results
- [x] 6 training runs documented (v1-v6) with full experiment log
- [x] Inter-rater reliability data (Mathematics domain)
- [x] Algebraic layer verification (86% match across 6 algebras)
- [x] Companion papers published on Zenodo (Triadic Engine, reptimeline, triadic-microgpt)
- [x] `domain_validity_score.py` synced with `reference_domains.json` (no more hardcoded D-A-N)
- [x] Paper and README corrected: p95=0.931, all 8 Regla de Tres quadruples, duality table aligned
- [x] **Q13 algebraic Markov blanket** — verified PASS 100% on v8 and v9 (500K pairs each, 0 violations) — confirms FTA-guaranteed gcd(μ₁,μ₂)=1 implementation
- [x] **Q13 MI probe** — v8 NEGATIVE / v9 MIXED (T2 layer hierarchy passes, T4 partial-correlation fails)
- [x] **Q15 quaternionic coordinates** — (r,i,j,k) assigned to 72 primitives for v8 and v9
- [x] **Q18 quaternionic product** — VERIFIED (T1–T7: closure, associativity, inverses, ij=k, non-commutativity, layer recovery, 14 dual products)
- [x] **Q32 inter-rater (model vs human)** — Cohen's κ computed for 8 domains; all in slight-to-poor range (κ ∈ [-0.082, 0.111]); does NOT substitute for K2 human-vs-human
- [x] **D15 formal proposal** — `docs/teoria/37_operador_capa6_D15.md`: layer-6 internal operator (Collapse/Superposition) closing the symmetric pattern 1,1,2,2,1,1
- [x] Two new companion papers published on Zenodo (Apr 13, 2026): *Duality Synthesis in Quaternionic Logic* (DOI 10.5281/zenodo.19561634) and *Pre-Logical States and the Birth of Information* (DOI 10.5281/zenodo.19561722)

### Pending — High Priority

- [ ] **CI/CD** — No GitHub Actions. Minimum: lint + validation script runner on push.
- [ ] **Complete K2 human-vs-human inter-rater data** — Only Mathematics_rater2.csv exists. Need remaining 8 domains for full external verification. Note: Q32 model-vs-human is computed for 8 domains but does NOT substitute for K2 (κ ≤ 0.11 across all domains shows the trained model does not recover expert classifications).
- [ ] **Publish model weights** — v5_frozen and v6 checkpoints not publicly available. Options: GitHub Releases or HuggingFace Hub.
- [ ] **Rerun neural probes Q1-Q8 with v6 model** — Current results computed with 65-bit v2/v3 model, not current 72-bit.

### Pending — Medium Priority

- [ ] **Scale-algebra tradeoff** — GPT-2 355M achieves 76.9% subsumption vs 98.3% at 40M. Cause under investigation.
- [ ] **Docker environment** — For reproducible GPU training.
- [ ] **Translate theory docs to English** — 23 documents currently in Spanish. At minimum, translate abstracts/summaries.
- [ ] **Generate DAG/spiral figures** — `figures/` directory does not exist. Need DAG visualization, spiral diagram, per-domain results. reptimeline plots exist in `runs/v6/plots/`.

### Pending — Low Priority

- [ ] **REST API / CLI** — For querying primitives of a given concept.
- [ ] **pip-installable package** — `pip install triadic-emergent-duality`.
- [ ] **Technical documentation site** — Sphinx or MkDocs.

---

## Commercial

### Assets Ready

- **Paper** — 9-page LaTeX, compiled PDF, with v5 and v6 results.
- **Framework** — 72 semantic primitives, 6 algebraic layers, 14 dualities. Validated across 9 disciplines.
- **Model** — GPT-2 Medium + 72-bit triadic head. v5_frozen (72 prims) + v6 (2,166 concepts). Catastrophic forgetting solved.
- **License** — BUSL-1.1 with consortium model. Free for individuals/academia/nonprofits. Companies must participate.
- **Companion papers** — Triadic Engine, reptimeline, triadic-microgpt all on Zenodo with DOIs.

### Pending — Monetization

- [ ] **Zenodo DOI for this repo** — Required before any other publication step.
- [ ] **Benchmarks vs alternatives** — Compare against ConceptNet, FrameNet, WordNet for positioning.
- [ ] **Concrete use case demo** — NLP, ontology engineering, knowledge graphs, or curriculum design.
- [ ] **Landing page** — Interactive demo (input concept, output vector + active dualities).

---

## Blockers

| Blocker | Severity | Impact |
|---------|----------|--------|
| No published model weights | High | Results not reproducible by third parties |
| Inter-rater data incomplete (1/9 domains) | High | IDVS metric not externally verifiable for 8 domains |
| Neural probes Q1-Q8 from 65-bit model | Medium | Probe results do not reflect current 72-bit architecture |
| Underpowered statistics (n=7/14) | High | Peer reviewers may reject ordering claims without more evidence |
| No peer review | Medium | All results are self-reported |
| Theory docs in Spanish only | Medium | Limits international audience |
