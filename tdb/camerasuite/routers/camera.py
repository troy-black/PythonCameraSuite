import os
from datetime import datetime
from zipfile import ZipFile

from fastapi import APIRouter, BackgroundTasks
from starlette.responses import StreamingResponse, Response, FileResponse

from camerasuite.models import ZipFileRequest
from camerasuite.utilities import verify_file_exists, verify_folder
from tdb.camerasuite.config import config

router = APIRouter()

img_path = f'tdb/camerasuite/storage/img/'
zip_path = 'tdb/camerasuite/storage/zip/'


@router.get('/jpg')
async def get_jpg():
    if not config.camera_driver.background_task:
        config.camera_driver.generate_image()
    return Response(config.camera_driver.last_image_bytes, media_type='image/jpeg')


@router.get('/jpg/{path}/{filename}')
async def get_jpg_save_or_load(path: str, filename: str):
    last_image_bytes = None
    full_path = f'{img_path}{path}'
    if not verify_file_exists(full_path, filename):
        verify_folder(full_path)
        if not config.camera_driver.background_task:
            config.camera_driver.generate_image()
        with open(f'{full_path}/{filename}', 'wb') as file:
            last_image_bytes = config.camera_driver.last_image_bytes
            file.write(last_image_bytes)
    if not last_image_bytes:
        with open(f'{full_path}/{filename}', 'rb') as file:
            last_image_bytes = file.read()

    return Response(last_image_bytes or config.camera_driver.last_image_bytes, media_type='image/jpeg')


@router.get('/stream/video')
async def get_stream_video():
    if not config.camera_driver.background_task:
        config.camera_driver.generate_image()
        return Response(config.camera_driver.last_image_bytes, media_type='image/jpeg')
    return StreamingResponse(config.camera_driver.stream_images(),
                             media_type='multipart/x-mixed-replace; boundary=frame')


@router.get('/stream/{boolean}')
async def get_stream_action(boolean: bool, background_tasks: BackgroundTasks):
    config.camera_driver.background_task = boolean
    if boolean:
        background_tasks.add_task(config.camera_driver.generate_images)
    return {
        'result': boolean
    }


@router.get('/zip/{zip_filename}')
async def get_zip(zip_filename: str, background_tasks: BackgroundTasks):
    def delete_file():
        os.remove(f'{zip_path}{zip_filename}')

    background_tasks.add_task(delete_file)
    return FileResponse(f'{zip_path}{zip_filename}', media_type='application/zip', filename=zip_filename)


@router.post('/zip')
async def put_download_zip_request(zip_file_request: ZipFileRequest):
    zip_filename = f'{datetime.now().strftime("%Y%m%d%H%M%S%f")}.zip'
    verify_folder(zip_path)
    with ZipFile(f'{zip_path}{zip_filename}', mode='x') as zipfile:
        for file in zip_file_request.files:
            if file:
                zipfile.write(f'{img_path}{file}', arcname=file)
    return {
        'zip_filename': zip_filename
    }
