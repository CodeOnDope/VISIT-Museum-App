# VISIT Application Setup Script
# Developed by Dineshkumar Rajendran

from setuptools import setup, find_packages

setup(
    name="visit-museum-app",
    version="1.0.0",
    author="Dineshkumar Rajendran",
    description="Interactive Museum Application with Computer Vision",
    packages=find_packages(),
    install_requires=[
        "opencv-python==4.8.1.78",
        "mediapipe==0.10.7",
        "pygame==2.5.2",
        "Pillow==10.0.1",
        "numpy==1.24.3",
        "cryptography==41.0.7"
    ],
    python_requires="^>=3.8",
)
