import unittest

from src.troydblack.camera.app import app


class FlaskAppBaseTester(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
