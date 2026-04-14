"""
Correlación MA ~ omega: Assembly Theory meets Danza Cósmica
============================================================
Objetivo: Testear la conjetura de que el assembly index (MA) se correlaciona
con omega (número de "factores primos" irreducibles) de una molécula.

Operacionalizaciones de omega para moléculas:
  omega_elements: # de tipos de elementos distintos (C,H,O,N,S,Cl,...)
  omega_heavy:    # de tipos de elementos pesados (excl. H)
  n_heavy_atoms:  # total de átomos pesados
  n_elements_total: # total de átomos (todos)
  MW: peso molecular (control)
"""

import pandas as pd
import numpy as np
import re
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter

# ============================================================
# 1. Parse molecular formulas
# ============================================================

def parse_formula(formula_str):
    """Parse molecular formula like 'C19H17N5O7S3' into element counts."""
    if not formula_str or pd.isna(formula_str):
        return {}
    formula_str = str(formula_str).strip()
    # Pattern: element symbol (1 uppercase + 0-1 lowercase) + optional count
    pattern = r'([A-Z][a-z]?)(\d*)'
    elements = {}
    for match in re.finditer(pattern, formula_str):
        elem = match.group(1)
        count = int(match.group(2)) if match.group(2) else 1
        if elem:  # skip empty matches
            elements[elem] = elements.get(elem, 0) + count
    return elements

def formula_from_inchi(inchi_str):
    """Extract molecular formula from InChI string."""
    if not inchi_str or pd.isna(inchi_str):
        return ""
    # InChI=1S/C23H29N5O5/... -> C23H29N5O5
    parts = str(inchi_str).split('/')
    if len(parts) >= 2:
        return parts[1]
    return ""

def compute_omega_metrics(elements):
    """Compute different omega operationalizations from element dict."""
    if not elements:
        return {'omega_elements': 0, 'omega_heavy': 0, 'n_heavy_atoms': 0, 'n_atoms_total': 0}

    omega_elements = len(elements)  # distinct element types
    omega_heavy = len([e for e in elements if e != 'H'])  # distinct heavy elements
    n_heavy_atoms = sum(v for k, v in elements.items() if k != 'H')  # total heavy atoms
    n_atoms_total = sum(elements.values())  # all atoms

    return {
        'omega_elements': omega_elements,
        'omega_heavy': omega_heavy,
        'n_heavy_atoms': n_heavy_atoms,
        'n_atoms_total': n_atoms_total
    }

# ============================================================
# 2. Load and process Dataset 2 (experimental MA, ~101 molecules)
# ============================================================
print("=" * 60)
print("DATASET 2: Experimental MA (Sharma et al.)")
print("=" * 60)

df2 = pd.read_csv('dataset_2_experimental_MA_450.csv')
print(f"Rows: {len(df2)}, Unique molecules (by CAS): {df2['CAS'].nunique()}")

# Parse formulas and compute omega
metrics_list = []
for _, row in df2.iterrows():
    elements = parse_formula(row['formula'])
    m = compute_omega_metrics(elements)
    m['MA'] = row['MA']
    m['MW'] = row['MW']
    m['formula'] = row['formula']
    m['CAS'] = row['CAS']
    metrics_list.append(m)

df2_metrics = pd.DataFrame(metrics_list)

# Deduplicate by CAS (take first measurement for each molecule)
df2_unique = df2_metrics.drop_duplicates(subset='CAS', keep='first').copy()
print(f"Unique molecules for analysis: {len(df2_unique)}")

print(f"\nMA range: {df2_unique['MA'].min()} - {df2_unique['MA'].max()}, mean: {df2_unique['MA'].mean():.1f}")
print(f"omega_elements range: {df2_unique['omega_elements'].min()} - {df2_unique['omega_elements'].max()}, mean: {df2_unique['omega_elements'].mean():.1f}")
print(f"omega_heavy range: {df2_unique['omega_heavy'].min()} - {df2_unique['omega_heavy'].max()}, mean: {df2_unique['omega_heavy'].mean():.1f}")
print(f"n_heavy_atoms range: {df2_unique['n_heavy_atoms'].min()} - {df2_unique['n_heavy_atoms'].max()}, mean: {df2_unique['n_heavy_atoms'].mean():.1f}")

# ============================================================
# 3. Load and process Dataset 1 (calculated MA, 10,000 molecules)
# ============================================================
print("\n" + "=" * 60)
print("DATASET 1: Calculated MA (10,000 molecules)")
print("=" * 60)

df1 = pd.read_csv('dataset_1_calculated_MA_10000.csv')
print(f"Rows: {len(df1)}")

metrics_list_1 = []
for _, row in df1.iterrows():
    formula = formula_from_inchi(row['InChI'])
    elements = parse_formula(formula)
    m = compute_omega_metrics(elements)
    m['MA'] = row['MA']
    m['formula'] = formula
    metrics_list_1.append(m)

df1_metrics = pd.DataFrame(metrics_list_1)
# Filter out any rows where parsing failed
df1_metrics = df1_metrics[df1_metrics['omega_elements'] > 0].copy()
print(f"Parsed successfully: {len(df1_metrics)}")

print(f"\nMA range: {df1_metrics['MA'].min()} - {df1_metrics['MA'].max()}, mean: {df1_metrics['MA'].mean():.1f}")
print(f"omega_elements range: {df1_metrics['omega_elements'].min()} - {df1_metrics['omega_elements'].max()}, mean: {df1_metrics['omega_elements'].mean():.1f}")
print(f"omega_heavy range: {df1_metrics['omega_heavy'].min()} - {df1_metrics['omega_heavy'].max()}, mean: {df1_metrics['omega_heavy'].mean():.1f}")
print(f"n_heavy_atoms range: {df1_metrics['n_heavy_atoms'].min()} - {df1_metrics['n_heavy_atoms'].max()}, mean: {df1_metrics['n_heavy_atoms'].mean():.1f}")

# ============================================================
# 4. Correlation Analysis
# ============================================================

def run_correlations(df, dataset_name, omega_cols, y_col='MA'):
    """Run Pearson and Spearman correlations for multiple omega definitions."""
    print(f"\n{'-' * 50}")
    print(f"CORRELACIONES: {dataset_name}")
    print(f"{'-' * 50}")
    print(f"{'Variable':<20} {'Pearson r':>10} {'p-value':>12} {'Spearman rho':>12} {'p-value':>12}")
    print(f"{'-' * 66}")

    results = {}
    for col in omega_cols:
        x = df[col].values
        y = df[y_col].values

        # Remove NaN
        mask = ~(np.isnan(x) | np.isnan(y))
        x, y = x[mask], y[mask]

        if len(x) < 3:
            continue

        r_pearson, p_pearson = stats.pearsonr(x, y)
        r_spearman, p_spearman = stats.spearmanr(x, y)

        sig_p = '***' if p_pearson < 0.001 else '**' if p_pearson < 0.01 else '*' if p_pearson < 0.05 else ''
        sig_s = '***' if p_spearman < 0.001 else '**' if p_spearman < 0.01 else '*' if p_spearman < 0.05 else ''

        print(f"{col:<20} {r_pearson:>9.4f}{sig_p:<3} {p_pearson:>12.2e} {r_spearman:>9.4f}{sig_s:<3} {p_spearman:>12.2e}")
        results[col] = {'pearson_r': r_pearson, 'pearson_p': p_pearson,
                        'spearman_r': r_spearman, 'spearman_p': p_spearman, 'n': len(x)}

    return results

# Dataset 2 correlations
omega_cols_2 = ['omega_elements', 'omega_heavy', 'n_heavy_atoms', 'n_atoms_total', 'MW']
results_2 = run_correlations(df2_unique, "Dataset 2 (Experimental, N={})".format(len(df2_unique)), omega_cols_2)

# Dataset 1 correlations
omega_cols_1 = ['omega_elements', 'omega_heavy', 'n_heavy_atoms', 'n_atoms_total']
results_1 = run_correlations(df1_metrics, "Dataset 1 (Calculado, N={})".format(len(df1_metrics)), omega_cols_1)

# ============================================================
# 5. Binned analysis: mean MA per omega value
# ============================================================
print("\n" + "=" * 60)
print("ANALISIS POR BINS: MA medio por omega_elements")
print("=" * 60)

for name, df in [("Dataset 1 (N=10000)", df1_metrics), ("Dataset 2 (N~101)", df2_unique)]:
    print(f"\n{name}:")
    print(f"{'omega_elements':<16} {'N':>6} {'MA mean':>10} {'MA std':>10} {'MA min':>8} {'MA max':>8}")
    grouped = df.groupby('omega_elements')['MA'].agg(['count', 'mean', 'std', 'min', 'max'])
    for omega_val, row in grouped.iterrows():
        print(f"{omega_val:<16} {int(row['count']):>6} {row['mean']:>10.2f} {row['std']:>10.2f} {row['min']:>8.1f} {row['max']:>8.1f}")

# ============================================================
# 6. Scatter plots
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('MA ~ omega Correlations: Assembly Theory <-> Danza Cosmica', fontsize=14, fontweight='bold')

# Dataset 1 plots
for i, col in enumerate(['omega_elements', 'omega_heavy', 'n_heavy_atoms']):
    ax = axes[0, i]
    x = df1_metrics[col].values
    y = df1_metrics['MA'].values

    # Jitter for discrete variables
    if col in ['omega_elements', 'omega_heavy']:
        x_plot = x + np.random.normal(0, 0.1, len(x))
    else:
        x_plot = x

    ax.scatter(x_plot, y, alpha=0.05, s=5, color='steelblue')

    # Regression line
    mask = ~(np.isnan(x) | np.isnan(y))
    z = np.polyfit(x[mask], y[mask], 1)
    p = np.poly1d(z)
    x_range = np.linspace(x[mask].min(), x[mask].max(), 100)
    ax.plot(x_range, p(x_range), 'r-', linewidth=2)

    r, pval = stats.pearsonr(x[mask], y[mask])
    rho, pval_s = stats.spearmanr(x[mask], y[mask])
    ax.set_title(f'Dataset 1: MA vs {col}\nr={r:.3f}, rho={rho:.3f}')
    ax.set_xlabel(col)
    ax.set_ylabel('MA (calculated)')

    # Mean line per bin
    means = df1_metrics.groupby(col)['MA'].mean()
    ax.plot(means.index, means.values, 'ko-', markersize=6, linewidth=2, label='mean MA')
    ax.legend()

# Dataset 2 plots
for i, col in enumerate(['omega_elements', 'omega_heavy', 'n_heavy_atoms']):
    ax = axes[1, i]
    x = df2_unique[col].values
    y = df2_unique['MA'].values

    if col in ['omega_elements', 'omega_heavy']:
        x_plot = x + np.random.normal(0, 0.08, len(x))
    else:
        x_plot = x

    ax.scatter(x_plot, y, alpha=0.5, s=30, color='darkorange')

    mask = ~(np.isnan(x) | np.isnan(y))
    z = np.polyfit(x[mask], y[mask], 1)
    p = np.poly1d(z)
    x_range = np.linspace(x[mask].min(), x[mask].max(), 100)
    ax.plot(x_range, p(x_range), 'r-', linewidth=2)

    r, pval = stats.pearsonr(x[mask], y[mask])
    rho, pval_s = stats.spearmanr(x[mask], y[mask])
    ax.set_title(f'Dataset 2: MA vs {col}\nr={r:.3f}, rho={rho:.3f}')
    ax.set_xlabel(col)
    ax.set_ylabel('MA (experimental)')

    means = df2_unique.groupby(col)['MA'].mean()
    ax.plot(means.index, means.values, 'ko-', markersize=6, linewidth=2, label='mean MA')
    ax.legend()

plt.tight_layout()
plt.savefig('correlacion_MA_omega.png', dpi=150, bbox_inches='tight')
print(f"\nGrafica guardada: correlacion_MA_omega.png")

# ============================================================
# 7. Partial correlation: omega_elements controlling for n_heavy_atoms
# ============================================================
print("\n" + "=" * 60)
print("CORRELACION PARCIAL: omega_elements -> MA, controlando n_heavy_atoms")
print("=" * 60)

def partial_correlation(x, y, z):
    """Partial correlation of x and y, controlling for z."""
    # Residualize x on z
    slope_xz, intercept_xz, _, _, _ = stats.linregress(z, x)
    x_resid = x - (slope_xz * z + intercept_xz)
    # Residualize y on z
    slope_yz, intercept_yz, _, _, _ = stats.linregress(z, y)
    y_resid = y - (slope_yz * z + intercept_yz)
    # Correlate residuals
    return stats.pearsonr(x_resid, y_resid)

for name, df in [("Dataset 1", df1_metrics), ("Dataset 2", df2_unique)]:
    mask = ~(df['omega_elements'].isna() | df['MA'].isna() | df['n_heavy_atoms'].isna())
    x = df.loc[mask, 'omega_elements'].values.astype(float)
    y = df.loc[mask, 'MA'].values.astype(float)
    z = df.loc[mask, 'n_heavy_atoms'].values.astype(float)

    r_partial, p_partial = partial_correlation(x, y, z)
    print(f"\n{name} (N={len(x)}):")
    print(f"  r_parcial(omega_elements, MA | n_heavy_atoms) = {r_partial:.4f}, p = {p_partial:.2e}")

    # Also: omega_heavy controlling for n_heavy_atoms
    x2 = df.loc[mask, 'omega_heavy'].values.astype(float)
    r_partial2, p_partial2 = partial_correlation(x2, y, z)
    print(f"  r_parcial(omega_heavy, MA | n_heavy_atoms) = {r_partial2:.4f}, p = {p_partial2:.2e}")

# ============================================================
# 8. Summary and interpretation
# ============================================================
print("\n" + "=" * 60)
print("RESUMEN E INTERPRETACION")
print("=" * 60)
print("""
La conjetura de la Danza Cosmica predice: MA(x) ~ omega(x)
donde omega = numero de "primos" irreducibles.

Para moleculas, omega se operacionaliza como:
  - omega_elements: tipos de elementos distintos (cada elemento = un "primo")
  - omega_heavy: idem sin contar H

La pregunta es: el assembly index de una molecula se correlaciona
con su diversidad elemental (omega), mas alla del simple tamano?

Si r(MA, omega) > 0 y la correlacion parcial controlando tamano
sigue siendo significativa -> evidencia a favor de la conjetura.
Si r(MA, omega) ~ 0 o la correlacion parcial desaparece -> la relacion
es espuria (ambos crecen con el tamano molecular).
""")
