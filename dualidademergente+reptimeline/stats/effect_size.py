"""Effect size measures — stdlib only.

Port of reptimeline/stats.py effect_size_cohens_d() and
selectivity_ratio() to pure stdlib.
Solo stdlib: math.

Usage standalone:
    python effect_size.py     Run self-tests
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import math


# ######################################################################
#  SECTION 1: COHEN'S D
# ######################################################################

def cohens_d(values_a, values_b):
    """Cohen's d effect size for two independent samples.

    Uses pooled standard deviation.

    Args:
        values_a: list of floats — first sample.
        values_b: list of floats — second sample.

    Returns:
        float — Cohen's d.
            |d| < 0.2  = small
            |d| 0.2-0.5 = small-medium
            |d| 0.5-0.8 = medium-large
            |d| >= 0.8  = large
    """
    if len(values_a) == 0 or len(values_b) == 0:
        raise ValueError("Both samples must be non-empty")

    n_a = len(values_a)
    n_b = len(values_b)
    mean_a = sum(values_a) / n_a
    mean_b = sum(values_b) / n_b

    if n_a > 1:
        var_a = sum((x - mean_a) ** 2 for x in values_a) / (n_a - 1)
    else:
        var_a = 0.0

    if n_b > 1:
        var_b = sum((x - mean_b) ** 2 for x in values_b) / (n_b - 1)
    else:
        var_b = 0.0

    denom = max(n_a + n_b - 2, 1)
    pooled_var = ((n_a - 1) * var_a + (n_b - 1) * var_b) / denom
    pooled_std = math.sqrt(pooled_var)

    if pooled_std < 1e-12:
        return 0.0

    return (mean_a - mean_b) / pooled_std


# ######################################################################
#  SECTION 2: SELECTIVITY RATIO
# ######################################################################

def selectivity_ratio(labeled_values, other_values):
    """Compute selectivity ratio: mean(labeled) / mean(other).

    Handles division by zero:
        Both near zero -> 0.0
        Only denominator near zero -> 999.0 (sentinel)

    Args:
        labeled_values: list of floats.
        other_values: list of floats.

    Returns:
        float — ratio.
    """
    mean_l = sum(labeled_values) / len(labeled_values) if labeled_values else 0.0
    mean_o = sum(other_values) / len(other_values) if other_values else 0.0

    if abs(mean_o) < 1e-8:
        if abs(mean_l) < 1e-8:
            return 0.0
        return 999.0

    return mean_l / mean_o


# ######################################################################
#  SECTION 3: SELF-TEST
# ######################################################################

if __name__ == '__main__':
    print("=== cohens_d self-test ===")

    # Test 1: large effect
    a = [1.0, 2.0, 3.0]
    b = [4.0, 5.0, 6.0]
    d = cohens_d(a, b)
    print(f"  [1,2,3] vs [4,5,6]: d = {d:.3f}")
    assert abs(d - (-3.0)) < 0.1, f"FAIL: expected ~-3.0, got {d}"
    print("  Test 1 PASS: large negative effect")

    # Test 2: no effect
    c = [5.0, 5.0, 5.0]
    d2 = cohens_d(c, c)
    assert d2 == 0.0, f"FAIL: expected 0.0, got {d2}"
    print("  Test 2 PASS: zero effect for identical groups")

    # Test 3: single element
    d3 = cohens_d([10.0], [5.0])
    print(f"  Single elements: d = {d3:.3f}")
    print("  Test 3 PASS: single element handled")

    print("\n=== selectivity_ratio self-test ===")

    # Test 4: normal ratio
    r = selectivity_ratio([10.0, 12.0], [5.0, 5.0])
    print(f"  ratio: {r:.2f}")
    assert abs(r - 2.2) < 0.01, f"FAIL: expected ~2.2, got {r}"
    print("  Test 4 PASS")

    # Test 5: zero denominator
    r2 = selectivity_ratio([5.0], [0.0, 0.0])
    assert r2 == 999.0, f"FAIL: expected 999.0, got {r2}"
    print("  Test 5 PASS: zero denominator -> 999.0")

    # Test 6: both zero
    r3 = selectivity_ratio([0.0], [0.0])
    assert r3 == 0.0, f"FAIL: expected 0.0, got {r3}"
    print("  Test 6 PASS: both zero -> 0.0")

    print("\nAll tests passed.")
