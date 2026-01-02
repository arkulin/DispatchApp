@echo off
echo ========================================
echo Starting DispatchApp...
echo ========================================
echo.

cd dispatcher_app

REM Try with default python, then with py -3.11 if it fails
python main.py
if %errorlevel% neq 0 (
    echo.
    echo Trying with Python 3.11...
    py -3.11 main.py
)

if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo ERROR: App failed to start
    echo ========================================
    echo.
    echo Make sure you ran INSTALL_WINDOWS_FIXED.bat first!
    echo.
    pause
)
