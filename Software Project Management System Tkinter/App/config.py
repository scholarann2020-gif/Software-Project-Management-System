# Database configuration
# Set DB_TYPE to either "mysql" or "mssql" depending on your server
DB_TYPE = "mssql"

# MySQL config (kept for backwards compatibility)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "spms_db"
}

# MSSQL config - update `server` to your instance and set `trusted` accordingly
MSSQL_CONFIG = {
    # Example server name with instance: r"DESKTOP-69ATCUG\SQLEXPRESS"
    "server": r"DESKTOP-69ATCUG\SQLEXPRESS",
    "database": "SPMS_DB",
    # If True, uses Windows Authentication (Trusted Connection).
    # If False, specify `user` and `password` below.
    "trusted": True,
    "user": "",
    "password": "",
    # ODBC driver to use on Windows. Change if you have a different driver installed.
    "driver": "ODBC Driver 18 for SQL Server"
}
