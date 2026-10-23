@echo off
title IRIS QUANTUM AUTO-CLICK & HOVER-LOCK SYSTEM
chcp 65001 >nul
mode con: cols=120 lines=38
color 0B
cls
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Python was not found in your system PATH.
    echo Please ensure Python is installed and added to PATH.
    pause
    exit /b
)

python "%~dp0iris_autoclicker.py"

echo.
echo [!] Iris Quantum Auto-Clicker Session Terminated.
pause
