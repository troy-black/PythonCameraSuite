class ConfigBase:
    """
    Default Config Profile
    """
    class App:
        routers_package: str = 'src.troydblack.suite.routers'
        secret_key: str = 'change_me_before_using_in_production'
        logging: str = 'NOTSET'  # CRITICAL, ERROR, WARNING, INFO, DEBUG
        host: str = '0.0.0.0'
        port: int = 8000

    class Camera:
        module = 'src.troydblack.suite.camera.mock'
        driver = 'MockDriver'
        kwargs = {
            'width': 1280,
            'height': 720,
            'sleep': 1 / 15  # FPS
        }

    class Uv4l:
        external: bool
        host: str
        steam_url: str
