import logging

import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from src.troydblack.suite.utilities.modules import import_submodules
from src.troydblack.suite.config import config

logging.basicConfig(level=getattr(logging, config.App.logging))

logging.debug('Starting Application')

app = FastAPI()
app.secret_key = config.App.secret_key

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


@app.get('/')
async def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


routes = import_submodules(config.App.routers_package)
for module_name, module in routes.items():
    module_name = module_name.split('.')[-1]
    app.include_router(module.router, prefix='/' + module_name, tags=[module_name])


if __name__ == '__main__':
    uvicorn.run(app, host=config.App.host, port=config.App.port)
