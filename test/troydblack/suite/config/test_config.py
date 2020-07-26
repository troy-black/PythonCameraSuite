import unittest

from src.troydblack.suite.config import load_config


class ConfigTester(unittest.TestCase):
    def test_readConfig(self):
        config = load_config()
        self.assertIsNotNone(config.App.secret_key, 'Unable to verify a valid key: config.App.secret_key')
