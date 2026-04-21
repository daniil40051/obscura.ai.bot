@echo off
cd /d "%~dp0"
py -3.11 --version >nul 2>&1
if errorlevel 1 (
    echo Python 3.11 not found.
    echo Install Python 3.11 and try again.
    pause
    exit /b
)
echo Installing dependencies...
py -3.11 -m ensurepip --upgrade
py -3.11 -m pip install --upgrade pip
py -3.11 -m pip install -r requirements.txt
echo.
echo Done.
pause
