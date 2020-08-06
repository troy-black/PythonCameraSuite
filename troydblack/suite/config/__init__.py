import importlib
from enum import Enum

from pydantic import BaseModel


class EnumDriver(Enum):
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

# class DriverBase:
#     module: str
#     class_name: str
#     route: str
#     template: str
#     title: str
#     url: str
#
#
# class MockDriver(DriverBase):
#     module = 'troydblack.suite.camera.mock'
#     class_name = 'MockDriver'
#     route = 'get_settings_mock'
#     template = 'settings_mock.html'
#     title = 'Mock'
#     url = '/mock'
#
#
# class OpenCvDriver(DriverBase):
#     module = 'troydblack.suite.camera.opencv'
#     class_name = 'OpenCvDriver'
#     route = 'get_settings_opencv'
#     template = 'settings_opencv.html'
#     title = 'OpenCv'
#     url = '/opencv'


# class WebBase(BaseModel):
#     routers_package: str = 'troydblack.suite.routers'


class ConfigApp(BaseModel):
    logging: EnumLoggingLevel = EnumLoggingLevel.NOTSET
    host: str = '0.0.0.0'
    port: int = 8000


class ConfigWeb(BaseModel):
    active_driver: EnumDriver = EnumDriver.MOCK
    display_mock: bool = True
    display_opencv: bool = True


class ConfigMockDriver(BaseModel):
    width: int = 1280
    height: int = 720
    sleep: float = 1 / 15  # FPS


class ConfigOpenCvDriver(BaseModel):
    source: str = '0'


class ConfigBase(BaseModel):

    # The following can be updated via Web API
    app: ConfigApp = ConfigApp()
    web: ConfigWeb = ConfigWeb()

    mock: ConfigMockDriver = ConfigMockDriver()
    opencv: ConfigOpenCvDriver = ConfigOpenCvDriver()


def load_config() -> ConfigBase:
    # Load base config
    base = ConfigBase()

    # Overlay settings for OS
    # TODO - finish me

    # Overlay settings from command line
    # TODO - finish me

    return base


config: ConfigBase = load_config()


def get_camera_driver(driver_details: EnumDriver):
    settings_dict = {
        key: val
        for key, val in getattr(config, driver_details.name.lower()).__dict__.items()
        if not key.startswith('__')
    }
    camera_module = importlib.import_module(f'{EnumPackages.CAMERA}.{driver_details.name.lower()}')
    return getattr(camera_module, f'{driver_details.value}Driver')(**settings_dict)


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
