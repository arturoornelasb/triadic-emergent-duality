# Roadmap: Triadic Emergent Duality

Status snapshot as of 2026-03-24. Items reflect actual repository state.

---

## Technical

### Done (no work required)

- [x] 37 theory documents (~44,000 words) covering formal definitions, philosophical precedents, and empirical tests
- [x] 32 validation scripts across 9 domains
- [x] GPT-2 Medium + 72-bit triadic head trained (v5_frozen: PPL 31.95, 90.8% accuracy, 100% unique)
- [x] `requirements.txt` with pinned dependencies
- [x] `LICENSE` file (BUSL-1.1 with consortium model)
- [x] TERMS.md and COMMERCIAL.md for contribution obligations
- [x] reptimeline integration for training dynamics analysis
- [x] Paper compiled (LaTeX, 7 pages)
- [x] 5 training runs documented (v1-v5) with full experiment log
- [x] Inter-rater reliability data (Mathematics domain)
- [x] Algebraic layer verification (86% match across 6 algebras)

### Pending — High Priority

- [ ] **Publish paper on Zenodo** — PDF compiled, needs DOI. Independent researcher without institutional affiliation (no arXiv access).
- [ ] **CI/CD** — No GitHub Actions. Minimum: lint + validation script runner on push.
- [ ] **Complete inter-rater data** — Only Mathematics_rater2.csv exists. Need remaining 8 domains for full external verification.
- [ ] **Publish model weights** — v5_frozen checkpoint not publicly available. Options: GitHub Releases or HuggingFace Hub.

### Pending — Medium Priority

- [ ] **Scale-algebra tradeoff** — GPT-2 355M achieves 76.9% subsumption vs 98.3% at 40M. Cause under investigation.
- [ ] **Docker environment** — For reproducible GPU training.
- [ ] **Translate theory docs to English** — 37 documents currently in Spanish. At minimum, translate abstracts/summaries.
- [ ] **Generate figures** — `figures/` directory empty. Need DAG, spiral, and per-domain result visualizations.

### Pending — Low Priority

- [ ] **REST API / CLI** — For querying primitives of a given concept.
- [ ] **pip-installable package** — `pip install triadic-emergent-duality`.
- [ ] **Technical documentation site** — Sphinx or MkDocs. Currently only the 37 theory .md files.

---

## Commercial

### Assets Ready

- **Paper** — 7-page LaTeX, compiled PDF, ready for Zenodo.
- **Framework** — 72 semantic primitives, 6 algebraic layers, 14 dualities. Validated across 9 disciplines.
- **Model** — GPT-2 Medium + 72-bit triadic head (v5_frozen). Catastrophic forgetting solved.
- **License** — BUSL-1.1 with consortium model. Free for individuals/academia/nonprofits. Companies must participate.

### Pending — Monetization

- [ ] **Zenodo DOI** — Required before any other publication step.
- [ ] **Benchmarks vs alternatives** — Compare against ConceptNet, FrameNet, WordNet for positioning.
- [ ] **Concrete use case demo** — NLP, ontology engineering, knowledge graphs, or curriculum design.
- [ ] **Landing page** — Interactive demo (input concept, output vector + active dualities).

---

## Blockers

| Blocker | Severity | Impact |
|---------|----------|--------|
| No published model weights | High | Results not reproducible by third parties |
| Inter-rater data incomplete (1/9 domains) | High | IDVS metric not externally verifiable for 8 domains |
| Underpowered statistics (n=7/14) | High | Peer reviewers may reject ordering claims without more evidence |
| 3 domains within null distribution | Medium | Weakens universal validation claim |
| No peer review | Medium | All results are self-reported |
| Theory docs in Spanish only | Medium | Limits international audience |
