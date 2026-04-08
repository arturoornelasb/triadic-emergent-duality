@echo off
echo ================================================================
echo   V9 FULL EVALUATION PIPELINE
echo   GPT-Neo 125M / OpenWebText / 72-bit / 50K steps
echo   Addresses: Debilidades #5 (N=1), #6 (Q1/Q2 NULL), #7 (FEP fit)
echo ================================================================
echo.

cd /d "%~dp0"
call conda activate triadic-microgpt

echo ────────────────────────────────────────────────────────────
echo  STEP 1: Extract reptimeline (timeline, curves, plots)
echo ────────────────────────────────────────────────────────────
python save_v9_timeline.py
if errorlevel 1 (
    echo FAILED: save_v9_timeline.py
    echo Continuing anyway...
)
echo.

echo ────────────────────────────────────────────────────────────
echo  STEP 2: Fit FEP wave to entropy curve (Roadmap #12)
echo ────────────────────────────────────────────────────────────
python fit_wave_fep_v9.py
if errorlevel 1 (
    echo FAILED: fit_wave_fep_v9.py
    echo Continuing anyway...
)
echo.

echo ────────────────────────────────────────────────────────────
echo  STEP 3: Run 8 neural probes (Q1-Q8)
echo ────────────────────────────────────────────────────────────
cd /d "%~dp0\..\neural"
call run_all_probes_v9.bat nopause
echo.

echo ================================================================
echo   EVALUATION COMPLETE
echo ================================================================
echo.
echo   Results:
echo     Timeline:   ..\neural\results\timeline_v9.json
echo     Curves:     ..\neural\results\v9_curves.csv
echo     FEP fit:    ..\neural\results\v9_fep_wave_fit.json
echo     Probes:     ..\neural\results\v9\q*.txt
echo     Plots:      ..\runs\v9_neo\plots\
echo.
echo   KEY CHECKS:
echo     1. Crystallization detected?     (timeline_v9.json)
echo     2. Q5 replicates (p less 0.05)?  (results\v9\q5_phases.txt)
echo     3. Q1 or Q2 flip?               (results\v9\q1/q2*.txt)
echo     4. Wave preferred over exp?      (v9_fep_wave_fit.json)
echo     5. Genuine oscillation (f greater 0)? (v9_fep_wave_fit.json)
echo.
pause
