from fastapi import APIRouter
from starlette.requests import Request

from troydblack.suite.camera import CameraDriver
from troydblack.suite.app import templates
from troydblack.suite.config import config, ConfigWeb, EnumDriver

router = APIRouter()


async def template(request: Request, template_name: str):
    return templates.TemplateResponse(template_name, {
        'request': request,
        'details': config.web.dict(),
        'drivers': EnumDriver
    })


@router.get('/')
async def get_settings(request: Request):
    return await template(request, 'settings.html')


@router.put('/', response_model=ConfigWeb)
async def put_settings(settings: ConfigWeb):
    return config.web.merge(settings)


@router.get('/mock')
async def get_settings_mock(request: Request):
    return await template(request, 'settings_mock.html')


@router.get('/opencv')
async def get_settings_opencv(request: Request):
    return await template(request, 'settings_opencv.html')
