from fastapi import APIRouter, BackgroundTasks
from starlette.responses import StreamingResponse, Response, RedirectResponse

from tdb.camerasuite.config import config

router = APIRouter()


@router.get('/jpg')
async def get_jpg():
    if not config.camera_driver.background_task:
        config.camera_driver.generate_image()
    if config.camera_driver.forwarder:
        return RedirectResponse(url=config.camera_driver.forwarder_get_jpg)
    else:
        return Response(config.camera_driver.last_image_bytes, media_type='image/jpeg')


@router.get('/stream/video')
async def get_stream_video():
    if config.camera_driver.forwarder:
        return RedirectResponse(url=config.camera_driver.forwarder_get_stream_video)
    else:
        return StreamingResponse(config.camera_driver.stream_images(),
                                 media_type='multipart/x-mixed-replace; boundary=frame')


@router.get('/stream/start')
async def get_stream_start(background_tasks: BackgroundTasks):
    config.camera_driver.background_task = True
    background_tasks.add_task(config.camera_driver.generate_images)
    return {
        'result': 'start'
    }


@router.get('/stream/stop')
async def get_stream_stop():
    config.camera_driver.background_task = False
    return {
        'result': 'stop'
    }
