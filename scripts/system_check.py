# System Requirements Checker for VISIT
# Developed by Dineshkumar Rajendran

import sys
import subprocess
import platform

def check_python_version():
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python 3.8+ required")
        return False

def check_dependencies():
    deps = ['opencv-python', 'mediapipe', 'pygame', 'Pillow', 'numpy', 'cryptography']
    missing = []
    for dep in deps:
        try:
            __import__(dep.replace('-', '_'))
            print(f"✅ {dep} is installed")
        except ImportError:
            print(f"❌ {dep} is missing")
            missing.append(dep)
    return missing

if __name__ == "__main__":
    print("VISIT System Requirements Check")
    print("="*40)
ECHO is off.
    print(f"Operating System: {platform.system^(^)} {platform.release^(^)}")
ECHO is off.
    python_ok = check_python_version()
    missing_deps = check_dependencies()
ECHO is off.
    if python_ok and not missing_deps:
        print("\n🎉 System is ready for VISIT!")
    else:
        print("\n⚠️ Please install missing requirements")
