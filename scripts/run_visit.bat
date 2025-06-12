@echo off
echo ========================================
echo VISIT Interactive Museum Application
echo Developed by Dineshkumar Rajendran
echo ========================================
echo.

REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0
set APP_DIR=%SCRIPT_DIR%..\app

echo Script Directory: %SCRIPT_DIR%
echo App Directory: %APP_DIR%
echo.

REM Check if app directory exists
if not exist "%APP_DIR%" (
    echo ERROR: App directory not found!
    echo Expected: %APP_DIR%
    echo Please ensure the folder structure is correct.
    echo.
    pause
    exit /b 1
)

REM Change to app directory
cd /d "%APP_DIR%"
echo Current Directory: %CD%
echo.

REM Check if visit_app.py exists
if not exist "visit_app.py" (
    echo ERROR: visit_app.py not found!
    echo Please copy visit_app.py to the app folder.
    echo Expected location: %APP_DIR%\visit_app.py
    echo.
    pause
    exit /b 1
)

REM Check if license file exists
if not exist "license.key" (
    echo ERROR: License file not found!
    echo Please generate a license using license_tools\license_generator.py
    echo and save it as 'license.key' in the app folder.
    echo Expected location: %APP_DIR%\license.key
    echo.
    echo Steps to generate license:
    echo 1. cd license_tools
    echo 2. python license_generator.py
    echo 3. Generate license and save as license.key in app folder
    echo.
    pause
    exit /b 1
)

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://python.org
    echo.
    pause
    exit /b 1
)

echo ✅ All checks passed! Starting VISIT application...
echo.
echo Python version:
python --version
echo.
echo License found: %APP_DIR%\license.key
echo Application: %APP_DIR%\visit_app.py
echo.

REM Start the application
echo Starting VISIT Interactive Museum Application...
echo Press Ctrl+C to stop the application
echo.
python visit_app.py

REM If we get here, the application has closed
echo.
echo ========================================
echo VISIT Application has closed.
echo ========================================
if %errorlevel% neq 0 (
    echo Application exited with error code: %errorlevel%
    echo Check the error messages above for details.
)
echo.
pause