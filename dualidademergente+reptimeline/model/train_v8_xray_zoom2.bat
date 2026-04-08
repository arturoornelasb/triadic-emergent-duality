@echo off
REM V8_xray Paso 3: Ultra-zoom en la explosion (step 30000-30150)
REM Reentrenar desde step 30K con checkpoints cada 5 steps
REM V8_xray zoom detecto explosion entre 30050 y 30100 (churn 0->0.53)
REM Extendemos a 30150 para capturar oleadas post-explosion
REM
REM Despues de correr, ejecutar: save_v8_xray_zoom2_timeline.py
REM
REM Nota: NO modifica v8_deep, v8_xray ni v8_xray_zoom. Checkpoints van a v8_xray_zoom2/

call conda activate triadic-microgpt
cd /d C:\Github\dualidad_emergente\dualidademergente+reptimeline\model
python train.py ^
  --model gpt2-medium ^
  --bits 72 ^
  --head-mode deep ^
  --activation ifsq ^
  --freeze-base ^
  --steps 30150 ^
  --batch-size 4 ^
  --accum-steps 2 ^
  --lr 0.0003 ^
  --lr-min-ratio 0.03 ^
  --alpha 0.05 ^
  --entropy-weight 3.0 ^
  --align-weight 5.0 ^
  --align-mode infonce ^
  --sup-weight 2.0 ^
  --sub-weight 5.0 ^
  --triadic-warmup-pct 0.1 ^
  --contrast-weight 0.3 ^
  --n-sample 128 ^
  --anchor-weight 50.0 ^
  --gold-file gold_extended_v7.json ^
  --run-name v8_xray_zoom2 ^
  --save-every 5 ^
  --eval-every 5 ^
  --print-every 5 ^
  --dtype bfloat16 ^
  --grad-checkpoint ^
  --resume checkpoints/v8_deep/step_30000.pt
pause
