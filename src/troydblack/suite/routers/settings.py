from fastapi import APIRouter
from starlette.requests import Request

from src.troydblack.suite.app import templates
from src.troydblack.suite.config import config


router = APIRouter()
settingsList = [s for s in config.Settings.__dict__ if not s.startswith('__')]


@router.get('/')
async def get_settings(request: Request):
    return templates.TemplateResponse('settings.html', {
        'request': request,
        'settingsList': settingsList
    })


@router.get('/uv4l')
async def get_settings_uv4l(request: Request):
    return templates.TemplateResponse('settings_uv4l.html', {
        'request': request,
        'settingsList': settingsList
    })


@router.get('/opencv')
async def get_settings_opencv(request: Request):
    return templates.TemplateResponse('settings_opencv.html', {
        'request': request,
        'settingsList': settingsList
    })
