@echo off
echo ========================================
echo VISIT Application Dependencies Installer
echo Developed by Dineshkumar Rajendran
echo ========================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing VISIT dependencies...
echo This may take a few minutes...
echo.

echo [1/6] Installing OpenCV...
pip install opencv-python>=4.8.0

echo [2/6] Installing MediaPipe...
pip install mediapipe>=0.10.13

echo [3/6] Installing Pygame...
pip install pygame>=2.5.0

echo [4/6] Installing Pillow...
pip install Pillow>=10.0.0

echo [5/6] Installing NumPy...
pip install numpy>=1.24.0

echo [6/6] Installing Cryptography...
pip install cryptography>=41.0.0

echo.
echo ========================================
echo Verifying installation...
echo ========================================

python -c "import cv2; print('✅ OpenCV:', cv2.__version__)"
python -c "import mediapipe; print('✅ MediaPipe:', mediapipe.__version__)"
python -c "import pygame; print('✅ Pygame:', pygame.version.ver)"
python -c "import PIL; print('✅ Pillow:', PIL.__version__)"
python -c "import numpy; print('✅ NumPy:', numpy.__version__)"
python -c "import cryptography; print('✅ Cryptography installed successfully')"

echo.
echo ========================================
echo ✅ Dependencies installation completed!
echo ========================================
echo.
echo You can now run the VISIT application using:
echo   scripts\run_visit.bat
echo.
echo Or manually with:
echo   cd app
echo   python visit_app.py
echo.
pause