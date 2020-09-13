from camera import CameraDriver
from config import ConfigUv4lDriver

from utilities.commands import Process


class Uv4lDriver(CameraDriver):
    cmd: list = ['sudo', 'service', 'uv4l_raspicam']

    def __init__(self, settings: ConfigUv4lDriver):
        self._settings: ConfigUv4lDriver = settings
        self.forwarder = True
        self.forwarder_get_jpg = f'http://{self._settings.host}:{self._settings.port}/stream/snapshot.jpeg'
        self.forwarder_get_stream_video = f'http://{self._settings.host}:{self._settings.port}/stream/video.mjpeg'
        if self.service_uv4l_raspicam('status') != 0:
            self.service_uv4l_raspicam('start')

    def __del__(self):
        self.service_uv4l_raspicam('stop')

    def service_uv4l_raspicam(self, action):
        process = Process(self.cmd + [action])
        process.run()
        return process.returncode
