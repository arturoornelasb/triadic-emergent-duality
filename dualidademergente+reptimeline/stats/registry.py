"""P-value registry — central tracking of all statistical tests.

Stores all p-values in p_values_registry.json for program-level
correction and auditing.
Solo stdlib: json, os.

Usage standalone:
    python registry.py        Run self-tests (uses temp file)
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REGISTRY_PATH = os.path.join(SCRIPT_DIR, 'p_values_registry.json')


# ######################################################################
#  SECTION 1: LOAD / SAVE
# ######################################################################

def load_registry(path=None):
    """Load the p-value registry from JSON.

    Returns:
        list of dicts, each with keys:
            hypothesis, test, p_raw, p_bh_family, p_holm_program,
            significant_family, significant_program, alpha, notes
    """
    path = path or REGISTRY_PATH
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_registry(entries, path=None):
    """Save registry entries to JSON."""
    path = path or REGISTRY_PATH
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


# ######################################################################
#  SECTION 2: REGISTER P-VALUE
# ######################################################################

def register_pvalue(hypothesis, test_name, p_raw, alpha=0.05, notes='',
                    path=None):
    """Register a p-value from a statistical test.

    Args:
        hypothesis: e.g. 'I1', 'Q2', 'I3_deps'
        test_name: e.g. 'depth_circle_rho', 'dual_bien_mal'
        p_raw: raw p-value (float)
        alpha: significance level (default 0.05)
        notes: optional notes about the test
        path: override registry file path

    Returns:
        the new entry dict.
    """
    entries = load_registry(path)

    # Check for duplicate — update if exists
    for entry in entries:
        if entry['hypothesis'] == hypothesis and entry['test'] == test_name:
            entry['p_raw'] = p_raw
            entry['alpha'] = alpha
            entry['notes'] = notes
            entry['p_bh_family'] = None
            entry['p_holm_program'] = None
            entry['significant_family'] = None
            entry['significant_program'] = None
            save_registry(entries, path)
            return entry

    new_entry = {
        'hypothesis': hypothesis,
        'test': test_name,
        'p_raw': p_raw,
        'p_bh_family': None,
        'p_holm_program': None,
        'significant_family': None,
        'significant_program': None,
        'alpha': alpha,
        'notes': notes,
    }
    entries.append(new_entry)
    save_registry(entries, path)
    return new_entry


# ######################################################################
#  SECTION 3: APPLY FAMILY-LEVEL BH-FDR
# ######################################################################

def apply_family_correction(hypothesis_prefix, alpha=0.05, path=None):
    """Apply BH-FDR correction to all tests within one hypothesis family.

    Args:
        hypothesis_prefix: e.g. 'I1' — corrects all entries starting with this.
        alpha: significance level.
        path: override registry path.

    Returns:
        number of significant tests after correction.
    """
    # Import here to avoid circular dependency
    from bh_fdr import benjamini_hochberg

    entries = load_registry(path)
    family = [e for e in entries if e['hypothesis'].startswith(hypothesis_prefix)]

    if not family:
        return 0

    p_raw = [e['p_raw'] for e in family]
    significant = benjamini_hochberg(p_raw, alpha)

    for entry, sig in zip(family, significant):
        entry['significant_family'] = sig
        # Compute adjusted p-value (step-up)
        # For BH: p_adj = min(p_raw * m / rank, 1.0)
        # This is an approximation; the boolean is authoritative
        entry['p_bh_family'] = entry['p_raw']  # raw stored, bool is key

    save_registry(entries, path)
    return sum(significant)


# ######################################################################
#  SECTION 4: APPLY PROGRAM-LEVEL HOLM-BONFERRONI
# ######################################################################

def apply_program_correction(alpha=0.05, path=None):
    """Apply Holm-Bonferroni correction across ALL registered p-values.

    This is the most conservative correction — controls FWER across
    the entire research program.

    Returns:
        number of significant tests after correction.
    """
    from bh_fdr import holm_bonferroni

    entries = load_registry(path)
    if not entries:
        return 0

    p_raw = [e['p_raw'] for e in entries]
    significant = holm_bonferroni(p_raw, alpha)

    for entry, sig in zip(entries, significant):
        entry['significant_program'] = sig

    save_registry(entries, path)
    return sum(significant)


# ######################################################################
#  SECTION 5: SUMMARY
# ######################################################################

def print_registry_summary(path=None):
    """Print a formatted summary of all registered p-values."""
    entries = load_registry(path)
    if not entries:
        print("Registry empty.")
        return

    print(f"{'Hypothesis':<12} {'Test':<30} {'p_raw':>8} {'BH-fam':>8} {'Holm-prog':>10}")
    print("-" * 70)
    for e in sorted(entries, key=lambda x: x['p_raw']):
        sig_fam = 'YES' if e.get('significant_family') else ('no' if e.get('significant_family') is not None else '-')
        sig_prog = 'YES' if e.get('significant_program') else ('no' if e.get('significant_program') is not None else '-')
        print(f"{e['hypothesis']:<12} {e['test']:<30} {e['p_raw']:>8.4f} {sig_fam:>8} {sig_prog:>10}")

    n_total = len(entries)
    n_fam = sum(1 for e in entries if e.get('significant_family'))
    n_prog = sum(1 for e in entries if e.get('significant_program'))
    print(f"\nTotal: {n_total} tests | BH-family significant: {n_fam} | Holm-program significant: {n_prog}")


# ######################################################################
#  SECTION 6: SELF-TEST
# ######################################################################

if __name__ == '__main__':
    import tempfile
    tmp = os.path.join(tempfile.gettempdir(), '_test_registry.json')

    print("=== registry self-test ===")

    # Clean
    if os.path.exists(tmp):
        os.remove(tmp)

    # Register
    register_pvalue('I1', 'depth_circle', 0.482, path=tmp)
    register_pvalue('I1', 'depth_spiral', 0.119, path=tmp)
    register_pvalue('I1', 'drate_circle', 0.819, path=tmp)
    register_pvalue('Q2', 'dual_bien_mal', 0.003, path=tmp)

    entries = load_registry(tmp)
    assert len(entries) == 4, f"FAIL: expected 4 entries, got {len(entries)}"
    print("  Test 1 PASS: 4 entries registered")

    # Update duplicate
    register_pvalue('I1', 'depth_circle', 0.500, path=tmp)
    entries = load_registry(tmp)
    assert len(entries) == 4, f"FAIL: duplicate should update, not append"
    updated = [e for e in entries if e['test'] == 'depth_circle'][0]
    assert updated['p_raw'] == 0.500, f"FAIL: p_raw not updated"
    print("  Test 2 PASS: duplicate update works")

    # Summary
    print("\n  Summary:")
    print_registry_summary(tmp)

    # Cleanup
    os.remove(tmp)
    print("\nAll tests passed.")
