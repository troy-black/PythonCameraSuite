from enum import Enum

import cv2 as cv

from tdb.camerasuite.camera import CameraDriver
from tdb.camerasuite.config import ConfigOpenCvDriver


class OpenCvProperties(int, Enum):
    auto_exposure = cv.CAP_PROP_AUTO_EXPOSURE
    brightness = cv.CAP_PROP_BRIGHTNESS
    buffersize = cv.CAP_PROP_BUFFERSIZE
    contrast = cv.CAP_PROP_CONTRAST
    convert_rgb = cv.CAP_PROP_CONVERT_RGB
    exposure = cv.CAP_PROP_EXPOSURE
    fourcc = cv.CAP_PROP_FOURCC
    # fps = cv.CAP_PROP_FPS
    height = cv.CAP_PROP_FRAME_HEIGHT
    iso_speed = cv.CAP_PROP_ISO_SPEED
    mode = cv.CAP_PROP_MODE
    roll = cv.CAP_PROP_ROLL
    saturation = cv.CAP_PROP_SATURATION
    sharpness = cv.CAP_PROP_SHARPNESS
    white_balance_blue_u = cv.CAP_PROP_WHITE_BALANCE_BLUE_U
    white_balance_red_v = cv.CAP_PROP_WHITE_BALANCE_RED_V
    width = cv.CAP_PROP_FRAME_WIDTH


class OpenCvDriver(CameraDriver):

    def __init__(self, settings: ConfigOpenCvDriver):
        super().__init__()
        self._settings: ConfigOpenCvDriver = settings
        self.driver = cv.VideoCapture(settings.source)
        if not self.driver.isOpened():
            raise RuntimeError(f'Could not start camera from source: {settings.source}')
        self.default_settings: ConfigOpenCvDriver = ConfigOpenCvDriver(**self.get_camera_settings())

        for prop, val in self._settings.dict().items():
            if hasattr(self, prop):
                self.__setattr__(prop, val)

    def __getattr__(self, item):
        if item in OpenCvProperties.__members__:
            return self.driver.get(OpenCvProperties[item])
        return super().__getattr__(item)

    def __setattr__(self, key, value):
        if key in OpenCvProperties.__members__:
            return self.driver.set(OpenCvProperties[key], value)
        return super().__setattr__(key, value)

    def get_camera_settings(self) -> dict:
        return {
            attr: self.__getattr__(attr)
            for attr in OpenCvProperties.__members__
        }

    def modifiable_camera_settings(self) -> list:
        return [
            attr
            for attr in OpenCvProperties.__members__
            if self.__setattr__(attr,
                                self.__getattr__(attr))
        ]

    def _generate_image(self, *args):
        try:
            response, frame = self.driver.read()
            if not response:
                raise RuntimeError('Could not read frame')

            response, image = cv.imencode('.jpg', frame)
            if not response:
                raise RuntimeError('Could not encode image')

            self.last_image_bytes = image.tobytes()

        except Exception as e:
            return None
