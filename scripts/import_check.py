import sys
import importlib
sys.path.insert(0, r'c:\Users\DIGital\PycharmProjects\Software-Project-Management-System\Software-Project-Management-System\Software Project Management System Tkinter')

try:
    importlib.import_module('app.main')
    print('imported app.main OK')
except Exception:
    import traceback
    traceback.print_exc()
    raise
