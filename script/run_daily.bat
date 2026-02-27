@echo off
setlocal
cd /d "%~dp0"
where conda >nul 2>&1
if %errorlevel% neq 0 (
  echo conda not found in PATH
  pause
  exit /b 1
)
call conda activate wd
pip install -r requirements.txt
python main.py --run-now
set EC=%ERRORLEVEL%
pause
exit /b %EC%
