import io
import threading

import picamera
import time

from src.troydblack.suite.camera import CameraDriver


class OpenCvDriver(CameraDriver):
    def __init__(self):
        self.lock = threading.Lock()

    def stream_image(self):
        while True:
            lock = self.lock.acquire(False)
            if lock:
                with picamera.PiCamera() as camera:
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
                self.lock.release()

            yield from self._stream_image_formatter()
