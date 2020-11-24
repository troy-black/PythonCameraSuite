import json
from typing import Dict

from fastapi import APIRouter, BackgroundTasks
from starlette.requests import Request

from tdb.camerasuite.app import templates
from tdb.camerasuite.config import (config, ConfigWeb, EnumDriver, ConfigMockDriver, ConfigOpenCvDriver,
                                    ConfigPiCameraDriver, ConfigUv4lDriver, Uv4lRestApiId)

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


@router.get('/uv4l')
async def get_settings_uv4l(request: Request):
    # TODO - move this logic to javascript to keep Python code clean/consistent
    settings: dict = await config.uv4l.get_api_videodev_settings()
    controls: list = settings.get('controls')

    current_format: Dict[str, int] = settings.get('current_format')

    # Update controls with api key
    for control in controls:
        control['api'] = Uv4lRestApiId(control.get('id')).name

    available_formats = {
        _format.get('info').get('v4l2_fourcc'): {
            'description': _format.get('info').get('description'),
            'compressed': _format.get('info').get('compressed'),
            'emulated': _format.get('info').get('emulated'),
            'max_height': _format.get('available_sizes')[0].get('max_height'),
            'max_width': _format.get('available_sizes')[0].get('max_width'),
            'min_height': _format.get('available_sizes')[0].get('min_height'),
            'min_width': _format.get('available_sizes')[0].get('min_width'),
            'step_height': _format.get('available_sizes')[0].get('step_height'),
            'step_width': _format.get('available_sizes')[0].get('step_width')
        }
        for _format in settings.get('available_formats')
    }

    formats = [
        {
            'type': 'menu',
            'name': 'v4l2_fourcc',
            'current_value': current_format.get('v4l2_fourcc'),
            'options': [
                {
                    'index': key,
                    'name': '{}{}{}{}{}{}'.format(
                        vals.get('description'),
                        ' (' if (vals.get('compressed') or vals.get('emulated')) else '',
                        'compressed' if vals.get('compressed') else '',
                        '/' if (vals.get('compressed') and vals.get('emulated')) else '',
                        'emulated' if vals.get('emulated') else '',
                        ')' if (vals.get('compressed') or vals.get('emulated')) else '',
                    )
                }
                for key, vals in available_formats.items()
            ],
        },
        {
            'type': 'integer',
            'name': 'width',
            'current_value': current_format.get('width'),
            'max': available_formats.get(current_format.get('v4l2_fourcc')).get('max_width'),
            'min': available_formats.get(current_format.get('v4l2_fourcc')).get('min_width'),
            'step': available_formats.get(current_format.get('v4l2_fourcc')).get('step_width'),
        },
        {
            'type': 'integer',
            'name': 'height',
            'current_value': current_format.get('height'),
            'max': available_formats.get(current_format.get('v4l2_fourcc')).get('max_height'),
            'min': available_formats.get(current_format.get('v4l2_fourcc')).get('min_height'),
            'step': available_formats.get(current_format.get('v4l2_fourcc')).get('step_height'),
        },
    ]

    non_members = [
        {
            'type': 'text',
            'name': key,
            'current_value': val
        }
        for (key, val) in config.uv4l.dict().items()
        if key not in Uv4lRestApiId.__members__ and key not in [
            _format.get('name')
            for _format in formats
        ]
    ]

    return await template(request, 'settings_uv4l.html', {
        'available_formats': json.dumps(available_formats),
        'controls': non_members + formats + controls
    })


@router.put('/uv4l', response_model=ConfigUv4lDriver)
async def put_settings_uv4l(settings: ConfigUv4lDriver):
    config.uv4l.merge(settings)

    if config.web.active_driver == EnumDriver.UV4L:
        config.load_camera_driver()

    response: dict = await config.uv4l.put_api_videodev_settings()

    if response.get('response').get('code') != 200:
        # reload settings
        results: dict = await config.uv4l.get_api_videodev_settings()
        for control in results.get('controls'):
            setattr(config.uv4l, Uv4lRestApiId(control.get('id')).name, control.get('current_value'))

        for key, val in results.get('current_format').items():
            setattr(config.uv4l, key, val)

        config.uv4l.save()

    return config.uv4l
