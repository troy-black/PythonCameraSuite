import io
import logging
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
        self.event = threading.Event()
        self.event.clear()

    def generate_image(self):
        # while True:
        lock = self.lock.acquire(False)
        if lock:
            with picamera.PiCamera(sensor_mode=3) as camera:
                logging.debug('setting up...')
                self.timestamp = time.time()
                # camera.resolution = (self.width, self.height)
                # camera.resolution = (3280, 2464)
                camera.resolution = (4056, 3040)
                camera.framerate_range = (0.005, 10)
                # camera.sensor_mode = 3
                # camera.shutter_speed = 6000000
                # camera.shutter_speed = 10000000
                # camera.shutter_speed = 30000000
                # camera.shutter_speed = 40000000
                # camera.shutter_speed = 50000000
                # camera.shutter_speed = 60000000
                # camera.shutter_speed = 90000000
                # camera.shutter_speed = 120000000
                camera.shutter_speed = 195000000
                camera.iso = 800
                camera.exposure_mode = 'off'

                # let camera warm up
                logging.debug(f'sleeping... {camera.shutter_speed}')
                time.sleep(2)

                self.fps = 1 / (time.time() - self.timestamp)
                logging.debug(self.fps)

                stream = io.BytesIO()
                for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                    # return current frame
                    stream.seek(0)
                    self.last_image_bytes = stream.read()

                    # reset stream for next frame
                    stream.seek(0)
                    stream.truncate()

                    self.fps = 1 / (time.time() - self.timestamp)
                    logging.debug(self.fps)
                    self.timestamp = time.time()

                    if not self.background_task:
                        break
                    self.event.set()
                    # time.sleep(0)
                    self.event.clear()

            self.lock.release()
            # else:
            #     time.sleep(5)
            #
            # if self.last_image_bytes:
            #     yield from self.stream_image()
