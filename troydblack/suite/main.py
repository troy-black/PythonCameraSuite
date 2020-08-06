import uvicorn

from troydblack.suite.app import app, config, mount


mount(url='/static', directory='static', name='static')

if __name__ == '__main__':
    uvicorn.run(app, host=config.app.host, port=config.app.port)
