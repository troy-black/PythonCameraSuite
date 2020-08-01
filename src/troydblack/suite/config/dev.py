# from src.troydblack.suite.config.config import ConfigBase
#
#
# class Config(ConfigBase):
#     class App(ConfigBase.App):
#         logging = 'DEBUG'
#         driver = 'OpenCvDriver'
#
#     class Camera(ConfigBase.Camera):
#         module = 'src.troydblack.suite.camera.opencv'
#         driver = 'OpenCvDriver'
#         kwargs = {
#             '': 0  # local USB Cam 0
#         }
#
#     class Uv4l(ConfigBase.Uv4l):
#         external: bool = True
#         host: str = '192.168.1.157:8080'
#         steam_url: str = f'http://{host}/stream/video.mjpeg'
