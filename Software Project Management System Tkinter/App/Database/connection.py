from app.config import DB_TYPE, DB_CONFIG, MSSQL_CONFIG


class DatabaseUnavailable(Exception):
    pass


class DatabaseConnection:
    _connection = None

    @classmethod
    def get_connection(cls):
        if DB_TYPE.lower() == "mssql":
            return cls._get_mssql_connection()
        return cls._get_mysql_connection()

    @classmethod
    def _get_mysql_connection(cls):
        import mysql.connector

        if cls._connection is None or not getattr(cls._connection, "is_connected", lambda: True)():
            cls._connection = mysql.connector.connect(**DB_CONFIG)
        return cls._connection

    @classmethod
    def _get_mssql_connection(cls):
        cfg = MSSQL_CONFIG
        server = cfg.get("server")
        database = cfg.get("database", "")
        trusted = cfg.get("trusted", True)
        user = cfg.get("user", "")
        password = cfg.get("password", "")

        tried = []

        try:
            import pyodbc

            drivers_to_try = [cfg.get("driver")] if cfg.get("driver") else []
            drivers_to_try += ["ODBC Driver 18 for SQL Server", "ODBC Driver 17 for SQL Server", "SQL Server Native Client 11.0"]

            for drv in drivers_to_try:
                if not drv:
                    continue
                tried.append(drv)
                if trusted:
                    conn_str = f"DRIVER={{{drv}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
                else:
                    conn_str = f"DRIVER={{{drv}}};SERVER={server};DATABASE={database};UID={user};PWD={password};"
                try:
                    raw_conn = pyodbc.connect(conn_str, autocommit=False)
                    cls._connection = _MSSQLConnectionWrapper(raw_conn)
                    return cls._connection
                except Exception:
                    continue
        except Exception:
            pass

        try:
            import pymssql

            try:
                if trusted:
                    raise Exception("pymssql does not support Windows auth in this environment")
                raw_conn = pymssql.connect(server=server, user=user, password=password, database=database)
                cls._connection = _MSSQLConnectionWrapper(raw_conn)
                return cls._connection
            except Exception:
                pass
        except Exception:
            pass

        print("Tried MSSQL drivers:", tried)
        raise DatabaseUnavailable("Could not connect to MSSQL server. Ensure an ODBC driver (ODBC Driver 17/18) is installed and pyodbc is available, or install pymssql and provide credentials.")

        return cls._connection


class _MSSQLConnectionWrapper:
    def __init__(self, raw_conn):
        self._raw = raw_conn

    def cursor(self, dictionary=False):
        return _MSSQLCursorWrapper(self._raw.cursor(), dictionary)

    def commit(self):
        self._raw.commit()

    def rollback(self):
        self._raw.rollback()

    def is_connected(self):
        try:
            self._raw.cursor().execute("SELECT 1")
            return True
        except Exception:
            return False


class _MSSQLCursorWrapper:
    def __init__(self, raw_cursor, dictionary=False):
        self._cur = raw_cursor
        self._dict = dictionary

    def execute(self, query, params=None):
        q = query.replace("%s", "?")
        if params is None:
            return self._cur.execute(q)
        return self._cur.execute(q, params)

    def fetchone(self):
        row = self._cur.fetchone()
        if row is None:
            return None
        if not self._dict:
            return row
        return self._row_to_dict(row)

    def fetchall(self):
        rows = self._cur.fetchall()
        if not self._dict:
            return rows
        return [self._row_to_dict(r) for r in rows]

    def _row_to_dict(self, row):
        cols = [col[0] for col in self._cur.description]
        return {cols[i]: row[i] for i in range(len(cols))}

    def close(self):
        try:
            self._cur.close()
        except Exception:
            pass

    @property
    def rowcount(self):
        return getattr(self._cur, "rowcount", -1)

