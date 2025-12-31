"""Compatibility package for database module imports.

This package exists so code that imports `app.database.connection`
works on filesystems and environments where the existing folder is
named `Database` (capital D).
"""

from . import connection
