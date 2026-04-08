@echo off
REM V8: Deep head + less warmup + LR decay + reduced contrast
REM Based on V7 reptimeline diagnosis (2026-03-31):
REM   - Warmup 10%% (was 35%%) -> 225K effective triadic steps vs 130K
REM   - Deep head (561K params vs 74K) -> more capacity for 2166 concepts
REM   - contrast_weight 0.3 (was 1.0) -> stop fighting supervision
REM   - entropy_weight 3.0 (was 2.0) -> fix 32 persistent dead bits
REM   - lr-min-ratio 0.03 (was 0.1) -> deeper LR decay to fix 71%% churn
REM   - 250K steps (was 200K) -> more total training with less warmup waste
REM
REM Estimated: ~100h on RTX 5060 Ti 16GB (deep head is ~20%% slower)
REM Monitor:   double-click monitor_v8.bat

cd /d C:\Github\dualidad_emergente\dualidademergente+reptimeline\model
C:\Users\arqbu\Miniconda3\envs\triadic-microgpt\python train.py ^
    --model gpt2-medium ^
    --freeze-base ^
    --bits 72 ^
    --head-mode deep ^
    --activation ifsq ^
    --gold-file gold_extended_v7.json ^
    --run-name v8_deep ^
    --steps 250000 ^
    --batch-size 4 ^
    --accum-steps 2 ^
    --lr 3e-4 ^
    --lr-min-ratio 0.03 ^
    --alpha 0.05 ^
    --entropy-weight 3.0 ^
    --align-weight 5.0 ^
    --align-mode infonce ^
    --sup-weight 2.0 ^
    --sub-weight 5.0 ^
    --contrast-weight 0.3 ^
    --triadic-warmup-pct 0.10 ^
    --anchor-weight 50 ^
    --n-sample 128 ^
    --eval-every 1000 ^
    --save-every 5000 ^
    --print-every 50 ^
    --dtype bfloat16 ^
    --grad-checkpoint
pause
