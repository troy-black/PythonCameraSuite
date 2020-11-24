import io
import logging
import time

import picamera

from tdb.camerasuite.camera import CameraDriver
from tdb.camerasuite.config import ConfigPiCameraDriver


class PiCameraDriver(CameraDriver):
    def __init__(self, settings: ConfigPiCameraDriver):
        super().__init__()
        self.settings: ConfigPiCameraDriver = settings

        self.stream = io.BytesIO()
        self.camera: picamera.PiCamera = None

    def __del__(self):
        self.deactivate_camera()

    def activate_camera(self):
        self.camera = picamera.PiCamera(sensor_mode=self.settings.sensor_mode)
        self.camera.resolution = (self.settings.width, self.settings.height)
        self.camera.framerate_range = (0.005, 30)
        self.camera.iso = self.settings.iso
        self.camera.exposure_mode = self.settings.exposure_mode
        self.camera.brightness = self.settings.brightness

        if self.settings.shutter_speed > 0:
            self.camera.shutter_speed = self.settings.shutter_speed * 1000000

        logging.debug(f'Initializing PiCamera: wait {self.settings.shutter_speed}')
        time.sleep(2)

    def deactivate_camera(self):
        if self.camera and not self.camera.closed:
            self.camera.close()

    def generate_images(self):
        lock = self.lock.acquire(False)

        if lock:
            self.activate_camera()
            # while response and self.background_task:
            for _ in self.camera.capture_continuous(self.stream, 'jpeg', use_video_port=True):
                self.generate_image(False)
                if not self.background_task:
                    break

            self.deactivate_camera()
            self.lock.release()

    def _generate_image(self, set_lock: bool):
        try:
            if set_lock:
                self.camera.capture(self.stream, 'jpeg', use_video_port=False)
                self.deactivate_camera()

            # return current frame
            self.stream.seek(0)
            self.last_image_bytes = self.stream.read()

            # reset stream for next frame
            self.stream.seek(0)
            self.stream.truncate()

        except Exception as e:
            return None
