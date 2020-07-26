import importlib
import platform

import sys

from src.troydblack.suite.config.config import ConfigBase


def load_config():
    itr = next(
        (
            argv
            for argv in sys.argv
            if argv.startswith('profile=')  # filter by profile arg
        ),
        None
    )
    profile = itr.split('=')[-1] if itr \
        else platform.system().lower()  # default to current system profile

    base_config = tmp = getattr(
        importlib.import_module(
            f'{__name__}.{profile}'  # import: from *.config import dev
        ),
        'Config'
    )

    for arg in sys.argv:
        if '=' in arg and not arg.startswith('profile='):  # filter out any profile from args
            param, val = arg.split('=')

            keys = param.split('.')
            for i in range(0, len(keys) - 1):  # walk object tree to variable
                tmp = getattr(tmp, keys[i])

            setattr(tmp, keys[-1], val)  # update variable name with arg value

    return base_config


config: ConfigBase = load_config()
