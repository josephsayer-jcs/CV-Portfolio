@echo off
setlocal
title QA E-commerce Demo - Setup

echo.
echo ==========================================
echo      QA E-commerce Demo - Setup
echo ==========================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python was not found.
    echo Please install Python 3.10+ and make sure "Add Python to PATH" is enabled.
    echo.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating Python virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Could not create the virtual environment.
        pause
        exit /b 1
    )
)

echo.
echo Installing/updating dependencies...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Dependency installation failed.
    pause
    exit /b 1
)

echo.
echo Creating/resetting the demo database and seed data...
".venv\Scripts\python.exe" seed.py
if errorlevel 1 (
    echo.
    echo ERROR: Database seeding failed.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Setup complete!
echo.
echo Starting the Flask server...
echo Open http://localhost:5000 in your browser.
echo Keep this window open while using the site.
echo Press Ctrl+C to stop the server.
echo ==========================================
echo.

".venv\Scripts\python.exe" run.py

pause
