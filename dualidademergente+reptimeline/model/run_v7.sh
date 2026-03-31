#!/bin/bash
# V7 training configuration
#
# Changes from V6:
#   1. Gold targets: gold_extended_v7.json (100% unique, 0 collisions vs V6's 529)
#   2. Anti-collision loss: contrast_weight=1.0 (prevents learned signature collapse)
#   3. More steps: 200K (V6 had 100K — not enough for 2,166 concepts)
#   4. Higher entropy: 2.0 (V6 had 1.0 — 24 dead bits)
#   5. Earlier triadic warmup: 0.35 (V6 had 0.50 — more triadic learning time)
#   6. Larger sample: 192 (V6 had 128 — more concept pairs per step)
#
# Expected improvements:
#   - Zero gold collisions → model CAN learn unique signatures
#   - Anti-collision loss → model WILL learn unique signatures
#   - More steps → adequate coverage (46 triadic steps/concept vs V6's 24)
#   - Higher entropy → fewer dead bits (target: <15 vs V6's 24)
#
# Hardware: RTX 4060 Ti 16GB, estimated ~24h (V6 took 12h at 100K steps)

conda run -n triadic-microgpt python train.py \
    --model gpt2-medium \
    --freeze-base \
    --bits 72 \
    --head-mode simple \
    --activation ifsq \
    --gold-file gold_extended_v7.json \
    --run-name v7_contrastive \
    --steps 200000 \
    --batch-size 4 \
    --accum-steps 2 \
    --lr 3e-4 \
    --alpha 0.05 \
    --entropy-weight 2.0 \
    --align-weight 5.0 \
    --align-mode infonce \
    --sup-weight 2.0 \
    --sub-weight 5.0 \
    --contrast-weight 1.0 \
    --triadic-warmup-pct 0.35 \
    --anchor-weight 50 \
    --n-sample 192 \
    --eval-every 1000 \
    --save-every 5000 \
    --print-every 50 \
    --dtype bfloat16 \
    --grad-checkpoint \
    "$@"
