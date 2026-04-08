@echo off
REM V8_xray Paso 1: Radiografia de la transicion de fase en v8 (GPT-2 Medium)
REM Reentrenar desde step 30K hasta 45K con checkpoints cada 1000 steps
REM Objetivo: localizar la explosion (churn 0->1.0 reportada en step 35K)
REM
REM Despues de correr, ejecutar: save_v8_xray_timeline.py
REM Si se identifica el rango exacto, crear train_v8_xray_zoom.bat para ese rango
REM
REM Nota: NO modifica v8_deep. Checkpoints van a v8_xray/
REM Nota: v8 usa gpt2-medium, TinyStories (sin --hf-dataset = usa corpus local)

call conda activate triadic-microgpt
cd /d C:\Github\dualidad_emergente\dualidademergente+reptimeline\model
python train.py ^
  --model gpt2-medium ^
  --bits 72 ^
  --head-mode deep ^
  --activation ifsq ^
  --freeze-base ^
  --steps 45000 ^
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
  --run-name v8_xray ^
  --save-every 1000 ^
  --eval-every 500 ^
  --print-every 50 ^
  --dtype bfloat16 ^
  --grad-checkpoint ^
  --resume checkpoints/v8_deep/step_30000.pt
pause
