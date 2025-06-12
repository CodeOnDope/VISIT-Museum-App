@echo off
echo ========================================
echo VISIT Application Dependencies Installer
echo ========================================
echo.
echo Installing Python dependencies...
pip install --upgrade pip
pip install opencv-python==4.8.1.78
pip install mediapipe==0.10.7
pip install pygame==2.5.2
pip install Pillow==10.0.1
pip install numpy==1.24.3
pip install cryptography==41.0.7
echo.
echo Dependencies installation completed!
echo You can now run the VISIT application.
pause
