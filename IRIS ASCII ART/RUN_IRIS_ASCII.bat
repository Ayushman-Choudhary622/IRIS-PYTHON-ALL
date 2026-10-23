@echo off
:: ============================================================================
::  IRIS UNIVERSAL - ULTRA-HD CLAUDE CODE STYLE ASCII ART LAUNCHER
:: ============================================================================
title IRIS UNIVERSAL ASCII ART CONTROLLER
chcp 65001 >nul
mode con: cols=124 lines=36
cd /d "%~dp0"

:: Check if python is available
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python is not installed or not found in system PATH.
    echo Please install Python 3 or add it to PATH.
    pause
    exit /b 1
)

:: Run the interactive IRIS ASCII Art terminal program
python iris_ascii.py --interactive

if %ERRORLEVEL% neq 0 (
    echo.
    echo Program finished.
    pause
)
