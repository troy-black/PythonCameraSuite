from fastapi import APIRouter
from starlette.requests import Request

from troydblack.suite.app import templates
from troydblack.suite.config import config, ConfigWeb, EnumDriver

router = APIRouter()


@router.get('/')
async def get_settings(request: Request):
    return templates.TemplateResponse('settings.html', {
        'request': request,
        'details': config.web.dict(),
        'drivers': EnumDriver
    })


@router.put('/', response_model=ConfigWeb)
async def put_settings(settings: ConfigWeb):
    config.web = settings
    return settings


@router.get('/mock')
async def get_settings_mock(request: Request):
    return templates.TemplateResponse('settings_mock.html', {
        'request': request,
        'details': config.web.dict(),
        'drivers': EnumDriver
    })


@router.get('/opencv')
async def get_settings_opencv(request: Request):
    return templates.TemplateResponse('settings_opencv.html', {
        'request': request,
        'details': config.web.dict(),
        'drivers': EnumDriver
    })
