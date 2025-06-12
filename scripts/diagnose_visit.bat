@echo off
echo ========================================
echo VISIT Application Diagnostic Tool
echo ========================================
echo.

set BASE_DIR=E:\Personal Projects\VISIT-Museum-App

echo Checking VISIT installation...
echo Base Directory: %BASE_DIR%
echo.

REM Check if base directory exists
if not exist "%BASE_DIR%" (
    echo ❌ ERROR: Base directory not found!
    echo Expected: %BASE_DIR%
    goto :end
)
echo ✅ Base directory found

REM Check app directory
if not exist "%BASE_DIR%\app" (
    echo ❌ ERROR: App directory not found!
    goto :end
)
echo ✅ App directory found

REM Check for visit_app.py
if not exist "%BASE_DIR%\app\visit_app.py" (
    echo ❌ ERROR: visit_app.py not found!
    echo You need to copy visit_app.py to: %BASE_DIR%\app\
    goto :end
)
echo ✅ visit_app.py found

REM Check for license.key
if not exist "%BASE_DIR%\app\license.key" (
    echo ❌ ERROR: license.key not found!
    echo You need to generate a license and save it to: %BASE_DIR%\app\license.key
    goto :end
)
echo ✅ license.key found

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python not found or not in PATH!
    goto :end
)
echo ✅ Python found
python --version

REM Check Python packages
echo.
echo Checking required packages...

python -c "import cv2" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ OpenCV not installed
) else (
    echo ✅ OpenCV installed
)

python -c "import mediapipe" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ MediaPipe not installed
) else (
    echo ✅ MediaPipe installed
)

python -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Pygame not installed
) else (
    echo ✅ Pygame installed
)

python -c "import PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Pillow not installed
) else (
    echo ✅ Pillow installed
)

python -c "import numpy" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ NumPy not installed
) else (
    echo ✅ NumPy installed
)

python -c "import cryptography" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Cryptography not installed
) else (
    echo ✅ Cryptography installed
)

echo.
echo ========================================
echo Diagnostic complete!
echo ========================================

:end
echo.
pause