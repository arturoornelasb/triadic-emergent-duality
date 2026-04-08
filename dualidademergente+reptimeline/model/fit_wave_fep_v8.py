"""Fit damped oscillation (FEP wave) to v8 reptimeline entropy curve.

Same methodology as fit_wave_fep_v9.py but using v8 training log data.
Roadmap #12: compare wave vs exponential fit across architectures.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json

import numpy as np
from scipy.optimize import curve_fit, differential_evolution

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'neural', 'results'))


def damped_wave(t, A, d, f, phi, C):
    return A * np.exp(-d * t) * np.sin(2 * np.pi * f * t + phi) + C


def pure_exponential(t, A, d, C):
    return A * np.exp(-d * t) + C


def regime(d, f):
    w = 2 * np.pi * f
    ratio = d / w if w > 1e-10 else float('inf')
    if ratio < 0.9:
        return 'underdamped', ratio
    elif ratio < 1.1:
        return 'critical', ratio
    else:
        return 'overdamped', ratio


def fit_models(steps, entropy):
    t = np.array(steps, dtype=float)
    y = np.array(entropy, dtype=float)
    t_norm = (t - t[0]) / (t[-1] - t[0]) if t[-1] > t[0] else t

    results = {}
    ss_tot = np.sum((y - np.mean(y)) ** 2)

    # --- Damped wave fit ---
    bounds_wave = ([
        -1.0, 0.0, 0.01, -np.pi, 0.0,
    ], [
        1.0, 50.0, 20.0, np.pi, 1.0,
    ])

    try:
        def neg_r2_wave(params):
            yhat = damped_wave(t_norm, *params)
            ss_res = np.sum((y - yhat) ** 2)
            return ss_res / ss_tot

        de_bounds = list(zip(bounds_wave[0], bounds_wave[1]))
        de_result = differential_evolution(neg_r2_wave, de_bounds, seed=42,
                                           maxiter=1000, tol=1e-10)
        p0_wave = de_result.x

        popt_w, pcov_w = curve_fit(damped_wave, t_norm, y, p0=p0_wave,
                                   bounds=bounds_wave, maxfev=50000)
        yhat_w = damped_wave(t_norm, *popt_w)
        ss_res_w = np.sum((y - yhat_w) ** 2)
        r2_w = 1 - ss_res_w / ss_tot
        aic_w = len(y) * np.log(ss_res_w / len(y)) + 2 * 5

        reg_name, reg_ratio = regime(popt_w[1], popt_w[2])

        results['wave'] = {
            'params': {'A': popt_w[0], 'd': popt_w[1], 'f': popt_w[2],
                       'phi': popt_w[3], 'C': popt_w[4]},
            'R2': r2_w, 'AIC': aic_w,
            'regime': reg_name, 'damping_ratio': reg_ratio,
            'residuals_std': np.std(y - yhat_w),
        }
        print(f'  Wave fit: R2={r2_w:.6f}, regime={reg_name} (d/w={reg_ratio:.3f})')
        print(f'    A={popt_w[0]:.4f}, d={popt_w[1]:.4f}, f={popt_w[2]:.4f}, '
              f'phi={popt_w[3]:.4f}, C={popt_w[4]:.4f}')
    except Exception as e:
        print(f'  Wave fit FAILED: {e}')
        results['wave'] = {'error': str(e)}

    # --- Pure exponential fit ---
    try:
        popt_e, pcov_e = curve_fit(pure_exponential, t_norm, y,
                                   p0=[0.3, 2.0, np.mean(y[-3:])],
                                   bounds=([-1, 0, 0], [1, 50, 1]),
                                   maxfev=50000)
        yhat_e = pure_exponential(t_norm, *popt_e)
        ss_res_e = np.sum((y - yhat_e) ** 2)
        r2_e = 1 - ss_res_e / ss_tot
        aic_e = len(y) * np.log(ss_res_e / len(y)) + 2 * 3

        results['exponential'] = {
            'params': {'A': popt_e[0], 'd': popt_e[1], 'C': popt_e[2]},
            'R2': r2_e, 'AIC': aic_e,
            'residuals_std': np.std(y - yhat_e),
        }
        print(f'  Exp  fit: R2={r2_e:.6f}')
        print(f'    A={popt_e[0]:.4f}, d={popt_e[1]:.4f}, C={popt_e[2]:.4f}')
    except Exception as e:
        print(f'  Exp fit FAILED: {e}')
        results['exponential'] = {'error': str(e)}

    # --- Model comparison ---
    if 'R2' in results.get('wave', {}) and 'R2' in results.get('exponential', {}):
        delta_aic = results['exponential']['AIC'] - results['wave']['AIC']
        results['comparison'] = {
            'delta_AIC': delta_aic,
            'preferred': 'wave' if delta_aic > 2 else ('exponential' if delta_aic < -2 else 'inconclusive'),
            'genuine_oscillation': results['wave']['params']['f'] > 0.5 and delta_aic > 2,
        }
        print(f'\n  Delta AIC (exp - wave) = {delta_aic:.2f}')
        print(f'  Preferred model: {results["comparison"]["preferred"]}')
        print(f'  Genuine oscillation: {results["comparison"]["genuine_oscillation"]}')

    # --- Bootstrap CI ---
    if 'params' in results.get('wave', {}):
        print('\n  Bootstrap CI (1000 resamples)...')
        rng = np.random.RandomState(42)
        n_boot = 1000
        boot_params = {k: [] for k in ['A', 'd', 'f', 'phi', 'C']}
        for _ in range(n_boot):
            idx = rng.choice(len(y), size=len(y), replace=True)
            t_b, y_b = t_norm[idx], y[idx]
            sort_idx = np.argsort(t_b)
            t_b, y_b = t_b[sort_idx], y_b[sort_idx]
            try:
                popt_b, _ = curve_fit(damped_wave, t_b, y_b, p0=popt_w,
                                      bounds=bounds_wave, maxfev=10000)
                for i, k in enumerate(['A', 'd', 'f', 'phi', 'C']):
                    boot_params[k].append(popt_b[i])
            except Exception:
                pass
        n_success = len(boot_params['A'])
        print(f'  Bootstrap success: {n_success}/{n_boot}')
        if n_success > 100:
            ci = {}
            for k, vals in boot_params.items():
                lo, hi = np.percentile(vals, [2.5, 97.5])
                ci[k] = {'lo': lo, 'hi': hi, 'median': np.median(vals)}
                print(f'    {k}: {ci[k]["median"]:.4f} [{lo:.4f}, {hi:.4f}]')
            results['bootstrap_ci'] = ci

    return results


def plot_fit(steps, entropy, results, save_path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    t = np.array(steps, dtype=float)
    y = np.array(entropy, dtype=float)
    t_norm = (t - t[0]) / (t[-1] - t[0]) if t[-1] > t[0] else t
    t_fine = np.linspace(0, 1, 500)
    steps_fine = np.linspace(steps[0], steps[-1], 500)

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]})
    ax = axes[0]
    ax.scatter(steps, y, c='black', s=20, zorder=5, label='Data')

    if 'params' in results.get('wave', {}):
        p = results['wave']['params']
        y_wave = damped_wave(t_fine, p['A'], p['d'], p['f'], p['phi'], p['C'])
        ax.plot(steps_fine, y_wave, 'r-', lw=2,
                label=f'Wave (R²={results["wave"]["R2"]:.4f}, {results["wave"]["regime"]})')

    if 'params' in results.get('exponential', {}):
        p = results['exponential']['params']
        y_exp = pure_exponential(t_fine, p['A'], p['d'], p['C'])
        ax.plot(steps_fine, y_exp, 'b--', lw=2,
                label=f'Exponential (R²={results["exponential"]["R2"]:.4f})')

    ax.set_xlabel('Training Step')
    ax.set_ylabel('Entropy')
    ax.set_title('V8 Entropy Curve: Wave-FEP Fit (GPT-2 Medium)')
    ax.legend()
    ax.grid(True, alpha=0.3)

    ax2 = axes[1]
    if 'params' in results.get('wave', {}):
        p = results['wave']['params']
        y_wave_data = damped_wave(t_norm, p['A'], p['d'], p['f'], p['phi'], p['C'])
        ax2.scatter(steps, y - y_wave_data, c='red', s=10, alpha=0.7, label='Wave residuals')
    if 'params' in results.get('exponential', {}):
        p = results['exponential']['params']
        y_exp_data = pure_exponential(t_norm, p['A'], p['d'], p['C'])
        ax2.scatter(steps, y - y_exp_data, c='blue', s=10, alpha=0.7, label='Exp residuals')

    ax2.axhline(0, c='gray', ls='-', lw=0.5)
    ax2.set_xlabel('Training Step')
    ax2.set_ylabel('Residual')
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f'\n  Plot saved: {save_path}')
    plt.close()


def main():
    print('=' * 60)
    print('  FEP Wave Fit — V8 (GPT-2 Medium, wikitext-103)')
    print('  Roadmap #12')
    print('=' * 60)

    log_path = os.path.join(SCRIPT_DIR, 'checkpoints', 'v8_deep', 'training_log.csv')

    if not os.path.exists(log_path):
        print(f'ERROR: No training log found at {log_path}')
        sys.exit(1)

    print(f'\nUsing training log: {log_path}')
    import csv
    with open(log_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    # v8 training log columns:
    # step, loss, lang_loss, tri_loss, sup_loss, sub_loss,
    # bit_acc_train, bit_acc_test, sub_train, sub_test, dead_bits, entropy
    # Skip header if present
    data_rows = [r for r in rows if r and r[0].strip() and r[0].strip() != 'step']
    steps = [int(float(r[0])) for r in data_rows]
    entropy = [float(r[11]) for r in data_rows]

    # Remove duplicates (keep last)
    seen = {}
    for s, e in zip(steps, entropy):
        seen[s] = e
    steps = sorted(seen.keys())
    entropy = [seen[s] for s in steps]

    print(f'  Steps: {len(steps)} ({steps[0]} -> {steps[-1]})')
    print(f'  Entropy range: [{min(entropy):.4f}, {max(entropy):.4f}]')

    print('\nFitting models...')
    results = fit_models(steps, entropy)

    # Save
    def jsonify(obj):
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, (np.float32, np.float64)):
            return float(obj)
        if isinstance(obj, (np.int32, np.int64)):
            return int(obj)
        if isinstance(obj, dict):
            return {k: jsonify(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [jsonify(v) for v in obj]
        return obj

    out_path = os.path.join(RESULTS_DIR, 'v8_fep_wave_fit.json')
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(jsonify(results), f, indent=2)
    print(f'\nResults saved: {out_path}')

    # Plot
    plots_dir = os.path.join(SCRIPT_DIR, '..', 'runs', 'v8_deep', 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    try:
        plot_fit(steps, entropy, results, os.path.join(plots_dir, 'fep_wave_fit.png'))
    except Exception as e:
        print(f'Plot failed: {e}')

    # Cross-model comparison
    v9_fit_path = os.path.join(RESULTS_DIR, 'v9_fep_wave_fit.json')
    if os.path.exists(v9_fit_path):
        with open(v9_fit_path, 'r') as f:
            v9 = json.load(f)
        print('\n  === V8 vs V9 Wave-FEP Comparison ===')
        print(f'  {"Metric":<20} {"V8":>12} {"V9":>12}')
        print(f'  {"-"*20} {"-"*12} {"-"*12}')
        for k in ['R2', 'regime', 'damping_ratio']:
            v8_val = results.get('wave', {}).get(k, 'N/A')
            v9_val = v9.get('wave', {}).get(k, 'N/A')
            if isinstance(v8_val, float):
                v8_val = f'{v8_val:.4f}'
            if isinstance(v9_val, float):
                v9_val = f'{v9_val:.4f}'
            print(f'  {k:<20} {str(v8_val):>12} {str(v9_val):>12}')
        v8_pref = results.get('comparison', {}).get('preferred', 'N/A')
        v9_pref = v9.get('comparison', {}).get('preferred', 'N/A')
        print(f'  {"preferred":<20} {v8_pref:>12} {v9_pref:>12}')
        v8_daic = results.get('comparison', {}).get('delta_AIC', 'N/A')
        v9_daic = v9.get('comparison', {}).get('delta_AIC', 'N/A')
        if isinstance(v8_daic, float):
            v8_daic = f'{v8_daic:.1f}'
        if isinstance(v9_daic, float):
            v9_daic = f'{v9_daic:.1f}'
        print(f'  {"delta_AIC":<20} {str(v8_daic):>12} {str(v9_daic):>12}')

    print('\n' + '=' * 60)


if __name__ == '__main__':
    main()
