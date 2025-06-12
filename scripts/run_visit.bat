@echo off
echo ========================================
echo VISIT Interactive Museum Application
echo Starting Application...
echo ========================================
echo.
cd /d "%~dp0..\app"
if exist "license.key" (
    echo License found. Starting VISIT...
    python visit_app.py
) else (
    echo ERROR: License file not found!
    echo Please place a valid license.key file in the app/ folder.
    echo Contact the software owner for a license.
    pause
)
