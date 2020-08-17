from fastapi import APIRouter
from starlette.requests import Request

from app import templates
from config import config, ConfigWeb, EnumDriver, ConfigMockDriver, ConfigOpenCvDriver

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
            'drivers': EnumDriver
        }
    })


@router.get('/')
async def get_settings(request: Request):
    return await template(request, 'settings.html', config.web.dict())


@router.put('/', response_model=ConfigWeb)
async def put_settings(settings: ConfigWeb):
    return config.web.merge(settings)


@router.get('/mock')
async def get_settings_mock(request: Request):
    return await template(request, 'settings_mock.html', config.mock.dict())


@router.put('/mock', response_model=ConfigMockDriver)
async def put_settings_mock(settings: ConfigMockDriver):
    return config.mock.merge(settings)


@router.get('/opencv')
async def get_settings_opencv(request: Request):
    return await template(request, 'settings_opencv.html', config.opencv.dict())


@router.put('/opencv', response_model=ConfigOpenCvDriver)
async def put_settings_opencv(settings: ConfigOpenCvDriver):
    return config.opencv.merge(settings)
