@echo off
echo ========================================
echo DispatchApp - Windows Installation
echo ========================================
echo.
echo This script will install Kivy and run your app.
echo.
pause

echo Installing Kivy...
python -m pip install kivy[base]==2.3.0
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install Kivy.
    echo Make sure Python is installed and added to PATH.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation complete!
echo ========================================
echo.
echo To run the app, use: RUN_APP.bat
echo Or manually run: python dispatcher_app\main.py
echo.
pause
