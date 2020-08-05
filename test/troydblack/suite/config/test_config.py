import unittest

from src.troydblack.suite.config import load_config


class ConfigTester(unittest.TestCase):
    def test_load_config(self):
        config = load_config()
        self.assertIsNotNone(config, 'Unable to load config')
