@echo off
echo ========================================
echo Starting DispatchApp...
echo ========================================
echo.

cd dispatcher_app
python main.py

if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo ERROR: App failed to start
    echo ========================================
    echo.
    echo Make sure you ran INSTALL_WINDOWS.bat first!
    echo.
    pause
)
