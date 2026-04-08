@echo off
:loop
cls
echo === V8 Training Monitor ===
echo.

set LOG=C:\Github\dualidad_emergente\dualidademergente+reptimeline\model\checkpoints\v8_deep\training_log.csv

if not exist "%LOG%" (
    echo Training hasn't started yet. No log file found.
    echo Expected: %LOG%
    echo.
    echo Press any key to retry...
    pause >nul
    goto loop
)

echo Last 5 entries:
echo.
for /f "skip=1 tokens=1-12 delims=," %%a in ('more +1 "%LOG%"') do (
    set S=%%a
    set L=%%b
    set BA=%%h
    set SU=%%j
    set DB=%%k
    set EN=%%l
)
echo Step: %S%  Loss: %L%  BitAcc_test: %BA%  Sub_test: %SU%  DeadBits: %DB%  Entropy: %EN%
echo.

type "%LOG%" | find /c ","
echo eval entries logged
echo.
echo Press any key to refresh...
pause >nul
goto loop
