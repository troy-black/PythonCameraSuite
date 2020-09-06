from pydantic import BaseModel

NOT_IMPLEMENTED = 'Must be implemented by Driver subclass'


class CameraDriver:
    last_image_bytes = None

    # used to forward to external url instead of generating img in Python
    forwarder: bool = False
    forwarder_get_jpg: str = None
    forwarder_get_stream_video: str = None

    _settings: BaseModel

    def stream_image(self):
        raise RuntimeError(NOT_IMPLEMENTED)

    def _stream_image_formatter(self):
        yield b'--frame\r\nContent-Type:image/jpeg\r\n\r\n' + self.last_image_bytes + b'\r\n'
