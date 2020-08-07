from fastapi import APIRouter
from starlette.requests import Request

from troydblack.suite.app import templates
from troydblack.suite.config import config, ConfigWeb, EnumDriver

router = APIRouter()


async def template(request: Request, name: str):
    return templates.TemplateResponse(f'{name}.html', {
        'request': request,
        'details': config.web.dict(),
        'drivers': EnumDriver
    })


@router.get('/')
async def get_settings(request: Request):
    return await template(request, 'settings')


@router.put('/', response_model=ConfigWeb)
async def put_settings(settings: ConfigWeb):
    config.web = ConfigWeb({**config.web.dict(), **settings.dict()})
    return config.web


@router.get('/mock')
async def get_settings_mock(request: Request):
    return await template(request, 'settings_mock')


@router.get('/opencv')
async def get_settings_opencv(request: Request):
    return await template(request, 'settings_opencv')
