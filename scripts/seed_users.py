"""Seed script to insert sample users into the configured database.

Usage (from workspace root):
    python scripts/seed_users.py

This uses the project's `app.config` and `app.Database.connection.DatabaseConnection`.
"""
import sys
from pathlib import Path

# Make `app` importable when running from `scripts/`
repo_root = Path(__file__).resolve().parents[1]
tk_dir = repo_root / "Software Project Management System Tkinter"
if tk_dir.exists():
    sys.path.insert(0, str(tk_dir))
else:
    if (repo_root / "app").exists():
        sys.path.insert(0, str(repo_root))

from app.config import DB_TYPE
from app.Database.connection import DatabaseConnection

SAMPLE_USERS = [
    ("admin", "admin123", "Admin"),
    ("user", "user123", "User"),
]


def seed():
    conn = DatabaseConnection.get_connection()
    cur = conn.cursor()

    # Create table if it doesn't exist (simple schema)
    try:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT IDENTITY(1,1) PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(50) NULL
            )
            """
        )
    except Exception:
        # Some DB backends (e.g., sqlite/mysql) may use different DDL; ignore errors
        pass

    # Insert sample users if not present
    for username, password, role in SAMPLE_USERS:
        try:
            # Use parameterized query; DatabaseConnection wrapper expects %s
            cur.execute("SELECT id FROM users WHERE username=%s", (username,))
            exists = cur.fetchone()
            if not exists:
                cur.execute(
                    "INSERT INTO users (username, password, role) VALUES (%s,%s,%s)",
                    (username, password, role),
                )
        except Exception as e:
            # best-effort reporting
            print(f"Warning: could not insert {username}: {e}")

    try:
        conn.commit()
    except Exception:
        pass

    try:
        cur.close()
    except Exception:
        pass

    print("Seeding finished.")


if __name__ == "__main__":
    seed()
