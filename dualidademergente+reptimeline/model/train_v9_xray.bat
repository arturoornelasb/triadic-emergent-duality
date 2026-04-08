@echo off
REM V9_xray Paso 1: Radiografia de la transicion de fase
REM Reentrenar desde step 5K hasta 15K con checkpoints cada 1000 steps
REM Objetivo: ver si la explosion (churn 0->1.0) es instantanea o tiene micro-secuencia
REM
REM Despues de correr, ejecutar: save_v9_xray_timeline.py
REM Si se identifica el rango exacto, crear train_v9_xray_zoom.bat para ese rango
REM
REM Nota: NO modifica v9_neo_openwebtext. Checkpoints van a v9_xray/

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
  --steps 15000 ^
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
  --run-name v9_xray ^
  --save-every 1000 ^
  --eval-every 500 ^
  --print-every 50 ^
  --dtype bfloat16 ^
  --seed 42 ^
  --no-compile ^
  --resume checkpoints/v9_neo_openwebtext/step_5000.pt
pause
