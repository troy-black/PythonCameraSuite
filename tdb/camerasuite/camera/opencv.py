import logging
import threading
from enum import Enum
from time import time

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
        # [cv.videoio_registry.getBackendName(b) for b in cv.videoio_registry.getBackends()]
        self.driver = cv.VideoCapture(settings.source, cv.CAP_V4L2)
        if not self.driver.isOpened():
            raise RuntimeError(f'Could not start camera from source: {settings.source}')
        self.default_settings: ConfigOpenCvDriver = ConfigOpenCvDriver(**self.get_camera_settings())
        self.lock = threading.Lock()
        self._settings: ConfigOpenCvDriver = settings
        self.timestamp = time()

        self.width = 3840.0
        self.height = 2160.0

        # self.width = 4056.0
        # self.height = 3040.0

        self.fps = 0.0
        self.event = threading.Event()
        self.event.clear()

        # for prop, val in self._settings.dict().items():
        #     if hasattr(self, prop):
        #         self.__setattr__(prop, val)

    def __getattr__(self, item):
        if item in OpenCvProperties.__members__:
            return self.driver.get(OpenCvProperties[item])
        # print(item)
        # return getattr(self, item)
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

    def generate_image(self):
        response = True
        while response and self.background_task:
        #     lock = self.lock.acquire(False)
        #     if lock:
        #         logging.debug('Acquire stream_image Lock')
            response, frame = self.driver.read()
            if not response:
                raise RuntimeError('Could not read frame')

            response, image = cv.imencode('.jpg', frame)
            if not response:
                raise RuntimeError('Could not encode image')

            self.last_image_bytes = image.tobytes()

            self.fps = 1.0 / (time() - self.timestamp)
            logging.debug(self.fps)
            self.timestamp = time()
            self.event.set()

            #     logging.debug('Release stream_image Lock')
            #     self.lock.release()
            # # else:
            # #     logging.debug('Skip Lock')
            #
            # if self.last_image_bytes is not None:
            #     yield from self.stream_image()
