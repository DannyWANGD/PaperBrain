@echo off
cd /d "%~dp0"
:: Change this to your python path if not in system PATH, or activate conda env
:: Example: call conda activate wd
python main.py --run-now
pause