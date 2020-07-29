import unittest

from fastapi.testclient import TestClient

from src.troydblack.suite.app import app, mount


class FastApiBaseTester(unittest.TestCase):
    def setUp(self):
        mount(url='/static', directory='../src/troydblack/suite/static', name='static')
        self.client = TestClient(app)
