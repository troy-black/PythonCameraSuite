from fastapi import APIRouter
from starlette.requests import Request

from app import templates

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
