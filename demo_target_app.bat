@echo off
title IRIS TARGET SIMULATOR // TEST CONSOLE
color 0A
cls

:MENU
cls
echo ===============================================================================
echo            IRIS TARGET SIMULATOR // INTERACTIVE BATCH CONSOLE
echo ===============================================================================
echo.
echo   This is a sample batch application to test your Iris Auto-Clicker!
echo.
echo   [1] Option 1: System Diagnostic Pulse
echo   [2] Option 2: Quantum Core Status
echo   [3] Option 3: Sound FX Ping
echo   [4] Option 4: Clear Console
echo   [5] Exit Simulator
echo.
echo ===============================================================================
echo.
set /p choice="Select an option (1-5): "

if "%choice%"=="1" goto OPTION1
if "%choice%"=="2" goto OPTION2
if "%choice%"=="3" goto OPTION3
if "%choice%"=="4" goto MENU
if "%choice%"=="5" goto EXIT
echo [!] Invalid option.
timeout /t 1 >nul
goto MENU

:OPTION1
echo.
echo [*] Executing System Diagnostic Pulse...
echo [*] CPU: NOMINAL  |  MEMORY: OPTIMAL  |  RADAR: ACTIVE
echo.
pause
goto MENU

:OPTION2
echo.
echo [*] Quantum Core Status: 99.8%% Synchronization
echo [*] All hover sensors fully calibrated.
echo.
pause
goto MENU

:OPTION3
echo.
echo [*] Sound Ping Triggered!
echo 
pause
goto MENU

:EXIT
echo.
echo [*] Exiting Target Simulator...
timeout /t 1 >nul
exit /b
