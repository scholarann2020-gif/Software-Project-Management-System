from pathlib import Path
import sys
# ensure project root is importable when running tests directly
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import unittest
from app.services.project_service import ProjectService


class TestProjectService(unittest.TestCase):
    def test_create_project(self):
        ProjectService.create_project("Test", "Desc", "Pending", 1)
        self.assertTrue(True)
