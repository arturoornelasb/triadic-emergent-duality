"""Benjamini-Hochberg FDR and Holm-Bonferroni corrections.

Port of reptimeline/stats.py benjamini_hochberg() to pure stdlib.
Solo stdlib: math, no numpy.

Usage standalone:
    python bh_fdr.py          Run self-tests
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')


# ######################################################################
#  SECTION 1: BENJAMINI-HOCHBERG FDR
# ######################################################################

def benjamini_hochberg(p_values, alpha=0.05):
    """Benjamini-Hochberg False Discovery Rate correction.

    Args:
        p_values: list of p-values from m tests.
        alpha: significance level (default 0.05).

    Returns:
        list of booleans — True = significant after correction.
    """
    m = len(p_values)
    if m == 0:
        return []

    # Sort indices by p-value
    sorted_idx = sorted(range(m), key=lambda i: p_values[i])
    sorted_p = [p_values[i] for i in sorted_idx]

    # Compute thresholds: alpha * rank / m
    thresholds = [alpha * (i + 1) / m for i in range(m)]

    # Find passing tests
    passing = [sorted_p[i] <= thresholds[i] for i in range(m)]

    if not any(passing):
        return [False] * m

    # Find largest k where p_(k) <= threshold_(k)
    max_k = max(i for i, v in enumerate(passing) if v)

    # All tests with rank <= max_k are significant
    significant = [False] * m
    for i in range(max_k + 1):
        significant[sorted_idx[i]] = True

    return significant


# ######################################################################
#  SECTION 2: HOLM-BONFERRONI (STEP-DOWN)
# ######################################################################

def holm_bonferroni(p_values, alpha=0.05):
    """Holm-Bonferroni step-down correction for multiple comparisons.

    More powerful than plain Bonferroni, controls FWER.

    Args:
        p_values: list of p-values from m tests.
        alpha: significance level (default 0.05).

    Returns:
        list of booleans — True = significant after correction.
    """
    m = len(p_values)
    if m == 0:
        return []

    sorted_idx = sorted(range(m), key=lambda i: p_values[i])
    significant = [False] * m

    for rank, idx in enumerate(sorted_idx):
        threshold = alpha / (m - rank)
        if p_values[idx] > threshold:
            break
        significant[idx] = True

    return significant


# ######################################################################
#  SECTION 3: SELF-TEST
# ######################################################################

if __name__ == '__main__':
    print("=== Benjamini-Hochberg self-test ===")

    # Test 1: known example — 3 of 4 pass BH at alpha=0.05
    # sorted: 0.005, 0.015, 0.030, 0.060
    # thresholds: 0.0125, 0.025, 0.0375, 0.05
    # 0.005<=0.0125 T, 0.015<=0.025 T, 0.030<=0.0375 T, 0.060<=0.05 F
    pvals = [0.005, 0.015, 0.030, 0.060]
    result = benjamini_hochberg(pvals, 0.05)
    expected = [True, True, True, False]
    assert result == expected, f"FAIL: got {result}, expected {expected}"
    print(f"  Test 1 PASS: {pvals} -> {result}")

    # Test 2: nothing significant
    pvals2 = [0.50, 0.60, 0.70]
    result2 = benjamini_hochberg(pvals2, 0.05)
    assert result2 == [False, False, False], f"FAIL: got {result2}"
    print(f"  Test 2 PASS: {pvals2} -> {result2}")

    # Test 3: all significant
    pvals3 = [0.001, 0.002, 0.003]
    result3 = benjamini_hochberg(pvals3, 0.05)
    assert result3 == [True, True, True], f"FAIL: got {result3}"
    print(f"  Test 3 PASS: {pvals3} -> {result3}")

    # Test 4: empty
    assert benjamini_hochberg([], 0.05) == []
    print("  Test 4 PASS: empty list")

    print("\n=== Holm-Bonferroni self-test ===")

    # Test 5: basic Holm
    pvals5 = [0.01, 0.04, 0.03, 0.06]
    result5 = holm_bonferroni(pvals5, 0.05)
    # Sorted: 0.01(idx0), 0.03(idx2), 0.04(idx1), 0.06(idx3)
    # Thresholds: 0.05/4=0.0125, 0.05/3=0.0167, 0.05/2=0.025, 0.05/1=0.05
    # 0.01 <= 0.0125 -> True
    # 0.03 <= 0.0167 -> False -> STOP
    expected5 = [True, False, False, False]
    assert result5 == expected5, f"FAIL: got {result5}, expected {expected5}"
    print(f"  Test 5 PASS: {pvals5} -> {result5}")

    # Test 6: Holm more conservative than BH
    pvals6 = [0.01, 0.03, 0.04]
    bh = benjamini_hochberg(pvals6, 0.05)
    holm = holm_bonferroni(pvals6, 0.05)
    # BH is more liberal than Holm
    bh_count = sum(bh)
    holm_count = sum(holm)
    assert holm_count <= bh_count, f"FAIL: Holm ({holm_count}) > BH ({bh_count})"
    print(f"  Test 6 PASS: Holm ({holm_count}) <= BH ({bh_count})")

    print("\nAll tests passed.")
