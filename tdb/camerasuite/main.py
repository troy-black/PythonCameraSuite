import uvicorn
# from starlette.staticfiles import StaticFiles

from tdb.camerasuite.app import app
from tdb.camerasuite.config import config

if __name__ == '__main__':
    # app.mount('/static', StaticFiles(directory='tdb/camerasuite/static'), name='static')
    uvicorn.run(app, host=config.app.host, port=config.app.port)
