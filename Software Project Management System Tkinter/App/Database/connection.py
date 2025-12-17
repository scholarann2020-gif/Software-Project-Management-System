import mysql.connector
from app.config import DB_CONFIG


class DatabaseConnection:
    _connection = None

    @classmethod
    def get_connection(cls):
        if cls._connection is None or not cls._connection.is_connected():
            cls._connection = mysql.connector.connect(**DB_CONFIG)
        return cls._connection
