import uvicorn

from app import mount, app
from config import config

if __name__ == '__main__':
    mount(url='/static', directory='static', name='static')
    uvicorn.run(app, host=config.app.host, port=config.app.port)
