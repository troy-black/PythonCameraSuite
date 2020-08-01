import importlib
from enum import Enum
from typing import List, Any, Dict

from pydantic import BaseModel

from troydblack.suite.camera import CameraDriver


class EnumDriver(str, Enum):
    MOCK = 'MockDriver'
    OPENCV = 'OpenCvDriver'


class EnumLoggingLevel(str, Enum):
    NOTSET = 'NOTSET'
    CRITICAL = 'CRITICAL'
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    INFO = 'INFO'
    DEBUG = 'DEBUG'


class DriverBase(BaseModel):
    module: str
    class_name: str
    name: str


class MockDriver(DriverBase):
    module = 'src.troydblack.suite.camera.mock'
    class_name = 'MockDriver'
    name = 'mock'


class OpenCvDriver(DriverBase):
    module = 'src.troydblack.suite.camera.opencv'
    class_name = 'OpenCvDriver'
    name = 'opencv'


class WebBase(BaseModel):
    routers_package: str = 'src.troydblack.suite.routers'
    secret_key: str = 'change_me_before_using_in_production'


class ConfigBaseApp(BaseModel):
    logging: EnumLoggingLevel = EnumLoggingLevel.NOTSET
    host: str = '0.0.0.0'
    port: int = 8000


class ConfigWebApp(BaseModel):
    active_driver: EnumDriver = EnumDriver.MOCK
    display_settings: List[EnumDriver] = [
        EnumDriver.MOCK,
        EnumDriver.OPENCV
    ]


class ConfigMockDriverSettings(BaseModel):
    width: int = 1280
    height: int = 720
    sleep: float = 1 / 15  # FPS


class ConfigOpenCvDriverSettings(BaseModel):
    source: str = '0'


class ConfigBase(BaseModel):
    # web_base: WebBase = WebBase()

    # The following can be updated via Web API
    base: ConfigBaseApp = ConfigBaseApp()
    web: ConfigWebApp = ConfigWebApp()


def load_config() -> ConfigBase:
    # Load base config
    base = ConfigBase()

    # Overlay settings for OS
    # TODO - finish me

    # Overlay settings from command line
    # TODO - finish me

    return base


driver_details: Dict[EnumDriver, DriverBase] = {
    EnumDriver.MOCK: MockDriver(),
    EnumDriver.OPENCV: OpenCvDriver()
}

driver_settings: Dict[EnumDriver, BaseModel] = {
    EnumDriver.MOCK: ConfigMockDriverSettings(),
    EnumDriver.OPENCV: ConfigOpenCvDriverSettings()
}

config: ConfigBase = load_config()


def get_camera_driver(driver_name: EnumDriver):
    base: DriverBase = driver_details[driver_name]
    settings: BaseModel = driver_settings[driver_name]
    settings_dict = {
        key: val
        for key, val in settings.__dict__.items()
        if not key.startswith('__')
    }
    camera_module = importlib.import_module(base.module)
    return getattr(camera_module, base.class_name)(**settings_dict)

# import importlib
# import platform
#
# import sys
#
# from src.troydblack.suite.config.config import ConfigBase
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
