# import argparse
import importlib
import json
import os
import sys
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
    UV4L = 'Uv4l'


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
    display_uv4l: bool = False


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
    width: int = 1280
    height: int = 720


class ConfigUv4lDriver(BaseConfig):
    host: str = networking.get_hostname()
    port: int = 8080
    v4l2_fourcc: int = 1196444237
    width: int = 1920
    height: int = 1080
    brightness: int = 50
    contrast: int = 0
    saturation: int = 0
    red_balance: int = 100
    blue_balance: int = 100
    sharpness: int = 0
    rotate: int = 0
    shutter_speed: int = 0
    zoom_factor: int = 1
    iso_sensitivity: int = 0
    jpeg_quality: int = 85
    frame_rate: int = 30
    horizontal_mirror: int = 0
    vertical_mirror: int = 0
    text_overlay: int = 0
    object_face_detection: int = 0
    stills_denoise: int = 0
    video_denoise: int = 0
    image_stabilization: int = 0
    flicker_avoidance: int = 3
    awb_mode: int = 0
    exposure_mode: int = 1
    exposure_metering: int = 0
    drc_strength: int = 3

    def get_url(self):
        return f'http://{self.host}:{self.port}/api/videodev/settings'

    async def get_api_videodev_settings(self) -> dict:
        return await get_json(self.get_url())

    async def put_api_videodev_settings(self) -> dict:
        return await put_json(self.get_url(),
                              json={
                                  'apply_settings_only_if_changed': True,
                                  'controls': [
                                      {
                                          'current_value': val,
                                          'id': Uv4lRestApiId[key].value
                                      }
                                      for key, val in self.dict().items()
                                      if key in Uv4lRestApiId.__members__
                                  ],
                                  'current_format': {
                                      'height': self.height,
                                      'v4l2_fourcc': self.v4l2_fourcc,
                                      'width': self.width
                                  }
                              })


class Uv4lRestApiId(int, Enum):
    brightness = 9963776
    contrast = 9963777
    saturation = 9963778
    red_balance = 9963790
    blue_balance = 9963791
    sharpness = 9963803
    rotate = 9963810
    shutter_speed = 134217728
    zoom_factor = 134217729
    iso_sensitivity = 134217730
    jpeg_quality = 134217739
    frame_rate = 134217741
    horizontal_mirror = 9963796
    vertical_mirror = 9963797
    text_overlay = 134217734
    object_face_detection = 134217736
    stills_denoise = 134217737
    video_denoise = 134217738
    image_stabilization = 134217740
    flicker_avoidance = 9963800
    awb_mode = 134217731
    exposure_mode = 134217732
    exposure_metering = 134217733
    drc_strength = 134217735


# class Uv4lFourCC(int, Enum):
#     MJPEG_Video = 1196444237
#     JPEG_Still = 1195724874
#
#
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
        self.uv4l: ConfigUv4lDriver = ConfigUv4lDriver.build(profile=profile) \
            if 'uv4l' in self.camera_drivers else None

        self.last_driver = None
        self._camera_driver: CameraDriver = self.camera_driver

    @property
    def camera_driver(self) -> CameraDriver:
        if self.last_driver != self.web.active_driver:
            self.load_camera_driver()
        return self._camera_driver

    def load_camera_driver(self):
        if hasattr(self, '_camera_driver') and self._camera_driver is not None:
            del self._camera_driver
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
