import uvicorn

from src.troydblack.suite.app import app, config, mount


mount(url='/static', directory='static', name='static')

if __name__ == '__main__':
    uvicorn.run(app, host=config.App.host, port=config.App.port)
