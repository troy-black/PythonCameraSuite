from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import StreamingResponse, Response

from troydblack.suite.camera import CameraDriver
from troydblack.suite.config import config, get_camera_driver
from troydblack.suite.app import templates

router = APIRouter()

camera_driver: CameraDriver = get_camera_driver(config.web.active_driver)


@router.get('/jpg')
def get_jpg():
    return Response(camera_driver.last_image_bytes, media_type='image/jpeg')


@router.get('/stream/video')
async def get_stream_video():
    """Return async video streaming response"""
    return StreamingResponse(camera_driver.stream_image(), media_type='multipart/x-mixed-replace; boundary=frame')


@router.get('/stream')
async def get_stream(request: Request):
    return templates.TemplateResponse('stream.html', {'request': request})
