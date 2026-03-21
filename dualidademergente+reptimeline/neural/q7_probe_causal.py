"""Q7: Do causal interventions on bits produce layer-consistent effects?

Probe: Use CausalVerifier to intervene on individual bits and measure
downstream effects. Group effects by theoretical layer. If higher-layer
bit interventions produce larger cascading effects, this is consistent
with the emergence hierarchy.

Caveat: Causal effects in neural networks depend on model architecture
(attention patterns, residual connections), not on ontological structure.

Requiere: pip install reptimeline
Usage: python q7_probe_causal.py --checkpoints <dir> --model <path>
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import argparse
import json
import math
import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(SCRIPT_DIR, 'results')
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))
STATS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'stats'))
sys.path.insert(0, STATS_DIR)

from bootstrap import bootstrap_ci
from registry import register_pvalue

try:
    from reptimeline import CausalVerifier
    from reptimeline.extractors import TriadicExtractor
    HAS_REPTIMELINE = True
except ImportError:
    HAS_REPTIMELINE = False


# ######################################################################
#  SECTION 0: DATA LOADING
# ######################################################################

with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
    prim_data = json.load(f)

prims = prim_data['primitivos']
bit_to_capa = {p.get('bit'): p['capa'] for p in prims if p.get('bit') is not None}
bit_to_name = {p.get('bit'): p['nombre'] for p in prims if p.get('bit') is not None}


# ######################################################################
#  SECTION 1: SPEARMAN RHO
# ######################################################################

def _rank(values):
    n = len(values)
    indexed = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j < n - 1 and values[indexed[j + 1]] == values[indexed[j]]:
            j += 1
        avg = (i + j) / 2.0 + 1
        for k in range(i, j + 1):
            ranks[indexed[k]] = avg
        i = j + 1
    return ranks


def spearman_rho(x, y):
    n = len(x)
    if n < 3:
        return 0.0
    rx, ry = _rank(x), _rank(y)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    dx = math.sqrt(sum((rx[i] - mx) ** 2 for i in range(n)))
    dy = math.sqrt(sum((ry[i] - my) ** 2 for i in range(n)))
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)


def spearman_p_perm(x, y, n_perms=5000, seed=42):
    rng = random.Random(seed)
    observed = abs(spearman_rho(x, y))
    count = 0
    yc = list(y)
    for _ in range(n_perms):
        rng.shuffle(yc)
        if abs(spearman_rho(x, yc)) >= observed:
            count += 1
    return (count + 1) / (n_perms + 1)


# ######################################################################
#  SECTION 2: RUN PROBE
# ######################################################################

def build_intervene_fn(model_path):
    """Build the intervention function for CausalVerifier.

    The intervene_fn must: perturb one bit for one concept, measure
    the effect on model output (e.g., KL divergence of next-token
    distribution).

    This is model-specific. Placeholder loads TriadicGPT.
    """
    # In practice, this would load the model and implement:
    # 1. Forward pass with original code
    # 2. Flip bit_index in the triadic code
    # 3. Forward pass with modified code
    # 4. Return KL divergence between outputs
    try:
        from triadic_microgpt.model import TriadicGPT
        import torch

        model = TriadicGPT.load(model_path)
        model.eval()

        def intervene(concept, bit_index):
            # Get original code
            with torch.no_grad():
                orig_code = model.encode_concept(concept)
                orig_output = model.forward_from_code(orig_code)

                # Flip bit
                mod_code = orig_code.clone()
                mod_code[0, bit_index] = 1 - mod_code[0, bit_index]
                mod_output = model.forward_from_code(mod_code)

                # KL divergence
                kl = torch.nn.functional.kl_div(
                    mod_output.log_softmax(-1),
                    orig_output.softmax(-1),
                    reduction='batchmean'
                )
                return kl.item()

        return intervene
    except (ImportError, FileNotFoundError):
        return None


def run_probe(checkpoints_dir, model_path):
    """Run Q7 probe."""
    if not HAS_REPTIMELINE:
        return None

    intervene_fn = build_intervene_fn(model_path)
    if intervene_fn is None:
        print("ERROR: Could not build intervention function.")
        print("  Need triadic_microgpt model at: " + str(model_path))
        return None

    extractor = TriadicExtractor(checkpoints_dir)
    snapshots = extractor.load_snapshots(checkpoints_dir)
    snapshot = snapshots[-1]

    # Only test bits that map to known primitives
    test_bits = [b for b in bit_to_capa if b < snapshot.code_dim]

    verifier = CausalVerifier(
        intervene_fn=intervene_fn,
        n_bootstrap=1000,
        n_perms=1000,
        alpha=0.05,
    )
    causal_report = verifier.verify(snapshot, bit_indices=test_bits)

    return causal_report, snapshot


def analyze(causal_report, snapshot):
    """Analyze causal effects by layer."""
    print("=" * 70)
    print("Q7: Causal interventions — layer-consistent effects?")
    print("=" * 70)

    print(f"\n  Bits tested: {causal_report.n_tested}")
    print(f"  Significant (BH-FDR): {causal_report.n_significant}")
    print(f"  Verdict: {causal_report.verdict}")

    # Group effects by layer
    layer_effects = {}
    for br in causal_report.bit_results:
        bit = br.bit_index
        capa = bit_to_capa.get(bit)
        if capa is None:
            continue

        if capa not in layer_effects:
            layer_effects[capa] = []
        layer_effects[capa].append(br.effect_size)

    print("\n  --- Mean effect size by layer ---\n")
    layers = []
    mean_effects = []

    for layer in sorted(layer_effects):
        effs = layer_effects[layer]
        mean_e = sum(effs) / len(effs)
        layers.append(layer)
        mean_effects.append(mean_e)
        print(f"  Layer {layer}: n={len(effs)}, "
              f"mean |Cohen's d| = {mean_e:.3f}")

    # Spearman: does layer predict effect size?
    if len(layers) >= 3:
        rho = spearman_rho(layers, mean_effects)
        p_val = spearman_p_perm(layers, mean_effects)
        print(f"\n  Spearman rho(layer, effect) = {rho:.3f}")
        print(f"  Permutation p = {p_val:.4f}")
    else:
        rho = 0.0
        p_val = 1.0
        print("\n  Too few layers for correlation.")

    # All individual bits
    print("\n  --- Top 10 bits by effect size ---\n")
    sorted_bits = sorted(causal_report.bit_results,
                         key=lambda b: abs(b.effect_size), reverse=True)
    for br in sorted_bits[:10]:
        name = bit_to_name.get(br.bit_index, f'bit{br.bit_index}')
        capa = bit_to_capa.get(br.bit_index, '?')
        sig = 'SIG' if br.significant else '---'
        print(f"  [{sig}] {name:<20} layer={capa} "
              f"|d|={abs(br.effect_size):.3f} p={br.p_value:.4f}")

    # Register
    reg_path = os.path.join(STATS_DIR, 'p_values_registry.json')
    register_pvalue('neural_causal', 'q7_layer_vs_effect', p_val,
                    notes=f'rho={rho:.3f}, n_layers={len(layers)}',
                    path=reg_path)

    # Interpretation
    print("\n  --- Interpretation ---\n")
    if rho > 0.5 and p_val < 0.05:
        print("  POSITIVE: Higher layers produce larger causal effects.")
        print("  Confounder: architecture-dependent (attention, residuals).")
        verdict = 'positive_with_caveats'
    elif rho > 0:
        print("  MIXED: Weak positive trend, not significant.")
        verdict = 'mixed'
    else:
        print("  NULL: No layer-effect relationship.")
        verdict = 'null'

    results = {
        'n_tested': causal_report.n_tested,
        'n_significant': causal_report.n_significant,
        'causal_verdict': causal_report.verdict,
        'layer_effects': {
            str(k): {
                'n': len(v),
                'mean_effect': round(sum(v) / len(v), 4),
            }
            for k, v in layer_effects.items()
        },
        'rho_layer_effect': round(rho, 4),
        'p_value': round(p_val, 4),
        'verdict': verdict,
    }
    return results


# ######################################################################
#  SECTION 3: MAIN
# ######################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Q7: Causal probe')
    parser.add_argument('--checkpoints', required=True)
    parser.add_argument('--model', required=True,
                        help='Path to TriadicGPT model weights')
    args = parser.parse_args()

    if not HAS_REPTIMELINE:
        print("=" * 70)
        print("Q7: Causal Probe — reptimeline NOT INSTALLED")
        print("=" * 70)
        print("\nInstall with: pip install reptimeline")
        sys.exit(1)

    result = run_probe(args.checkpoints, args.model)
    if result is None:
        sys.exit(1)

    causal_report, snapshot = result
    results = analyze(causal_report, snapshot)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_path = os.path.join(RESULTS_DIR, 'q7_causal.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to: {out_path}")
