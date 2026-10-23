@echo off
title IRIS 3-Sec Universal Auto Clicker
set PYTHONIOENCODING=utf-8
chcp 65001 >nul 2>&1
mode con: cols=120 lines=38 >nul 2>&1
cd /d "%~dp0"

python "%~dp0autoclicker.py"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] Python failed to launch with standard 'python'. Trying 'py'...
    py "%~dp0autoclicker.py"
)

pause
