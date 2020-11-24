import logging

from tdb.camerasuite.camera import CameraDriver
from tdb.camerasuite.config import ConfigUv4lDriver

from tdb.camerasuite.utilities import networking
from tdb.camerasuite.utilities.commands import Process


def service_uv4l_raspicam(action: str) -> int:
    return Process(['service', 'uv4l_raspicam'] + [action]).run()


class Uv4lDriver(CameraDriver):
    def __init__(self, settings: ConfigUv4lDriver):
        self._settings: ConfigUv4lDriver = settings
        self.forwarder = True
        self.forwarder_get_jpg = f'http://{networking.get_hostname()}:{self._settings.port}/stream/snapshot.jpeg'
        self.forwarder_get_stream_video = f'http://{networking.get_hostname()}:{self._settings.port}/stream/video.mjpeg'

        # force service restart
        if service_uv4l_raspicam('status') != 3:  # stopped state exit code
            logging.debug(service_uv4l_raspicam('stop'))
        logging.debug(service_uv4l_raspicam('start'))

    def __del__(self):
        # force service stop
        logging.debug(service_uv4l_raspicam('stop'))


if service_uv4l_raspicam('status') == 1:
    raise ImportError('cannot find service uv4l_raspicam')
