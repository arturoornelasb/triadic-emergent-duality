@echo off
REM V9_xray Paso 2 (zoom): Alta resolucion de la explosion
REM Reentrenar desde step 5K hasta 6K con checkpoints cada 50 steps
REM Objetivo: ver la micro-secuencia de la explosion (bit_acc 52%%->78%%, sub 0.7%%->96.7%%)
REM
REM Hallazgo de Paso 1: la explosion ocurre entre step 5001 y 5501
REM Este zoom captura 10 snapshots dentro de ese rango
REM
REM Despues de correr, ejecutar: save_v9_xray_zoom_timeline.py
REM
REM Nota: NO modifica v9_neo_openwebtext ni v9_xray.
REM       Checkpoints van a v9_xray_zoom/

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
  --steps 6000 ^
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
  --run-name v9_xray_zoom ^
  --save-every 50 ^
  --eval-every 50 ^
  --print-every 10 ^
  --dtype bfloat16 ^
  --seed 42 ^
  --no-compile ^
  --resume checkpoints/v9_neo_openwebtext/step_5000.pt
pause
