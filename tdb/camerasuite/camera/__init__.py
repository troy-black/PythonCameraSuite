from pydantic import BaseModel
from threading import Event


class CameraDriver(object):
    background_task = False
    last_image_bytes = None

    # used to forward to external url instead of generating img in Python
    forwarder: bool = False
    forwarder_get_jpg: str = None
    forwarder_get_stream_video: str = None

    event: Event
    # _settings: BaseModel

    def generate_image(self):
        raise RuntimeError('Must be implemented by Driver subclass')

    def stream_image(self):
        while self.background_task:
            self.event.wait()
            print('yield')
            yield b'--frame\r\nContent-Type:image/jpeg\r\n\r\n' + self.last_image_bytes + b'\r\n'
