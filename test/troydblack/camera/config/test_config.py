import unittest

from src.troydblack.camera.config import config


class ConfigTester(unittest.TestCase):
    def test_readConfig(self):
        self.assertIn('APP', config, 'Unable to find APP Section in Config')
        self.assertIn('secret_key', config['APP'], 'Unable to find secret_key under APP Config')
