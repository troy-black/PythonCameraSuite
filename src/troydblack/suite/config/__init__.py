import importlib
import platform

import sys

from src.troydblack.suite.config.config import ConfigBase


def load_config(*, config_module: type = None, config_name: str = 'Config'):
    if config_module is None:
        config_module = importlib.import_module(f'{__name__}.{platform.system().lower()}')

    base_config = _config = getattr(config_module, config_name)

    for arg in [arg for arg in sys.argv if '=' in arg]:
        param, val = arg.split('=')

        keys = param.split('.')
        for i in range(0, len(keys) - 1):
            _config = getattr(_config, keys[i])

        setattr(_config, keys[-1], val)

    return base_config


config: ConfigBase = load_config()
