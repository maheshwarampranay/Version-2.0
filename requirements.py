import sys
import subprocess
import shutil
import os

REQUIRED_PACKAGES = [
    "fastapi>=0.100.0",
    "uvicorn>=0.22.0",
    "python-multipart>=0.0.6",
    "pydantic>=2.0.0",
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "scikit-learn>=1.2.0",
    "openpyxl>=3.1.0",
    "jinja2>=3.1.0",
    "reportlab>=4.0.0",
    "requests>=2.31.0"
]

def check_and_install_python_packages():
    print("=" * 60)
    print("   Checking & Installing Python Dependencies (Fairness Pipeline)")
    print("=" * 60)
    
    python_exe = sys.executable
    print(f"Using Python executable: {python_exe}\n")
    
    for pkg in REQUIRED_PACKAGES:
        pkg_name = pkg.split(">=")[0].split("==")[0]
        print(f"Checking package: {pkg_name} ...", end=" ")
        try:
            __import__(pkg_name.replace("-", "_"))
            print("[ INSTALLED ]")
        except ImportError:
            print(f"[ MISSING ] -> Installing {pkg} ...")
            subprocess.check_call([python_exe, "-m", "pip", "install", pkg])

def check_node_environment():
    print("\n" + "=" * 60)
    print("   Checking Node.js & Frontend Dependencies")
    print("=" * 60)
    
    node_path = shutil.which("node")
    npm_path = shutil.which("npm")
    
    if node_path:
        print(f"[OK] Node.js found at: {node_path}")
    else:
        print("[WARNING] Node.js not found in PATH! Please ensure Node.js is installed for frontend development.")
        
    if npm_path:
        print(f"[OK] npm found at: {npm_path}")
        frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
        node_modules = os.path.join(frontend_dir, "node_modules")
        
        if not os.path.exists(node_modules):
            print("\nInstalling frontend npm dependencies...")
            subprocess.check_call(["npm", "install"], cwd=frontend_dir, shell=True)
            print("[OK] Frontend npm dependencies installed successfully.")
        else:
            print("[OK] Frontend node_modules already exists.")
    else:
        print("[WARNING] npm not found in PATH!")

if __name__ == "__main__":
    check_and_install_python_packages()
    check_node_environment()
    print("\n" + "=" * 60)
    print("   All requirements verified successfully!")
    print("   You can now launch the app with: python run_app.py")
    print("=" * 60)
