import uvicorn

from troydblack.suite.app import app, config, mount


if __name__ == '__main__':
    mount(url='/static', directory='static', name='static')
    uvicorn.run(app, host=config.app.host, port=config.app.port)
