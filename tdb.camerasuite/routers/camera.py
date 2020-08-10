from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import StreamingResponse, Response

from app import templates
from config import config

router = APIRouter()


@router.get('/jpg')
async def get_jpg():
    return Response(config.camera_driver.last_image_bytes, media_type='image/jpeg')


@router.get('/stream/video')
async def get_stream_video():
    return StreamingResponse(config.camera_driver.stream_image(),
                             media_type='multipart/x-mixed-replace; boundary=frame')


@router.get('/stream')
async def get_stream(request: Request):
    return templates.TemplateResponse('stream.html', {'request': request})
