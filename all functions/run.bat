@echo off
title IRIS All Functions
set PYTHONIOENCODING=utf-8
chcp 65001 >nul 2>&1
cd /d "%~dp0"

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

echo [ERROR] Python not found in PATH.
pause
:end
