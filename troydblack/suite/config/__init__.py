import argparse

import importlib
import json
import os
from typing import Union

import sys
from enum import Enum

from pydantic import BaseModel

from troydblack.suite.camera import CameraDriver

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--profile", help="load specified settings profiles")
parser.add_argument("-v",
                    "--verbosity",
                    action="count",
                    help="increase output verbosity")
args = parser.parse_args()


class EnumDriver(str, Enum):
    # def __new__(cls, *args, **kwargs):
    #     obj = object.__new__(cls)
    #     obj._value_ = args[0]
    #     return obj
    #
    # def __init__(self, proper_name: str):
    #     self.proper_name: str = proper_name

    MOCK = 'Mock'  # , 'mock'
    OPENCV = 'OpenCv'  # , 'opencv'


# TODO - Don't recreate the wheel
class EnumLoggingLevel(str, Enum):
    NOTSET = 'NOTSET'
    CRITICAL = 'CRITICAL'
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    INFO = 'INFO'
    DEBUG = 'DEBUG'


class EnumPackages(str, Enum):
    CAMERA = 'troydblack.suite.camera'
    ROUTERS = 'troydblack.suite.routers'


class BaseConfig(BaseModel):

    @classmethod
    def build(cls, *, profile: str = None):
        base = cls()
        details = base.dict()
        profiles = set()
        [
            details.update(base.load(profile=prof) or {})
            for prof in (sys.platform, None, profile)
            if prof not in profiles or profiles.add(prof)
        ]
        return cls(**details)

    def filename(self, *, profile: str = None) -> str:
        return '{}{}.json'.format(
            f'{profile}_' if profile else '',
            self.__class__.__name__
        )

    def load(self, *, profile: str = None) -> dict:
        filename = self.filename(profile=profile)
        if os.path.exists(filename):
            with open(filename, 'r') as json_file:
                return json.load(json_file)

    def merge(self, settings: BaseModel):
        self.__dict__.update(settings.dict())
        self.save()
        return self

    def save(self):
        with open(self.filename(), 'w') as json_file:
            json.dump(self.dict(), json_file)


class ConfigApp(BaseConfig):
    logging: EnumLoggingLevel = EnumLoggingLevel.NOTSET
    host: str = '0.0.0.0'
    port: int = 8000


class ConfigWeb(BaseConfig):
    active_driver: EnumDriver = EnumDriver.MOCK
    display_mock: bool = True
    display_opencv: bool = True


class ConfigMockDriver(BaseConfig):
    width: int = 1280
    height: int = 720
    sleep: float = 1 / 15  # FPS


class ConfigOpenCvDriver(BaseConfig):
    source: Union[int, str] = 0


class ConfigBase:
    def __init__(self, *, profile: str = None):
        profile = profile or args.profile
        self.app: ConfigApp = ConfigApp.build(profile=profile)
        self.web: ConfigWeb = ConfigWeb.build(profile=profile)
        self.mock: ConfigMockDriver = ConfigMockDriver.build(profile=profile)
        self.opencv: ConfigOpenCvDriver = ConfigOpenCvDriver.build(profile=profile)
        self._last_driver = None
        self._camera_driver: CameraDriver = self.camera_driver  # = CameraDriver.build()

    @property
    def camera_driver(self):
        if self._last_driver != self.web.active_driver:
            camera_module = importlib.import_module(f'{EnumPackages.CAMERA}.{self.web.active_driver.name.lower()}')
            self._camera_driver = getattr(camera_module, f'{self.web.active_driver.value}Driver')(
                **getattr(self, self.web.active_driver.name.lower()).dict())
            self._last_driver = self.web.active_driver
        return self._camera_driver


config: ConfigBase = ConfigBase()


# def get_camera_driver(driver_details: EnumDriver):
#     settings_dict = {
#         key: val
#         for key, val in getattr(config, driver_details.name.lower()).__dict__.items()
#         if not key.startswith('__')
#     }
#     camera_module = importlib.import_module(f'{EnumPackages.CAMERA}.{driver_details.name.lower()}')
#     return getattr(camera_module, f'{driver_details.value}Driver')(**settings_dict)


# def get_settings_details():
#     def build(title, route, template):
#         return {
#             title: {
#                 'route': route,
#                 'template': template,
#                 # 'active': config.web.active_driver == title
#             }
#         }
#
#     details = build('Settings', 'get_settings', 'settings.html')
#     [
#         details.update(
#             build(
#                 driver_details[d].title,
#                 driver_details[d].route,
#                 driver_details[d].template
#             )
#         )
#         for d in config.web.display_settings
#     ]
#
#     return details


# import importlib
# import platform
#
# import sys
#
# from troydblack.suite.config.config import ConfigBase
#
#
# def load_config():
#     itr = next(
#         (
#             argv
#             for argv in sys.argv
#             if argv.startswith('profile=')  # filter by profile arg
#         ),
#         None
#     )
#     profile = itr.split('=')[-1] if itr \
#         else platform.system().lower()  # default to current system profile
#
#     base_config = tmp = getattr(
#         importlib.import_module(
#             f'{__name__}.{profile}'  # import: from *.config import dev
#         ),
#         'Config'
#     )
#
#     for arg in sys.argv:
#         if '=' in arg and not arg.startswith('profile='):  # filter out any profile from args
#             param, val = arg.split('=')
#
#             keys = param.split('.')
#             for i in range(0, len(keys) - 1):  # walk object tree to variable
#                 tmp = getattr(tmp, keys[i])
#
#             setattr(tmp, keys[-1], val)  # update variable name with arg value
#
#     return base_config
#
#
# config: ConfigBase = load_config()
