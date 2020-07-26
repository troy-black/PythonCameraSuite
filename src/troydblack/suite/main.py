import logging

import uvicorn
from fastapi import FastAPI

from src.troydblack.suite.utilities.modules import import_submodules
from src.troydblack.suite.config import config

logging.basicConfig(level=getattr(logging, config.App.logging))

logging.debug('Starting Application')

app = FastAPI()
app.secret_key = config.App.secret_key

routes = import_submodules('src.troydblack.suite.routers')
for module_name, module in routes.items():
    module_name = module_name.split('.')[-1]
    app.include_router(module.router, prefix='/' + module_name, tags=[module_name])


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
