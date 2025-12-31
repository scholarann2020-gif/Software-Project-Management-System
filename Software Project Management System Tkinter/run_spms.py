"""Launcher for the SPMS Tkinter app.

Usage:
  cd "Software Project Management System Tkinter"
  python run_spms.py

This script ensures the current folder (which contains `app/`) is on `sys.path`
so `import app` works even when IDEs set a different working directory.
"""
import sys
import runpy
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Run the app as a module so `app/main.py` behavior (if __name__ == '__main__') executes
runpy.run_module('app.main', run_name='__main__')
