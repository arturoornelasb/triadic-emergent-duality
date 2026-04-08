@echo off
REM V9_xray Paso 3 (zoom2): Maxima resolucion de la explosion
REM Reentrenar desde step 5050 hasta 5100 con checkpoints cada 5 steps
REM Objetivo: ver si el salto churn 0.0->1.0 es verdaderamente instantaneo
REM           o si hay una rampa dentro de esos 50 steps
REM
REM Hallazgos previos:
REM   Paso 1: explosion entre step 5001 y 5501 (res 1K)
REM   Paso 2: churn 0->1.0 entre step 5050 y 5100 (res 50)
REM   Paso 3: este — resolucion de 5 steps
REM
REM Despues de correr, ejecutar: save_v9_xray_zoom2_timeline.py
REM
REM Nota: NO modifica v9_neo_openwebtext, v9_xray, ni v9_xray_zoom.
REM       Checkpoints van a v9_xray_zoom2/

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
  --steps 5100 ^
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
  --run-name v9_xray_zoom2 ^
  --save-every 5 ^
  --eval-every 5 ^
  --print-every 1 ^
  --dtype bfloat16 ^
  --seed 42 ^
  --no-compile ^
  --resume checkpoints/v9_xray_zoom/step_5050.pt
pause
