@echo off
title IRIS FINALE - Eye Blink Mouse Clicker
chcp 65001 >nul
mode con: cols=120 lines=36
cd /d "%~dp0"
python eye_clicker.py
pause
