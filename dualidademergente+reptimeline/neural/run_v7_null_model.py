"""Run connections null model on V7 timeline data (72 primitives only).

Uses reptimeline's permutation test to check if connections between
primitivos are above random chance. O/E ≈ 1.0 means connections are
at chance level (consistent with MNIST and Pythia backends).
"""
import json
import sys
import time

sys.path.insert(0, r"C:\Github\reptimeline")

from reptimeline.core import ConceptSnapshot, Timeline
from reptimeline.tracker import TimelineTracker

TIMELINE_PATH = r"C:\Github\dualidad_emergente\dualidademergente+reptimeline\neural\results\timeline_v7.json"
GOLD_PATH = r"C:\Github\dualidad_emergente\dualidademergente+reptimeline\model\gold_extended_v7.json"

def main():
    # Load gold to get primitivo names (capa 1-6)
    print("Loading gold file...")
    with open(GOLD_PATH, "r", encoding="utf-8") as f:
        gold = json.load(f)
    primitivos = [c for c in gold if gold[c].get("capa", 0) >= 1]
    print(f"  {len(primitivos)} primitivos (capas 1-6)")

    # Load timeline (1.9GB — may take a minute)
    print("Loading timeline_v7.json...")
    t0 = time.time()
    timeline = Timeline.load_json(TIMELINE_PATH)
    print(f"  Loaded in {time.time()-t0:.1f}s — {len(timeline.snapshots)} snapshots")

    # Filter snapshots to only primitivo concepts
    filtered_snapshots = []
    prim_set = set(primitivos)
    for snap in timeline.snapshots:
        filtered_codes = {k: v for k, v in snap.codes.items() if k in prim_set}
        filtered_snapshots.append(ConceptSnapshot(
            step=snap.step,
            codes=filtered_codes,
            metadata=snap.metadata,
        ))
    n_concepts = len(filtered_snapshots[-1].codes)
    n_pairs = n_concepts * (n_concepts - 1) // 2
    print(f"  Filtered to {n_concepts} concepts, {n_pairs} pairs")

    # Minimal extractor — only needs shared_features for null model
    class BinaryExtractor:
        def shared_features(self, code_a, code_b):
            return [i for i in range(min(len(code_a), len(code_b)))
                    if code_a[i] == 1 and code_b[i] == 1]

    tracker = TimelineTracker(extractor=BinaryExtractor())

    # First: quick run with 100 permutations
    print("\nRunning null model (100 permutations)...")
    t0 = time.time()
    result_100 = tracker.connections_null_model(
        filtered_snapshots, n_permutations=100, seed=42
    )
    elapsed = time.time() - t0
    print(f"  Done in {elapsed:.1f}s")
    print(f"  Observed: {result_100['n_observed']}")
    print(f"  Expected: {result_100['n_expected']:.1f} ± {result_100['null_std']:.1f}")
    print(f"  O/E ratio: {result_100['oe_ratio']:.3f}")
    print(f"  p-value: {result_100['null_p_value']:.4f}")
    print(f"  Kill K3 (O/E < 1.5): {result_100['kill_k3']}")

    # If fast enough, run 1000 permutations
    if elapsed < 120:
        print("\nRunning null model (1000 permutations)...")
        t0 = time.time()
        result_1000 = tracker.connections_null_model(
            filtered_snapshots, n_permutations=1000, seed=42
        )
        print(f"  Done in {time.time()-t0:.1f}s")
        print(f"  Observed: {result_1000['n_observed']}")
        print(f"  Expected: {result_1000['n_expected']:.1f} ± {result_1000['null_std']:.1f}")
        print(f"  O/E ratio: {result_1000['oe_ratio']:.3f}")
        print(f"  p-value: {result_1000['null_p_value']:.4f}")
        print(f"  Kill K3 (O/E < 1.5): {result_1000['kill_k3']}")

        # Save results
        out_path = r"C:\Github\dualidad_emergente\dualidademergente+reptimeline\neural\results\v7_connections_null.json"
        with open(out_path, "w") as f:
            json.dump(result_1000, f, indent=2)
        print(f"\nSaved to {out_path}")
    else:
        out_path = r"C:\Github\dualidad_emergente\dualidademergente+reptimeline\neural\results\v7_connections_null.json"
        with open(out_path, "w") as f:
            json.dump(result_100, f, indent=2)
        print(f"\nSaved to {out_path}")

if __name__ == "__main__":
    main()
