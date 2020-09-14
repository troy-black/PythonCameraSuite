from tdb.camerasuite.camera import CameraDriver
from tdb.camerasuite.config import ConfigUv4lDriver

from tdb.camerasuite.utilities.commands import Process


def service_uv4l_raspicam(action: str) -> int:
    return Process(['sudo', 'service', 'uv4l_raspicam'] + [action]).run()


class Uv4lDriver(CameraDriver):
    def __init__(self, settings: ConfigUv4lDriver):
        self._settings: ConfigUv4lDriver = settings
        self.forwarder = True
        self.forwarder_get_jpg = f'http://{self._settings.host}:{self._settings.port}/stream/snapshot.jpeg'
        self.forwarder_get_stream_video = f'http://{self._settings.host}:{self._settings.port}/stream/video.mjpeg'

        # force service restart
        if service_uv4l_raspicam('status') != 3:  # stopped state exit code
            service_uv4l_raspicam('stop')
        service_uv4l_raspicam('start')

    def __del__(self):
        # force service stop
        service_uv4l_raspicam('stop')


if service_uv4l_raspicam('status') == 1:
    raise ImportError('cannot find service uv4l_raspicam')
