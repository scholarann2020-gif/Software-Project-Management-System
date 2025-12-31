from app.Database.connection import DatabaseConnection
import logging


class AuthService:

    @staticmethod
    def login(username, password):
        """Attempt DB login; on DB error, allow a local fallback admin/admin user.

        This makes the GUI runnable without DB setup. Remove fallback in
        production or when DB is available.
        """
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (username, password)
            )
            return cursor.fetchone()
        except Exception as e:
            logging.warning("DB auth failed, using fallback auth: %s", e)
            # lightweight fallback for local runs
            if username == "admin" and password == "admin":
                return {"id": 0, "username": "admin", "role": "admin"}
            return None
