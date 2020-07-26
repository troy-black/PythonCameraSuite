from src.troydblack.suite.config.config import ConfigBase


class Config(ConfigBase):
    class App(ConfigBase.App):
        logging = 'DEBUG'

    class Camera(ConfigBase.Camera):
        module = 'src.troydblack.suite.camera.opencv'
        driver = 'OpenCvDriver'
        kwargs = {
            'source': 0  # local USB Cam 0
        }

    class Uv4l(ConfigBase.Uv4l):
        external: bool = True
        host: str = '192.168.1.xxx:8080'
        steam_url: str = f'http://{host}/stream/video.mjpeg'