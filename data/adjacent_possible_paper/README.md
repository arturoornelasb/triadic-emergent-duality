# Supplementary Data: Adjacent Possible Paper

Reproducible analyses and supplementary material for two papers:

> Ornelas Brand, J. A. (2026). *Duality Synthesis in Quaternionic Logic: How Opposites Generate Truth* (v0.1.0). Zenodo. https://doi.org/10.5281/zenodo.19561634
> — uses the MA ~ omega correlation results below. Paper source (`duality_synthesis.tex`) and compiled PDF (`duality_synthesis.pdf`) included in this folder.

> Ornelas Brand, J. A. (2026). *Pre-Logical States and the Birth of Information: How Reasoning Operates Before Truth Exists* (v0.1.0). Zenodo. https://doi.org/10.5281/zenodo.19561722
> — uses the Zipf's Law / adjacent possible lattice analyses below. Paper source (`pre_logical_states.tex`) and compiled PDF (`pre_logical_states.pdf`) included in this folder.

## Contents

### Zipf's Law on the Prime Lattice

Demonstrates that Polya-like reinforced random walks on the Boolean lattice of squarefree products reproduce Zipf and Heaps scaling laws.

| File | Description |
|------|-------------|
| `zipf_prime_lattice.py` | Simulation: 500 walks x 10,000 steps on 2^20 lattice, sweep over rho and dynamics |
| `results_table.csv` | Summary table: alpha, R2, beta for each (model, rho) combination |
| `zipf_additive.png` | Rank-frequency plots for additive dynamics |
| `zipf_toggle.png` | Rank-frequency plots for toggle dynamics |
| `zipf_comparison.png` | Side-by-side comparison |
| `heaps_law.png` | Heaps' law (unique nodes vs steps) |
| `zipf_paragraph.tex` | Pre-written LaTeX paragraph summarizing results |

**Key result:** Additive model with rho=5.0 produces near-exact Zipf (alpha=0.995, R2=0.966).

### MA ~ omega Correlation (Assembly Theory)

Tests whether the structural parallel between assembly index (MA) and prime factor count (omega) extends to numerical correlation on shared objects (molecules).

| File | Description |
|------|-------------|
| `correlacion_MA_omega.py` | Full analysis: formula parsing, Pearson/Spearman/partial correlations, bin means, plots |
| `correlacion_MA_omega.png` | 6 scatter plots (2 datasets x 3 variables) with regressions |
| `RESUMEN_CORRELACION_MA_OMEGA.md` | Detailed results summary (in Spanish) |
| `dataset_1_calculated_MA_10000.csv` | 10,000 molecules with calculated MA (from Sharma et al. 2023) |
| `dataset_2_experimental_MA_450.csv` | 101 unique molecules with experimentally measured MA |

**Key result:** Partial correlation r=0.52-0.57 (p < 10^-10) controlling for molecular size. Element-type diversity (number of distinct chemical elements) used as conservative proxy for omega.

**Data source:** Sharma, A. et al. (2023). Assembly theory explains and quantifies selection and evolution. *Nature*, 622, 321-328. Data extracted from [croningp/molecular_complexity](https://github.com/croningp/molecular_complexity).

## How to run

```bash
# Zipf simulation (no dependencies beyond numpy/scipy/matplotlib)
python zipf_prime_lattice.py

# MA-omega correlation (requires pandas, scipy, matplotlib)
python correlacion_MA_omega.py
```
