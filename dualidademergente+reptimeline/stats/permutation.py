"""Permutation test — stdlib only.

Port of reptimeline/stats.py permutation_test() to pure stdlib.
Solo stdlib: random.

Usage standalone:
    python permutation.py     Run self-tests
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import random


# ######################################################################
#  SECTION 1: PERMUTATION TEST
# ######################################################################

def permutation_test(values_a, values_b, statistic_fn, n_perms=1000,
                     seed=42):
    """Two-sided permutation test.

    Pools values_a and values_b, reshuffles, recomputes statistic_fn,
    and returns the fraction of permuted statistics >= observed.

    Args:
        values_a: list of floats — first sample.
        values_b: list of floats — second sample.
        statistic_fn: function(a, b) -> float.
        n_perms: number of permutations (default 1000).
        seed: random seed.

    Returns:
        p-value in [1/(n_perms+1), 1.0].
    """
    if len(values_a) == 0 or len(values_b) == 0:
        raise ValueError("Both samples must be non-empty")

    rng = random.Random(seed)
    observed = abs(statistic_fn(values_a, values_b))

    pooled = list(values_a) + list(values_b)
    n_a = len(values_a)
    count_ge = 0

    for _ in range(n_perms):
        perm = pooled[:]
        rng.shuffle(perm)
        perm_stat = abs(statistic_fn(perm[:n_a], perm[n_a:]))
        if perm_stat >= observed:
            count_ge += 1

    return (count_ge + 1) / (n_perms + 1)


# ######################################################################
#  SECTION 2: SELF-TEST
# ######################################################################

if __name__ == '__main__':
    print("=== permutation_test self-test ===")

    def mean_diff(a, b):
        return sum(a) / len(a) - sum(b) / len(b)

    # Test 1: clearly different groups -> small p
    a = [10.0, 11.0, 12.0, 13.0, 14.0]
    b = [1.0, 2.0, 3.0, 4.0, 5.0]
    p = permutation_test(a, b, mean_diff, n_perms=5000, seed=42)
    print(f"  Different groups: p = {p:.4f}")
    assert p < 0.05, f"FAIL: p={p} should be < 0.05"
    print("  Test 1 PASS: p < 0.05 for clearly different groups")

    # Test 2: identical groups -> large p
    c = [5.0, 5.1, 4.9, 5.0, 5.1]
    d = [5.0, 4.9, 5.1, 5.0, 4.9]
    p2 = permutation_test(c, d, mean_diff, n_perms=5000, seed=42)
    print(f"\n  Identical groups: p = {p2:.4f}")
    assert p2 > 0.30, f"FAIL: p={p2} should be > 0.30"
    print("  Test 2 PASS: p > 0.30 for identical groups")

    # Test 3: p-value bounds
    assert 0 < p <= 1.0, f"FAIL: p out of bounds: {p}"
    assert 0 < p2 <= 1.0, f"FAIL: p2 out of bounds: {p2}"
    print("\n  Test 3 PASS: p-values in valid range")

    print("\nAll tests passed.")
