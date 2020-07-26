class ConfigBase:

    class App:
        secret_key = 'QWXYYESG3TVD32HRYHM3HXAA45SRW6QP'
        logging = 'DEBUG'

    class Camera:
        module = 'src.troydblack.suite.camera.opencv'
        driver = 'OpenCvDriver'
        kwargs = {
            'source': 'http://192.168.1.157:8080/stream/video.mjpeg'
        }

    class Uv4l:
        pass
