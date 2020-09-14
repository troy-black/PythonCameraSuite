import io
import threading
import time

import picamera

from tdb.camerasuite.camera import CameraDriver
from tdb.camerasuite.config import ConfigPiCameraDriver


class PiCameraDriver(CameraDriver):
    def __init__(self, settings: ConfigPiCameraDriver):
        self._settings: ConfigPiCameraDriver = settings
        self.lock = threading.Lock()
        self.timestamp = time.time()
        self.fps = 0.0
        self.width = settings.width
        self.height = settings.height

    def stream_image(self):
        while True:
            lock = self.lock.acquire(False)
            if lock:
                with picamera.PiCamera() as camera:
                    camera.resolution = (self.width, self.height)
                    # let camera warm up
                    time.sleep(2)

                    stream = io.BytesIO()
                    for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                        # return current frame
                        stream.seek(0)
                        self.last_image_bytes = stream.read()

                        # reset stream for next frame
                        stream.seek(0)
                        stream.truncate()

                        self.fps = 1 / (time.time() - self.timestamp)
                        self.timestamp = time.time()

                self.lock.release()

            yield from self._stream_image_formatter()
