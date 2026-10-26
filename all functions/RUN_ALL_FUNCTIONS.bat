@echo off
title IRIS ALL-FUNCTIONS ASSISTIVE CONTROLLER & KEYBOARD
set PYTHONIOENCODING=utf-8
chcp 65001 >nul 2>&1
mode con: cols=120 lines=38 >nul 2>&1
color 0B
cls
cd /d "%~dp0"

echo ================================================================================
echo           👁️ PROJECT IRIS // ALL-FUNCTIONS ASSISTIVE DESKTOP SUITE
echo ================================================================================
echo   Initializing Universal On-Screen Virtual Keyboard, Scroll Suite & Actions...
echo ================================================================================
echo.

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python "%~dp0iris_all_functions.py"
    goto :end
)

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py "%~dp0iris_all_functions.py"
    goto :end
)

color 0C
echo [ERROR] Python was not found in your system PATH.
echo Please install Python 3.10+ and check "Add Python to PATH".
echo.
pause
exit /b 1

:end
echo.
echo [!] IRIS Assistive Controller Session Terminated.
pause
