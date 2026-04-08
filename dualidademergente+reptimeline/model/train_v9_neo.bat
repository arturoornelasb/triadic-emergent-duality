@echo off
call conda activate triadic-microgpt
cd /d C:\Github\dualidad_emergente\dualidademergente+reptimeline\model
python train.py ^
  --model EleutherAI/gpt-neo-125m ^
  --bits 72 ^
  --head-mode deep ^
  --activation ifsq ^
  --freeze-base ^
  --hf-dataset Skylion007/openwebtext ^
  --max-docs 100000 ^
  --steps 50000 ^
  --batch-size 48 ^
  --accum-steps 1 ^
  --lr 0.0003 ^
  --lr-min-ratio 0.03 ^
  --alpha 0.05 ^
  --entropy-weight 3.0 ^
  --align-weight 5.0 ^
  --sup-weight 2.0 ^
  --sub-weight 5.0 ^
  --triadic-warmup-pct 0.1 ^
  --contrast-weight 0.3 ^
  --n-sample 128 ^
  --anchor-weight 50.0 ^
  --gold-file gold_extended_v7.json ^
  --run-name v9_neo_openwebtext ^
  --save-every 5000 ^
  --eval-every 1000 ^
  --dtype bfloat16 ^
  --seed 42 ^
  --no-compile
pause
