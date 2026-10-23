@echo off
title IRIS 3-Sec Auto Clicker (CLI)
set PYTHONIOENCODING=utf-8
chcp 65001 >nul 2>&1
mode con: cols=120 lines=38 >nul 2>&1
cd /d "%~dp0"
python "%~dp0cli_clicker.py"
pause
