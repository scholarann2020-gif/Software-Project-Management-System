import unittest
from unittest.mock import patch

from app.services.project_service import ProjectService
from app.services.task_service import TaskService


class DummyCursor:
    def __init__(self, rows=None):
        self.queries = []
        self._rows = rows or []

    def execute(self, query, params=None):
        self.queries.append((query, params))

    def fetchall(self):
        return self._rows


class MockConn:
    def __init__(self, cursor):
        self._cursor = cursor
        self.committed = False

    def cursor(self, **kwargs):
        return self._cursor

    def commit(self):
        self.committed = True


class TestServices(unittest.TestCase):

    @patch('app.Database.connection.DatabaseConnection.get_connection')
    def test_project_create_calls_execute_and_commit(self, mock_get_conn):
        cur = DummyCursor()
        conn = MockConn(cur)
        mock_get_conn.return_value = conn

        ProjectService.create_project('TestProj', 'Desc', 'Planned', 42)

        self.assertTrue(cur.queries)
        q, params = cur.queries[0]
        self.assertIn('INSERT INTO projects', q)
        self.assertEqual(params, ('TestProj', 'Desc', 'Planned', 42))
        self.assertTrue(conn.committed)

    @patch('app.Database.connection.DatabaseConnection.get_connection')
    def test_get_projects_returns_rows(self, mock_get_conn):
        rows = [{'id': 1, 'name': 'A'}]
        cur = DummyCursor(rows=rows)
        conn = MockConn(cur)
        mock_get_conn.return_value = conn

        result = ProjectService.get_projects()
        self.assertEqual(result, rows)

    @patch('app.Database.connection.DatabaseConnection.get_connection')
    def test_task_create_calls_execute_and_commit(self, mock_get_conn):
        cur = DummyCursor()
        conn = MockConn(cur)
        mock_get_conn.return_value = conn

        TaskService.create_task('Task 1', 'Pending', 7, 'alice')

        self.assertTrue(cur.queries)
        q, params = cur.queries[0]
        self.assertIn('INSERT INTO tasks', q)
        self.assertEqual(params, ('Task 1', 'Pending', 7, 'alice'))
        self.assertTrue(conn.committed)

    @patch('app.Database.connection.DatabaseConnection.get_connection')
    def test_get_tasks_returns_rows(self, mock_get_conn):
        rows = [{'id': 1, 'title': 'Do X'}]
        cur = DummyCursor(rows=rows)
        conn = MockConn(cur)
        mock_get_conn.return_value = conn

        result = TaskService.get_tasks(7)
        self.assertEqual(result, rows)


if __name__ == '__main__':
    unittest.main()
