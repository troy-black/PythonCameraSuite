import threading
from time import time


class CameraDriver(object):
    background_task = False
    last_image_bytes = None

    # used to forward to external url instead of generating img in Python
    forwarder: bool = False
    forwarder_get_jpg: str = None
    forwarder_get_stream_video: str = None

    def __init__(self):
        self.timestamp = time()
        self.lock = threading.Lock()
        self.event = threading.Event()
        self.event.clear()
        self.fps = 0.0

    def activate_camera(self):
        pass

    def deactivate_camera(self):
        pass

    def generate_images(self):
        lock = self.lock.acquire(False)

        if lock:
            self.activate_camera()
            while self.background_task:
                self.generate_image(False)

            self.deactivate_camera()
            self.lock.release()

    def generate_image(self, set_lock=True):
        lock = self.lock.acquire(False) if set_lock else True

        if lock:
            if set_lock:
                self.activate_camera()
            self._generate_image(set_lock)

            self.fps = ((1.0 / (time() - self.timestamp)) + self.fps) / 2
            self.timestamp = time()

            self.event.set()
            self.event.clear()

            if set_lock:
                self.deactivate_camera()
                self.lock.release()

    def _generate_image(self, set_lock: bool):
        raise RuntimeError('Must be implemented by Driver subclass')

    def stream_images(self):
        while self.background_task:
            if self.last_image_bytes:
                yield b'--frame\r\nContent-Type:image/jpeg\r\n\r\n' + self.last_image_bytes + b'\r\n'
            self.event.wait()
