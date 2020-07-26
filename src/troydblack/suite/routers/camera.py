import importlib

from fastapi import APIRouter
from starlette.responses import StreamingResponse, Response

from src.troydblack.suite.camera import CameraDriver
from src.troydblack.suite.config import config

router = APIRouter()

camera_module = importlib.import_module(config.Camera.module)
camera_driver: CameraDriver = getattr(camera_module, config.Camera.driver)(**config.Camera.kwargs)


@router.get('/jpg')
def get_jpg():
    return Response(camera_driver.last_image_bytes, media_type='image/jpeg')


@router.get('/video')
async def get_video_stream():
    """Return async video streaming response"""
    return StreamingResponse(camera_driver.stream_image(), media_type='multipart/x-mixed-replace; boundary=frame')
