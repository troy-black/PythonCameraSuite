import logging

from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from src.troydblack.suite.config import config, WebBase
from src.troydblack.suite.utilities.modules import import_submodules

logging.basicConfig(level=getattr(logging, config.base.logging))

logging.debug('Starting Application')

app = FastAPI()
app.secret_key = WebBase().secret_key

templates = Jinja2Templates(directory='templates')

routes = import_submodules(WebBase().routers_package)
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


def mount(*, url: str, directory: str, name: str):
    app.mount(url, StaticFiles(directory=directory), name=name)
