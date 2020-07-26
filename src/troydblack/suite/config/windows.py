from src.troydblack.suite.config.config import ConfigBase


class Config(ConfigBase):
    class Camera(ConfigBase.Camera):
        module = 'src.troydblack.suite.camera.opencv'
        driver = 'OpenCvDriver'
        kwargs = {
            'source': 0  # local USB Cam 0
        }