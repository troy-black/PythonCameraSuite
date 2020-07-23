import logging

import flask

from src.troydblack.camera.config import config

logging.debug('Starting Application')

app = flask.Flask(__name__)
app.secret_key = config['APP'].get('secret_key')

# Force JSON to Return as Pretty/Readable Print
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/status')
def app_status():
    return flask.jsonify({
        'status': 'Running'
    })


if __name__ == '__main__':
    app.run('localhost', 8080)
