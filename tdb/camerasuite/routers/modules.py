from fastapi import APIRouter
from starlette.requests import Request

from tdb.camerasuite.app import templates
from tdb.camerasuite.config import config

router = APIRouter()


async def template(request: Request, template_name: str, details: dict):
    return templates.TemplateResponse(template_name, {
        'request': request,
        'details': details,
    })


@router.get('/celestial_tracker')
async def get_celestial_tracker(request: Request):
    return await template(request, 'celestial_tracker.html', {})


@router.get('/security')
async def get_security(request: Request):
    return await template(request, 'security.html', {})


@router.get('/astronomy')
async def get_astronomy(request: Request):
    details: dict = getattr(config, config.web.active_driver.lower()).dict()
    details['active_driver'] = config.web.active_driver.lower()
    details['stream_switch'] = config.camera_driver.background_task
    return await template(request, 'astronomy.html', details)
