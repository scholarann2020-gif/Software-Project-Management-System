from app.database.connection import DatabaseConnection


class AuthService:

    @staticmethod
    def login(username, password):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        return cursor.fetchone()
