import unittest

from fastapi.testclient import TestClient

from src.troydblack.suite.main import app


class FastApiBaseTester(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
