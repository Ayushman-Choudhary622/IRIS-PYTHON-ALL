@echo off
title IRIS UNIVERSAL - ULTRA-HD LOGO
chcp 65001 >nul
mode con: cols=120 lines=32
cd /d "%~dp0"

python iris_ascii.py --theme iris --size large

echo.
echo Press any key to exit...
pause >nul
