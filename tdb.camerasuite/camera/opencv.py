import threading
from time import time

import cv2 as cv

from camera import CameraDriver
from config import ConfigOpenCvDriver


class OpenCvDriver(CameraDriver):

    def __init__(self, settings: ConfigOpenCvDriver):
        self.driver = cv.VideoCapture(settings.source)
        if not self.driver.isOpened():
            raise RuntimeError(f'Could not start camera from source: {settings.source}')
        self.lock = threading.Lock()
        self._settings: ConfigOpenCvDriver = settings
        self.timestamp = time()
        self.fps = 0.0

        for prop, val in self._settings.dict().items():
            if hasattr(self, prop):
                setattr(self, prop, val)

    @property
    def brightness(self) -> int:
        return self.driver.get(cv.CAP_PROP_BRIGHTNESS)

    @brightness.setter
    def brightness(self, val: int):
        self.driver.set(cv.CAP_PROP_BRIGHTNESS, val)
        self._settings.brightness = self.brightness

    @property
    def contrast(self) -> int:
        return self.driver.get(cv.CAP_PROP_CONTRAST)

    @contrast.setter
    def contrast(self, val: int):
        self.driver.set(cv.CAP_PROP_CONTRAST, val)
        self._settings.contrast = self.contrast

    @property
    def exposure(self) -> int:
        return self.driver.get(cv.CAP_PROP_EXPOSURE)

    @exposure.setter
    def exposure(self, val: int):
        self.driver.set(cv.CAP_PROP_EXPOSURE, val)
        self._settings.exposure = self.exposure

    @property
    def height(self) -> float:
        return self.driver.get(cv.CAP_PROP_FRAME_HEIGHT)

    @height.setter
    def height(self, val: float):
        self.driver.set(cv.CAP_PROP_FRAME_HEIGHT, val)
        self._settings.height = self.height

    @property
    def width(self) -> float:
        return self.driver.get(cv.CAP_PROP_FRAME_WIDTH)

    @width.setter
    def width(self, val: float):
        self.driver.set(cv.CAP_PROP_FRAME_WIDTH, val)
        self._settings.width = self.width

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
