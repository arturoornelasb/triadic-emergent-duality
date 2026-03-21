# dualidademergente + reptimeline

Statistical hardening and neural probe suite for the dualidad_emergente framework.

## Structure

```
stats/          Pure-stdlib statistical toolkit (no numpy/scipy)
  bh_fdr.py       Benjamini-Hochberg FDR + Holm-Bonferroni
  bootstrap.py    Bootstrap confidence intervals
  permutation.py  Permutation tests
  effect_size.py  Cohen's d, selectivity ratio
  power_analysis.py  Simulation-based power analysis
  registry.py     Central p-value registry

internal/       Self-auditing analyses (no neural model needed)
  i1_recalc_pvalues.py     FDR correction of all reported p-values
  i2_null_baseline_idvs.py Permutation null for IDVS threshold
  i3_sensitivity.py        Perturbation robustness analysis
  i4_bayesian_orders.py    Bayes factor comparison of orderings
  i5_discrepancia_65_63.py Identify 65-vs-63 bit discrepancy

neural/         Neural probes (require reptimeline + trained model)
  q1-q8           Eight probe scripts, one per research question
  interpret.py    Consolidator for all probe results
```

## Quick start

```bash
cd dualidademergente+reptimeline

# Internal analyses (stdlib only, no dependencies)
python internal/i1_recalc_pvalues.py
python internal/i2_null_baseline_idvs.py
python internal/i3_sensitivity.py
python internal/i4_bayesian_orders.py
python internal/i5_discrepancia_65_63.py

# Neural probes (need: pip install reptimeline)
python neural/q1_probe_layer_order.py --checkpoints <dir>
# ...
python neural/interpret.py  # consolidate all results
```

## Key findings from internal analyses

**I1 — p-value recalculation:**
0/12 Spearman correlations survive BH-FDR correction.
8/8 permutation tests (anchor consistency) survive Holm-Bonferroni.
The rank correlations from Doc 34/35 are underpowered (n=7/14).

**I2 — IDVS null baseline:**
The 0.80 threshold is within the null distribution (78.4% of random assignments achieve it).
Recommended threshold: 0.90 (p95 of null = 0.896).
5/8 domains exceed p95: Chemistry, Biology, Music, Linguistics, Psychology.
3/8 within null: Philosophy, Physics, Mathematics.

**I3 — Sensitivity:**
DAG structure is robust (removing one edge: mean delta = -0.003).
Layer assignments have zero effect on triangularity.
D-A-N classifications are fragile (28.4% of 5% flips cause >5% IDVS change).

**I4 — Bayesian ordering:**
M_teo vs reversed: BF = 121.4 (decisive).
M_teo vs random: p = 0.005 (only 4/1000 match or exceed).
M_teo vs Hegel: BF = 1.1 (indistinguishable).
M_teo vs Peirce: BF = 1.9 (indistinguishable).

**I5 — 65 vs 63:**
`proporcion` (bit 63) and `quietud` (bit 64) are outside the 63-bit code.

## Epistemic framework

The neural probes (Q1-Q8) are structured as questions, not confirmations.
Every positive result is reported alongside its most probable confounder.
A coincidence between model and theory does NOT prove the theory —
it could reflect shared training-data bias or low test specificity.
A divergence does NOT falsify the theory —
the model may simply not be expressive enough for the structure.

## Dependencies

- **Internal analyses**: Python 3.8+ with stdlib only
- **Neural probes**: `pip install reptimeline` + trained TriadicGPT checkpoints
- **Data**: `../../data/` must contain `primitivos.json`, `dualidad_primitivo_map.json`, `reference_domains.json`
