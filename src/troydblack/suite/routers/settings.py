from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request

from src.troydblack.suite.app import templates
from troydblack.suite.config import config, EnumDriver

router = APIRouter()


@router.get('/')
async def get_settings(request: Request):
    return templates.TemplateResponse('settings.html', {
        'request': request,
        'activeDriver': config.web.active_driver.value,
        'drivers': ['Settings'] + [d.value for d in EnumDriver],
        'displayDrivers': [
            d.value
            for d in EnumDriver
            if getattr(config.web, f'display_{d.name.lower()}', False)
        ]
    })


class TestClass(BaseModel):
    defaultDriver: str
    Mock: str
    OpenCv: str


@router.put('/', response_model=TestClass)
async def put_settings(a: TestClass):
    return a


@router.get('/mock')
async def get_settings_mock(request: Request):
    return templates.TemplateResponse('settings_mock.html', {
        'request': request,
        # 'settingsDetails': get_settings_details()
    })


@router.get('/opencv')
async def get_settings_opencv(request: Request):
    return templates.TemplateResponse('settings_opencv.html', {
        'request': request,
        # 'settingsDetails': get_settings_details()
    })


# @router.get('/uv4l')
# async def get_settings_uv4l(request: Request):
#     return templates.TemplateResponse('settings_uv4l.html', {
#         'request': request,
#         'settingsList': settingsList
#     })
