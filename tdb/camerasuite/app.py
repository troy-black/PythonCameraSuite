import logging

from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from tdb.camerasuite.config import config, EnumPackages
from tdb.camerasuite.utilities import import_submodules

# logging.basicConfig(level=getattr(logging, config.app.logging))

logging.debug('Starting Application')

app = FastAPI()

# TODO - security
# app.secret_key = secret_key

templates = Jinja2Templates(directory='tdb/camerasuite/templates')
app.mount('/static', StaticFiles(directory='tdb/camerasuite/static'), name='static')
app.mount('/storage', StaticFiles(directory='tdb/camerasuite/storage'), name='storage')

routes = import_submodules(EnumPackages.ROUTERS)
for module_name, module in routes.items():
    module_name = module_name.split('.')[-1]
    app.include_router(module.router, prefix='/' + module_name, tags=[module_name])


@app.get('/')
async def get_home(request: Request):
    return templates.TemplateResponse('home.html', {
        'request': request,
        'title': 'Home',
        'navigation': {
            'About': 'get_about'
        }
    })


@app.get('/about')
async def get_about(request: Request):
    return templates.TemplateResponse('about.html', {'request': request})
