from fastapi import APIRouter
from starlette.responses import StreamingResponse, Response, RedirectResponse

from config import config

router = APIRouter()


@router.get('/jpg')
async def get_jpg():
    if config.camera_driver.forwarder:
        return RedirectResponse(url=config.camera_driver.forwarder_get_jpg)
    else:
        return Response(config.camera_driver.last_image_bytes, media_type='image/jpeg')


@router.get('/stream/video')
async def get_stream_video():
    if config.camera_driver.forwarder:
        return RedirectResponse(url=config.camera_driver.forwarder_get_stream_video)
    else:
        return StreamingResponse(config.camera_driver.stream_image(),
                                 media_type='multipart/x-mixed-replace; boundary=frame')
