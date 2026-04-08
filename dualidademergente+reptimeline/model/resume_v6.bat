@echo off
cd /d C:\Github\dualidad_emergente\dualidademergente+reptimeline\model
C:\Users\arqbu\Miniconda3\envs\triadic-microgpt\python.exe train.py --resume checkpoints/gpt2_triadic_72_v6/step_75000.pt --model gpt2-medium --freeze-base --bits 72 --steps 100000 --batch-size 4 --accum-steps 2 --lr 0.0003 --alpha 0.05 --entropy-weight 1.0 --align-weight 5.0 --align-mode infonce --sup-weight 2.0 --sub-weight 5.0 --triadic-warmup-pct 0.5 --anchor-weight 50.0 --n-sample 128 --gold-file gold_extended_v6.json --run-name gpt2_triadic_72_v6 --save-every 5000 --eval-every 1000 --print-every 50 --dtype bfloat16 --grad-checkpoint
pause
