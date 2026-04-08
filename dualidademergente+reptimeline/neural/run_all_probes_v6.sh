#!/bin/bash
# Run all 8 neural probes on v6 checkpoints (72-bit, 2166 concepts, GPT-2 Medium)
#
# Prerequisites:
#   pip install reptimeline torch transformers
#
# Usage:
#   cd C:/Github/dualidad_emergente/dualidademergente+reptimeline/neural
#   bash run_all_probes_v6.sh

set -e

CKPT_DIR="../model/checkpoints/gpt2_triadic_72_v6"
VOCAB="../model/gold_primitivos_72.json"
RESULTS_DIR="results/v6"

mkdir -p "$RESULTS_DIR"

echo "=== Neural Probes v6 (72-bit, 2166 concepts) ==="
echo "Checkpoints: $CKPT_DIR"
echo "Results: $RESULTS_DIR"
echo ""

echo "[1/8] Q1: Layer order emergence..."
python q1_probe_layer_order.py --checkpoints "$CKPT_DIR" --vocab "$VOCAB" \
  > "$RESULTS_DIR/q1_layer_order.txt" 2>&1 && echo "  DONE" || echo "  FAILED"

echo "[2/8] Q2: Dual anti-correlation..."
python q2_probe_duals.py --checkpoints "$CKPT_DIR" \
  > "$RESULTS_DIR/q2_duals.txt" 2>&1 && echo "  DONE" || echo "  FAILED"

echo "[3/8] Q3: DAG recovery..."
python q3_probe_dag.py --checkpoints "$CKPT_DIR" \
  > "$RESULTS_DIR/q3_dag.txt" 2>&1 && echo "  DONE" || echo "  FAILED"

echo "[4/8] Q4: Triadic composition..."
python q4_probe_triadic.py --checkpoints "$CKPT_DIR" \
  > "$RESULTS_DIR/q4_triadic.txt" 2>&1 && echo "  DONE" || echo "  FAILED"

echo "[5/8] Q5: Phase transitions..."
python q5_probe_phases.py --checkpoints "$CKPT_DIR" \
  > "$RESULTS_DIR/q5_phases.txt" 2>&1 && echo "  DONE" || echo "  FAILED"

echo "[6/8] Q6: Unsupervised clustering..."
python q6_probe_unsupervised.py --checkpoints "$CKPT_DIR" \
  > "$RESULTS_DIR/q6_unsupervised.txt" 2>&1 && echo "  DONE" || echo "  FAILED"

echo "[7/8] Q7: Causal pathways..."
python q7_probe_causal.py --checkpoints "$CKPT_DIR" \
  > "$RESULTS_DIR/q7_causal.txt" 2>&1 && echo "  DONE" || echo "  FAILED"

echo "[8/8] Q8: Cross-architecture transfer..."
python q8_probe_crossarch.py --checkpoints "$CKPT_DIR" \
  > "$RESULTS_DIR/q8_crossarch.txt" 2>&1 && echo "  DONE" || echo "  FAILED"

echo ""
echo "=== All probes complete. Results in $RESULTS_DIR ==="
