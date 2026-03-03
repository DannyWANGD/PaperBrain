@echo off
setlocal
cd /d "%~dp0"
set "LOCKDIR=%~dp0.run_daily.lock"
mkdir "%LOCKDIR%" >nul 2>&1
if %errorlevel% neq 0 (
  echo Another PaperBrain run is already in progress.
  echo Close any running cmd/python for PaperBrain, then delete "%LOCKDIR%" if needed.
  pause
  exit /b 1
)
where conda >nul 2>&1
if %errorlevel% neq 0 (
  echo conda not found in PATH
  set EC=1
  goto :cleanup
)
call conda activate wd
pip install -r requirements.txt
python main.py --run-now
set EC=%ERRORLEVEL%
:cleanup
rmdir "%LOCKDIR%" >nul 2>&1
exit /b %EC%
