import threading

import cv2 as cv

from camera import CameraDriver


class OpenCvDriver(CameraDriver):
    def __init__(self, *, source):
        self.driver = cv.VideoCapture(source)
        if not self.driver.isOpened():
            raise RuntimeError(f'Could not start camera from source: {source}')
        self.lock = threading.Lock()

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
                self.lock.release()

            yield from self._stream_image_formatter()
