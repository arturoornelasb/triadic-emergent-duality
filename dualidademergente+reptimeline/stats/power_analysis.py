"""Power analysis for small-sample Spearman tests — stdlib only.

Estimates statistical power via simulation: generate data with known
correlation, test it, count rejections.
Solo stdlib: math, random.

Usage standalone:
    python power_analysis.py  Run power table for all planned tests
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import math
import random


# ######################################################################
#  SECTION 1: SPEARMAN RHO (stdlib implementation)
# ######################################################################

def spearman_rho(x, y):
    """Compute Spearman rank correlation between x and y.

    Args:
        x, y: lists of numbers (same length).

    Returns:
        float in [-1, 1].
    """
    n = len(x)
    if n < 2:
        return 0.0

    def rank(data):
        indexed = sorted(range(n), key=lambda i: data[i])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j < n - 1 and data[indexed[j + 1]] == data[indexed[j]]:
                j += 1
            avg_rank = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                ranks[indexed[k]] = avg_rank
            i = j + 1
        return ranks

    rx = rank(x)
    ry = rank(y)

    mean_rx = sum(rx) / n
    mean_ry = sum(ry) / n
    num = sum((rx[i] - mean_rx) * (ry[i] - mean_ry) for i in range(n))
    den_x = math.sqrt(sum((rx[i] - mean_rx) ** 2 for i in range(n)))
    den_y = math.sqrt(sum((ry[i] - mean_ry) ** 2 for i in range(n)))

    if den_x < 1e-12 or den_y < 1e-12:
        return 0.0

    return num / (den_x * den_y)


# ######################################################################
#  SECTION 2: SPEARMAN P-VALUE (permutation-based)
# ######################################################################

def spearman_p(x, y, n_perms=1000, seed=None):
    """Compute two-sided p-value for Spearman rho via permutation.

    Args:
        x, y: lists of numbers.
        n_perms: number of permutations.
        seed: random seed (None = random).

    Returns:
        p-value.
    """
    rng = random.Random(seed)
    observed = abs(spearman_rho(x, y))
    count = 0
    y_perm = list(y)
    for _ in range(n_perms):
        rng.shuffle(y_perm)
        if abs(spearman_rho(x, y_perm)) >= observed:
            count += 1
    return (count + 1) / (n_perms + 1)


# ######################################################################
#  SECTION 3: GENERATE CORRELATED RANKS
# ######################################################################

def _generate_correlated(n, rho_target, rng):
    """Generate two lists of length n with approximate Spearman rho.

    Uses rank-based method: start with perfect rank correlation,
    then perturb to target rho.

    Args:
        n: sample size.
        rho_target: target Spearman rho in [0, 1].
        rng: random.Random instance.

    Returns:
        (x, y) where both are lists of floats.
    """
    x = list(range(n))
    y = list(range(n))

    # Number of random swaps to reduce correlation from 1.0 to ~rho_target
    # More swaps = lower correlation
    n_swaps = int(n * (1 - rho_target) * 1.5)
    for _ in range(n_swaps):
        i = rng.randint(0, n - 1)
        j = rng.randint(0, n - 1)
        y[i], y[j] = y[j], y[i]

    return x, y


# ######################################################################
#  SECTION 4: POWER SIMULATION
# ######################################################################

def power_spearman(n, rho_target, alpha=0.05, n_sim=2000, n_perms=500,
                   seed=42):
    """Estimate power of Spearman rho test via simulation.

    Args:
        n: sample size per test.
        rho_target: true rho to simulate.
        alpha: significance level.
        n_sim: number of simulated datasets.
        n_perms: permutations per test (for p-value).
        seed: random seed.

    Returns:
        dict with keys: power, n, rho_target, alpha, n_sim.
    """
    rng = random.Random(seed)
    rejections = 0

    for i in range(n_sim):
        x, y = _generate_correlated(n, rho_target, rng)
        p = spearman_p(x, y, n_perms=n_perms, seed=seed + i + 1)
        if p < alpha:
            rejections += 1

    power = rejections / n_sim
    return {
        'power': power,
        'n': n,
        'rho_target': rho_target,
        'alpha': alpha,
        'n_sim': n_sim,
    }


# ######################################################################
#  SECTION 5: MINIMUM DETECTABLE EFFECT
# ######################################################################

def min_detectable_effect(n, alpha=0.05, power_target=0.80, n_sim=1000,
                          n_perms=500, seed=42):
    """Find minimum rho detectable with given n and power.

    Binary search over rho in [0.1, 0.99].

    Returns:
        dict with keys: min_rho, power_at_min, n, alpha.
    """
    lo, hi = 0.1, 0.99

    for _ in range(8):  # ~8 iterations for precision ~0.01
        mid = (lo + hi) / 2.0
        result = power_spearman(n, mid, alpha, n_sim, n_perms, seed)
        if result['power'] >= power_target:
            hi = mid
        else:
            lo = mid

    final = power_spearman(n, hi, alpha, n_sim, n_perms, seed)
    return {
        'min_rho': round(hi, 2),
        'power_at_min': round(final['power'], 2),
        'n': n,
        'alpha': alpha,
    }


# ######################################################################
#  SECTION 6: POWER TABLE FOR ALL PLANNED TESTS
# ######################################################################

PLANNED_TESTS = [
    {'name': 'depth_circle (n=7)', 'n': 7, 'rho': 0.60},
    {'name': 'depth_spiral (n=7)', 'n': 7, 'rho': 0.60},
    {'name': 'drate_circle (n=7)', 'n': 7, 'rho': 0.60},
    {'name': 'drate_spiral (n=7)', 'n': 7, 'rho': 0.60},
    {'name': 'depth_combined (n=14)', 'n': 14, 'rho': 0.60},
    {'name': 'drate_combined (n=14)', 'n': 14, 'rho': 0.60},
    {'name': 'layer_emergence (n=6)', 'n': 6, 'rho': 0.80},
    {'name': 'causal_hierarchy (n=6)', 'n': 6, 'rho': 0.60},
]


def print_power_table():
    """Print power analysis for all planned tests."""
    print(f"{'Test':<30} {'n':>3} {'rho':>5} {'power':>7} {'min_rho(80%)':>13}")
    print("-" * 62)
    for t in PLANNED_TESTS:
        pw = power_spearman(t['n'], t['rho'], n_sim=1000, n_perms=300)
        mde = min_detectable_effect(t['n'], n_sim=500, n_perms=200)
        status = 'OK' if pw['power'] >= 0.50 else 'LOW'
        print(f"{t['name']:<30} {t['n']:>3} {t['rho']:>5.2f} {pw['power']:>6.2f} [{status}] {mde['min_rho']:>8.2f}")


# ######################################################################
#  SECTION 7: SELF-TEST / MAIN
# ######################################################################

if __name__ == '__main__':
    print("=== spearman_rho self-test ===")
    rho = spearman_rho([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    assert abs(rho - 1.0) < 0.01, f"FAIL: perfect correlation got {rho}"
    print(f"  Perfect correlation: rho = {rho:.3f} PASS")

    rho2 = spearman_rho([1, 2, 3, 4, 5], [5, 4, 3, 2, 1])
    assert abs(rho2 - (-1.0)) < 0.01, f"FAIL: perfect anti-correlation got {rho2}"
    print(f"  Perfect anti-correlation: rho = {rho2:.3f} PASS")

    print("\n=== power_spearman estimate (n=14, rho=0.60) ===")
    result = power_spearman(14, 0.60, n_sim=500, n_perms=300, seed=42)
    print(f"  power = {result['power']:.2f}")
    print(f"  (expected ~0.55-0.75 range)")

    print("\n=== Power table for all planned tests ===\n")
    print_power_table()

    print("\nDone.")
