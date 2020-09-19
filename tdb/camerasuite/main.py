import uvicorn

from tdb.camerasuite.app import app
from tdb.camerasuite.config import config

if __name__ == '__main__':
    uvicorn.run(app, host=config.app.host, port=config.app.port)
