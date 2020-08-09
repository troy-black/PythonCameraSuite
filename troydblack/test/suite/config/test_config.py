import unittest

from troydblack.suite.config import ConfigBase


class ConfigTester(unittest.TestCase):
    def test_load_config(self):
        config = ConfigBase(profile='dev')
        self.assertIsNotNone(config, 'Unable to load config')
