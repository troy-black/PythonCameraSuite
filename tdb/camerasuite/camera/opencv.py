import threading
from enum import Enum
from time import time

import cv2 as cv

from tdb.camerasuite.camera import CameraDriver
from tdb.camerasuite.config import ConfigOpenCvDriver


class OpenCvProperties(int, Enum):
    brightness = cv.CAP_PROP_BRIGHTNESS
    contrast = cv.CAP_PROP_CONTRAST
    exposure = cv.CAP_PROP_EXPOSURE
    height = cv.CAP_PROP_FRAME_HEIGHT
    width = cv.CAP_PROP_FRAME_WIDTH


class OpenCvDriver(CameraDriver):

    def __init__(self, settings: ConfigOpenCvDriver):
        self.driver = cv.VideoCapture(settings.source)
        self.default_settings: ConfigOpenCvDriver = ConfigOpenCvDriver(**self.get_camera_settings())
        if not self.driver.isOpened():
            raise RuntimeError(f'Could not start camera from source: {settings.source}')
        self.lock = threading.Lock()
        self._settings: ConfigOpenCvDriver = settings
        self.timestamp = time()
        self.fps = 0.0

        for prop, val in self._settings.dict().items():
            if hasattr(self, prop):
                self.__setattr__(prop, val)

    def __getattr__(self, item):
        if item in OpenCvProperties.__members__:
            return self.driver.get(OpenCvProperties[item])
        return getattr(self, item)
        # return super().__getattr__(item)

    def __setattr__(self, key, value):
        if key in OpenCvProperties.__members__:
            return self.driver.set(OpenCvProperties[key], value)
        return super().__setattr__(key, value)

    # def get_camera_settings(self) -> dict:
    #     return {
    #         attr: self.__getattr__(attr)
    #         for attr in [
    #             'brightness',
    #             'contrast',
    #             'exposure',
    #             'height',
    #             'width',
    #         ]
    #     }

    def stream_image(self):
        response = True
        while response:
            lock = self.lock.acquire(False)
            if lock:
                response, frame = self.driver.read()
                if not response:
                    raise RuntimeError('Could not read frame')

                response, image = cv.imencode('.jpg', frame)
                if not response:
                    raise RuntimeError('Could not encode image')

                self.last_image_bytes = image.tobytes()

                self.fps = 1 / (time() - self.timestamp)
                self.timestamp = time()

                self.lock.release()

            yield from self._stream_image_formatter()
