@echo off
echo ========================================
echo DispatchApp - Windows Installation (FIXED)
echo ========================================
echo.
echo This script will try to install the latest Kivy.

echo.
pause

echo Installing latest Kivy...
python -m pip install kivy[base]
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo ERROR: Failed to install latest Kivy.
    echo ========================================
    echo.
    echo This is likely because you are using Python 3.13, which is not yet fully supported by Kivy.
    echo.
    echo To fix this, please install Python 3.11 from python.org:
    echo https://www.python.org/downloads/release/python-3119/
    echo.
    echo During installation, make sure to check "Add Python to PATH".
    echo.
    echo After installing Python 3.11, run this command in a new terminal:
    echo py -3.11 -m pip install kivy[base]==2.3.0
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
