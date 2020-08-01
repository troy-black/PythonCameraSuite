import unittest

from src.troydblack.suite.config import WebBase
from src.troydblack.suite.config import load_config


class ConfigTester(unittest.TestCase):
    def test_load_config(self):
        self.assertIsNotNone(WebBase().routers_package)
        config = load_config()
        self.assertIsNotNone(config, 'Unable to load config')
