@echo.
echo ========================================
echo ✅ Virtual Environment Setup Complete!
echo ========================================
echo.
echo Virtual Environment Location: %PROJECT_DIR%\venv
echo.
echo To use VISIT application:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Navigate to app folder: cd app
echo 3. Run application: python visit_app.py
echo.
echo To deactivate virtual environment later: deactivate
echo.
echo Creating activation shortcut...

REM Create a shortcut script for easy activation
(
echo @echo off
echo echo Activating VISIT Virtual Environment...
echo cd /d "%PROJECT_DIR%"
echo call venv\Scripts\activate
echo echo.
echo echo ========================================
echo echo VISIT Virtual Environment Activated!
echo echo ========================================
echo echo.
echo echo You can now run:
echo echo   cd app
echo echo   python visit_app.py
echo echo.
echo echo To deactivate: deactivate
echo echo.
) > "activate_visit_env.bat"

echo ✅ Created activation shortcut: activate_visit_env.bat
echo.
pause off
echo ========================================
echo VISIT Virtual Environment Setup
echo Developed by Dineshkumar Rajendran
echo ========================================
echo.

set PROJECT_DIR=E:\Personal Projects\VISIT-Museum-App

echo Setting up virtual environment for VISIT...
echo Project Directory: %PROJECT_DIR%
echo.

REM Navigate to project directory
cd /d "%PROJECT_DIR%"

REM Check if virtual environment already exists
if exist "venv" (
    echo Virtual environment already exists!
    echo Do you want to recreate it? (This will delete the existing one)
    choice /C YN /M "Press Y for Yes, N for No"
    if errorlevel 2 goto :activate_existing
    echo Removing existing virtual environment...
    rmdir /s /q venv
)

echo Creating new virtual environment...
python -m venv venv

if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment!
    echo Make sure Python is installed and accessible.
    pause
    exit /b 1
)

echo ✅ Virtual environment created successfully!
echo.

:activate_existing
echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Installing VISIT dependencies in virtual environment...
echo This may take a few minutes...
echo.

echo [1/6] Installing NumPy (compatible version)...
pip install "numpy<2.0"

echo [2/6] Installing OpenCV...
pip install opencv-python==4.10.0.84

echo [3/6] Installing MediaPipe...
pip install mediapipe==0.10.14

echo [4/6] Installing Pygame...
pip install pygame>=2.5.0

echo [5/6] Installing Pillow...
pip install Pillow>=10.0.0

echo [6/6] Installing Cryptography...
pip install cryptography>=41.0.0

echo.
echo ========================================
echo Verifying installation...
echo ========================================

python -c "import numpy; print('✅ NumPy:', numpy.__version__)"
python -c "import cv2; print('✅ OpenCV:', cv2.__version__)"
python -c "import mediapipe; print('✅ MediaPipe:', mediapipe.__version__)"
python -c "import pygame; print('✅ Pygame:', pygame.version.ver)"
python -c "import PIL; print('✅ Pillow:', PIL.__version__)"
python -c "import cryptography; print('✅ Cryptography installed')"

echo