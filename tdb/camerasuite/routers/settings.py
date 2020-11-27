import json
from typing import Dict

from fastapi import APIRouter, BackgroundTasks
from starlette.requests import Request

from tdb.camerasuite.app import templates
from tdb.camerasuite.config import (config, ConfigWeb, EnumDriver, ConfigMockDriver, ConfigOpenCvDriver,
                                    ConfigPiCameraDriver)

router = APIRouter()


async def template(request: Request, template_name: str, details: dict):
    return templates.TemplateResponse(template_name, {
        'request': request,
        'details': details,
        'settings': {
            'display': {
                k: v
                for k, v in config.web.dict().items()
                if k.startswith('display_')
            },
            'drivers': [
                d
                for d in EnumDriver
                if d.lower() in config.camera_drivers
            ]
        }
    })


@router.get('/')
async def get_settings(request: Request):
    return await template(request, 'settings.html', config.web.dict())


@router.put('/', response_model=ConfigWeb)
async def put_settings(settings: ConfigWeb):
    config.web.merge(settings)
    if config.last_driver != config.web.active_driver:
        config.load_camera_driver()
    return config.web


@router.get('/mock')
async def get_settings_mock(request: Request):
    return await template(request, 'settings_mock.html', config.mock.dict())


@router.put('/mock', response_model=ConfigMockDriver)
async def put_settings_mock(settings: ConfigMockDriver):
    config.mock.merge(settings)
    if config.web.active_driver == EnumDriver.MOCK:
        config.load_camera_driver()
    return config.mock


@router.get('/opencv')
async def get_settings_opencv(request: Request):
    return await template(request, 'settings_opencv.html', config.opencv.dict())


@router.put('/opencv', response_model=ConfigOpenCvDriver)
async def put_settings_opencv(settings: ConfigOpenCvDriver):
    config.opencv.merge(settings)
    if config.web.active_driver == EnumDriver.OPENCV:
        config.load_camera_driver()
    return config.opencv


@router.get('/picamera')
async def get_settings_picamera(request: Request):
    details: dict = config.picamera.dict()
    # details['exposure_modes'] = [
    #     'off',
    #     'auto',
    #     'night',
    #     'nightpreview',
    #     'backlight',
    #     'spotlight',
    #     'sports',
    #     'snow',
    #     'beach',
    #     'verylong',
    #     'fixedfps',
    #     'antishake',
    #     'fireworks',
    # ]
    return await template(request, 'settings_picamera.html', details)


@router.put('/picamera', response_model=ConfigPiCameraDriver)
async def put_settings_picamera(settings: ConfigPiCameraDriver, background_tasks: BackgroundTasks):
    config.picamera.merge(settings)
    if config.web.active_driver == EnumDriver.PICAMERA:
        config.load_camera_driver()
    # config.camera_driver.background_task = True
    # background_tasks.add_task(config.camera_driver.generate_image)
    return config.picamera

