"""Bootstrap confidence intervals — stdlib only.

Port of reptimeline/stats.py bootstrap_ci() to pure stdlib.
Solo stdlib: math, random.

Usage standalone:
    python bootstrap.py       Run self-tests
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import math
import random


# ######################################################################
#  SECTION 1: HELPER — PERCENTILE
# ######################################################################

def percentile(data, p):
    """Compute the p-th percentile of data using linear interpolation.

    Args:
        data: list of numbers (will be sorted internally).
        p: percentile in [0, 100].

    Returns:
        float — the interpolated percentile value.
    """
    s = sorted(data)
    n = len(s)
    if n == 0:
        raise ValueError("Cannot compute percentile of empty list")
    if n == 1:
        return s[0]
    k = (n - 1) * p / 100.0
    f = math.floor(k)
    c = min(math.ceil(k), n - 1)
    if f == c:
        return s[int(k)]
    return s[f] * (c - k) + s[c] * (k - f)


# ######################################################################
#  SECTION 2: BOOTSTRAP CONFIDENCE INTERVAL
# ######################################################################

def bootstrap_ci(values_a, values_b, statistic_fn, n_bootstrap=1000,
                 ci=0.95, seed=42):
    """Compute bootstrap confidence interval for a two-sample statistic.

    Args:
        values_a: list of floats — first sample.
        values_b: list of floats — second sample.
        statistic_fn: function(a, b) -> float.
        n_bootstrap: number of resamples (default 1000).
        ci: confidence level (default 0.95).
        seed: random seed.

    Returns:
        dict with keys: observed, ci_low, ci_high, n_bootstrap.
    """
    if len(values_a) == 0 or len(values_b) == 0:
        raise ValueError("Both samples must be non-empty")

    rng = random.Random(seed)
    observed = statistic_fn(values_a, values_b)

    stats = []
    for _ in range(n_bootstrap):
        a_sample = [rng.choice(values_a) for _ in range(len(values_a))]
        b_sample = [rng.choice(values_b) for _ in range(len(values_b))]
        stats.append(statistic_fn(a_sample, b_sample))

    alpha = 1.0 - ci
    return {
        'observed': observed,
        'ci_low': percentile(stats, 100 * alpha / 2),
        'ci_high': percentile(stats, 100 * (1 - alpha / 2)),
        'n_bootstrap': n_bootstrap,
    }


# ######################################################################
#  SECTION 3: SELF-TEST
# ######################################################################

if __name__ == '__main__':
    print("=== percentile self-test ===")
    assert percentile([1, 2, 3, 4, 5], 50) == 3.0
    assert percentile([1, 2, 3, 4, 5], 0) == 1.0
    assert percentile([1, 2, 3, 4, 5], 100) == 5.0
    print("  percentile tests PASS")

    print("\n=== bootstrap_ci self-test ===")

    def mean_diff(a, b):
        return sum(a) / len(a) - sum(b) / len(b)

    # Two clearly different groups
    a = [10.0, 11.0, 12.0, 13.0, 14.0]
    b = [1.0, 2.0, 3.0, 4.0, 5.0]
    result = bootstrap_ci(a, b, mean_diff, n_bootstrap=5000, seed=42)
    print(f"  observed: {result['observed']:.2f}")
    print(f"  CI: [{result['ci_low']:.2f}, {result['ci_high']:.2f}]")
    assert result['ci_low'] > 0, "CI should be entirely above 0"
    print("  bootstrap_ci PASS: CI correctly excludes 0")

    # Two identical groups — CI should contain 0
    c = [5.0, 5.1, 4.9, 5.0, 5.1]
    d = [5.0, 4.9, 5.1, 5.0, 4.9]
    result2 = bootstrap_ci(c, d, mean_diff, n_bootstrap=5000, seed=42)
    print(f"\n  identical groups observed: {result2['observed']:.4f}")
    print(f"  CI: [{result2['ci_low']:.4f}, {result2['ci_high']:.4f}]")
    assert result2['ci_low'] <= 0 <= result2['ci_high'], "CI should contain 0"
    print("  bootstrap_ci PASS: CI correctly contains 0 for identical groups")

    print("\nAll tests passed.")
