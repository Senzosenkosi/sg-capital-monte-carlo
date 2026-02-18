@echo off
REM SG Capital Monte Carlo UI - Quick Start Script
REM This script sets up and runs the Streamlit web interface

echo.
echo ========================================
echo SG Capital Monte Carlo Analysis Platform
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Checking dependencies...
python -m pip install -q --upgrade streamlit pandas numpy matplotlib seaborn 2>nul

if errorlevel 1 (
    echo.
    echo Installing dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Starting Streamlit application...
echo Opening http://localhost:8501 in your browser...
echo.

streamlit run app.py

pause
