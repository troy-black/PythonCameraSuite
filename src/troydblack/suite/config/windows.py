from src.troydblack.suite.config.config import ConfigBase


class Config(ConfigBase):
    class Uv4l:
        external = True
        base_url = 'http://192.168.1.157:8080/'
        stream_url = 'http://192.168.1.157:8080/stream'
        webrtc_url = 'http://192.168.1.157:8080/stream/webrtc'
