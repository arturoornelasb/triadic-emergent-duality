@echo off
cd /d C:\Github\dualidad_emergente\dualidademergente+reptimeline\model
conda run -n triadic-microgpt python train.py ^
    --model gpt2-medium ^
    --freeze-base ^
    --bits 72 ^
    --head-mode simple ^
    --activation ifsq ^
    --gold-file gold_extended_v7.json ^
    --run-name v7_contrastive ^
    --steps 200000 ^
    --batch-size 4 ^
    --accum-steps 2 ^
    --lr 3e-4 ^
    --alpha 0.05 ^
    --entropy-weight 2.0 ^
    --align-weight 5.0 ^
    --align-mode infonce ^
    --sup-weight 2.0 ^
    --sub-weight 5.0 ^
    --contrast-weight 1.0 ^
    --triadic-warmup-pct 0.35 ^
    --anchor-weight 50 ^
    --n-sample 128 ^
    --eval-every 1000 ^
    --save-every 5000 ^
    --print-every 50 ^
    --dtype bfloat16 ^
    --grad-checkpoint
pause
