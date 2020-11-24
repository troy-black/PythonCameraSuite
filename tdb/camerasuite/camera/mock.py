import io
import time

import numpy
from PIL import Image

from tdb.camerasuite.camera import CameraDriver
from tdb.camerasuite.config import ConfigMockDriver


class MockDriver(CameraDriver):
    def __init__(self, settings: ConfigMockDriver):
        super().__init__()
        self._settings: ConfigMockDriver = settings
        self.height = settings.height
        self.width = settings.width
        self.mock_fps = settings.fps

    def _generate_image(self, *args):
        try:
            # Random color array
            array = numpy.random.rand(self.height, self.width, 3) * 255
            image = Image.fromarray(array.astype('uint8')).convert('RGB')
            _bytes = io.BytesIO()
            image.save(_bytes, format='JPEG')

            self.last_image_bytes = _bytes.getvalue()

            time.sleep(1 / self.mock_fps)

        except Exception as e:
            return None
