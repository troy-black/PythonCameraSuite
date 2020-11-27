# import argparse
import importlib
import json
import os
import sys
import time
from enum import Enum
from typing import Union, List

from pydantic import BaseModel

from tdb.camerasuite.utilities import networking
from tdb.camerasuite.camera import CameraDriver
from tdb.camerasuite.utilities import import_submodules
from tdb.camerasuite.utilities.requests import get_json, put_json

# parser = argparse.ArgumentParser()
# parser.add_argument("-p", "--profile", help="load specified settings profiles")
# parser.add_argument("-v",
#                     "--verbosity",
#                     action="count",
#                     help="increase output verbosity")
# args = parser.parse_args()


class EnumDriver(str, Enum):
    MOCK = 'Mock'
    OPENCV = 'OpenCv'
    PICAMERA = 'PiCamera'


# TODO - Don't recreate the wheel
class EnumLoggingLevel(str, Enum):
    NOTSET = 'NOTSET'
    CRITICAL = 'CRITICAL'
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    INFO = 'INFO'
    DEBUG = 'DEBUG'


class EnumPackages(str, Enum):
    CAMERA = 'tdb.camerasuite.camera'
    ROUTERS = 'tdb.camerasuite.routers'


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
    display_opencv: bool = False
    display_picamera: bool = False


class ConfigMockDriver(BaseConfig):
    width: int = 1280
    height: int = 720
    fps: int = 15


class ConfigOpenCvDriver(BaseConfig):
    source: Union[int, str] = 0
    brightness: float = None  # 50.0
    contrast: float = None  # 0.0
    exposure: float = None  # 1000.0
    width: float = None  # 1280.0
    height: float = None  # 720.0


class ConfigPiCameraDriver(BaseConfig):
    width: int = 1920
    height: int = 1080
    shutter_speed: int = 0
    exposure_mode: str = 'auto'
    iso: int = 100
    sensor_mode: int = 1
    brightness: int = 50


class ConfigBase:
    def __init__(self, *, profile: str = None):
        profile = profile  # or args.profile
        self.app: ConfigApp = ConfigApp.build(profile=profile)
        self.web: ConfigWeb = ConfigWeb.build(profile=profile)

        self.camera_drivers = verify_camera_drivers()

        self.mock: ConfigMockDriver = ConfigMockDriver.build(profile=profile) \
            if 'mock' in self.camera_drivers else None
        self.opencv: ConfigOpenCvDriver = ConfigOpenCvDriver.build(profile=profile) \
            if 'opencv' in self.camera_drivers else None
        self.picamera: ConfigPiCameraDriver = ConfigPiCameraDriver.build(profile=profile) \
            if 'picamera' in self.camera_drivers else None

        self.last_driver = None
        self._camera_driver: CameraDriver = self.camera_driver

    @property
    def camera_driver(self) -> CameraDriver:
        if self.last_driver != self.web.active_driver:
            self.load_camera_driver()
        return self._camera_driver

    def load_camera_driver(self):
        if hasattr(self, '_camera_driver') and self._camera_driver is not None:
            self.camera_driver.background_task = False
            del self._camera_driver
            time.sleep(2)
        camera_module = importlib.import_module(f'{EnumPackages.CAMERA}.{self.web.active_driver.name.lower()}')
        self._camera_driver = getattr(camera_module, f'{self.web.active_driver.value}Driver')(
            getattr(self, self.web.active_driver.name.lower()))
        self.last_driver = self.web.active_driver


def verify_camera_drivers() -> List[str]:
    return [
        key.split('.')[-1]
        for (key, val) in import_submodules(EnumPackages.CAMERA).items()
        if val
    ]


config: ConfigBase = ConfigBase()
