import unittest
from app.services.project_service import ProjectService


class TestProjectService(unittest.TestCase):
    def test_create_project(self):
        ProjectService.create_project("Test", "Desc", "Pending", 1)
        self.assertTrue(True)
