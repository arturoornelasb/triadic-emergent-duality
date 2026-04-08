@echo off
REM V8_xray Paso 2: Zoom en la explosion (step 31000-32000)
REM Reentrenar desde step 30K hasta 32K con checkpoints cada 50 steps
REM V8_xray paso 1 detecto explosion entre 31000 y 32000 (churn 0->0.81)
REM
REM Despues de correr, ejecutar: save_v8_xray_zoom_timeline.py
REM Si se identifica el rango exacto, crear train_v8_xray_zoom2.bat
REM
REM Nota: NO modifica v8_deep ni v8_xray. Checkpoints van a v8_xray_zoom/

call conda activate triadic-microgpt
cd /d C:\Github\dualidad_emergente\dualidademergente+reptimeline\model
python train.py ^
  --model gpt2-medium ^
  --bits 72 ^
  --head-mode deep ^
  --activation ifsq ^
  --freeze-base ^
  --steps 32000 ^
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
  --run-name v8_xray_zoom ^
  --save-every 50 ^
  --eval-every 50 ^
  --print-every 50 ^
  --dtype bfloat16 ^
  --grad-checkpoint ^
  --resume checkpoints/v8_deep/step_30000.pt
pause
