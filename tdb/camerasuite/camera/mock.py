import io
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

    @property
    def last_image_bytes(self):
        # Random color array
        array = numpy.random.rand(self.height, self.width, 3) * 255
        image = Image.fromarray(array.astype('uint8')).convert('RGB')
        b = io.BytesIO()
        image.save(b, format='JPEG')
        return b.getvalue()

    def stream_image(self):
        while True:
            time.sleep(1 / self.fps)
            yield from self._stream_image_formatter()
