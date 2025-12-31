import sys
from pathlib import Path
import tkinter as tk

# Ensure project root is on sys.path so 'views' can be imported when running this script directly
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from app.views.login_view import LoginView
except Exception:
    # fallback: load LoginView directly from file if package import fails
    import importlib.util

    login_path = Path(__file__).resolve().parent / "views" / "login_view.py"
    spec = importlib.util.spec_from_file_location("login_view", str(login_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    LoginView = getattr(module, "LoginView")


if __name__ == "__main__":
    root = tk.Tk()
    try:
        LoginView(root)
        root.mainloop()
    except Exception as e:
        import traceback

        traceback.print_exc()
        # Do not show raw exception details (like driver errors) in the UI
        tk.messagebox.showerror(
            "Startup Error",
            "Failed to start application. See console/logs for details."
        )
