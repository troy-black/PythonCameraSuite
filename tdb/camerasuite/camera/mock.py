import io
import threading
import time

import numpy
from PIL import Image

from tdb.camerasuite.camera import CameraDriver
from tdb.camerasuite.config import ConfigMockDriver


class MockDriver(CameraDriver):
    def __init__(self, settings: ConfigMockDriver):
        self._settings: ConfigMockDriver = settings
        self.height = settings.height
        self.width = settings.width
        self.fps = settings.fps
        self.event = threading.Event()
        self.event.clear()

    def generate_image(self):
        while self.background_task:
            # Random color array
            array = numpy.random.rand(self.height, self.width, 3) * 255
            image = Image.fromarray(array.astype('uint8')).convert('RGB')
            b = io.BytesIO()
            image.save(b, format='JPEG')
            self.last_image_bytes = b.getvalue()
            time.sleep(1 / self.fps)
            self.event.set()
            # yield from self.stream_image()
