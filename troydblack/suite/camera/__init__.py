class CameraDriver:
    last_image_bytes = None

    def stream_image(self):
        raise RuntimeError('Must be implemented by Driver subclass')

    def _stream_image_formatter(self):
        yield b'--frame\r\nContent-Type:image/jpeg\r\n\r\n' + self.last_image_bytes + b'\r\n'

    # @classmethod
    # def build(cls):
    #     camera_module = importlib.import_module(f'{EnumPackages.CAMERA}.{config.web.active_driver.name.lower()}')
    #     return getattr(camera_module, f'{config.web.active_driver.value}Driver')(
    #         **getattr(config, config.web.active_driver.name.lower()).dict())
