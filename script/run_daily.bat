@echo off
setlocal enabledelayedexpansion

:: --- PaperBrain Auto-Runner ---
:: Author: PaperBrain Team
:: Description: Activates conda environment and runs the daily job.
:: Usage: Can be scheduled via Windows Task Scheduler.

:: 1. Navigate to script directory
cd /d "%~dp0"

:: 2. Singleton Lock Mechanism
set "LOCKDIR=%~dp0.run_daily.lock"
mkdir "%LOCKDIR%" >nul 2>&1
if %errorlevel% neq 0 (
  echo [WARN] Another PaperBrain instance is running. Exiting.
  exit /b 1
)

:: 3. Check for Conda
where conda >nul 2>&1
if %errorlevel% neq 0 (
  echo [ERR] Conda not found in PATH. Please install Anaconda/Miniconda.
  goto :cleanup_error
)

:: 4. Activate Environment
:: Use 'call' to prevent script termination
:: Default to 'wd' if CONDA_ENV is not set
if "%CONDA_ENV%"=="" set CONDA_ENV=wd
call conda activate %CONDA_ENV%
if %errorlevel% neq 0 (
  echo [ERR] Failed to activate conda environment '%CONDA_ENV%'.
  goto :cleanup_error
)

:: 5. Install/Update Dependencies (Optional - can comment out for speed)
:: echo [INFO] Checking dependencies...
:: pip install -r requirements.txt >nul 2>&1

:: 6. Run Main Script
echo [INFO] Starting PaperBrain...
python main.py --run-now --provider openrouter

:: 7. Cleanup & Exit
set EC=%ERRORLEVEL%
rmdir "%LOCKDIR%" >nul 2>&1

if %EC% neq 0 (
    echo [ERR] PaperBrain failed with exit code %EC%.
    pause
) else (
    echo [SUCCESS] PaperBrain finished successfully.
    :: Close window automatically after 10 seconds if successful
    timeout /t 10
)
exit /b %EC%

:cleanup_error
rmdir "%LOCKDIR%" >nul 2>&1
pause
exit /b 1
