import argparse
import importlib
import json
import os
from enum import Enum
from typing import Union

import sys
from pydantic import BaseModel

from camera import CameraDriver

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--profile", help="load specified settings profiles")
parser.add_argument("-v",
                    "--verbosity",
                    action="count",
                    help="increase output verbosity")
args = parser.parse_args()


class EnumDriver(str, Enum):
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
    CAMERA = 'camera'
    ROUTERS = 'routers'


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
        self._camera_driver: CameraDriver = self.camera_driver

    @property
    def camera_driver(self):
        if self._last_driver != self.web.active_driver:
            camera_module = importlib.import_module(f'{EnumPackages.CAMERA}.{self.web.active_driver.name.lower()}')
            self._camera_driver = getattr(camera_module, f'{self.web.active_driver.value}Driver')(
                **getattr(self, self.web.active_driver.name.lower()).dict())
            self._last_driver = self.web.active_driver
        return self._camera_driver


config: ConfigBase = ConfigBase()
