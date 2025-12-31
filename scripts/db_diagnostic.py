"""DB diagnostic script — prints available ODBC drivers and attempts to connect.

Run from workspace root:
    python scripts/db_diagnostic.py

Paste the full console output here.
"""
import traceback
import sys
from pathlib import Path

# Make the `app` package importable when running from the `scripts/` folder.
repo_root = Path(__file__).resolve().parents[1]
tk_dir = repo_root / "Software Project Management System Tkinter"
if tk_dir.exists():
    sys.path.insert(0, str(tk_dir))
else:
    # fallback: if `app` is directly under repo root
    if (repo_root / "app").exists():
        sys.path.insert(0, str(repo_root))

try:
    import pyodbc
except Exception:
    pyodbc = None

try:
    import pymssql
except Exception:
    pymssql = None

from app.config import MSSQL_CONFIG

print("MSSQL_CONFIG:", MSSQL_CONFIG)
print()

if pyodbc:
    print("pyodbc available. ODBC drivers installed on this system:")
    try:
        print(pyodbc.drivers())
    except Exception as e:
        print("  (could not list drivers):", e)
else:
    print("pyodbc not installed")

print()

server = MSSQL_CONFIG.get("server")
database = MSSQL_CONFIG.get("database", "")
trusted = MSSQL_CONFIG.get("trusted", True)
user = MSSQL_CONFIG.get("user", "")
password = MSSQL_CONFIG.get("password", "")

# Try configured driver first then common drivers
drivers_to_try = []
if MSSQL_CONFIG.get("driver"):
    drivers_to_try.append(MSSQL_CONFIG.get("driver"))
drivers_to_try += ["ODBC Driver 18 for SQL Server", "ODBC Driver 17 for SQL Server", "SQL Server Native Client 11.0"]

if pyodbc:
    for drv in drivers_to_try:
        if not drv:
            continue
        print(f"Trying driver: {drv}")
        try:
            if trusted:
                conn_str = f"DRIVER={{{drv}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
                print("  Using Windows Authentication (Trusted_Connection=yes)")
                conn = pyodbc.connect(conn_str, timeout=5)
            else:
                conn_str = f"DRIVER={{{drv}}};SERVER={server};DATABASE={database};UID={user};PWD={password};"
                conn = pyodbc.connect(conn_str, timeout=5)
            print("  Connected successfully with pyodbc using", drv)
            conn.close()
            break
        except Exception as e:
            print("  Failed:")
            traceback.print_exc()
            print()
else:
    print("Skipping pyodbc driver attempts (pyodbc not available)")

print()

if pymssql:
    print("Trying pymssql...")
    try:
        if trusted:
            print("  pymssql typically does not support Windows auth — skipping attempt for trusted=True")
        else:
            conn = pymssql.connect(server=server, user=user, password=password, database=database, timeout=5)
            print("  Connected successfully with pymssql")
            conn.close()
    except Exception:
        traceback.print_exc()
else:
    print("pymssql not installed")

print()
print("Diagnostic finished — paste all output here.")
