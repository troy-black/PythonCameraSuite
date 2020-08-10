import io

import numpy
import time
from PIL import Image

from camera import CameraDriver


class MockDriver(CameraDriver):
    def __init__(self, *, height: int, width: int, sleep: int):
        self.height = height
        self.width = width
        self.sleep = sleep

    @property
    def last_image_bytes(self):
        array = numpy.random.rand(self.height, self.width, 3) * 255
        image = Image.fromarray(array.astype('uint8')).convert('RGB')
        b = io.BytesIO()
        image.save(b, format='JPEG')
        return b.getvalue()

    def stream_image(self):
        while True:
            time.sleep(self.sleep)
            yield from self._stream_image_formatter()
