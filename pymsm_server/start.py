
import flask
import os.path
import simplejson

from jar_downloader.discovery import get_jar_downloaders
from util.decorators import require_internal

EXTENSIONS_TO_MIMETYPES = {
    '.js': 'application/javascript',
    '.css': 'text/css',
}

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return flask.render_template('index.htm')

@app.route('/available_jars', methods=['GET'])
@require_internal
def available_jars():
    jar_downloaders = get_jar_downloaders()
    jar_downloader_names = [
        jar_downloader.__name__ for jar_downloader in jar_downloaders
    ]
    return simplejson.dumps(jar_downloader_names)

@app.route('/<path:path>')
def catch_all(path):
    if not app.debug:
        flask.abort(404)
    try:
        # Make the paths relative to where this file is
        path = os.path.join(
            os.path.split(os.path.abspath(__file__))[0],
            path
        )

        with open(path, 'r') as f:
            extension = os.path.splitext(path)[1]
            return flask.Response(
                f.read(),
                mimetype=EXTENSIONS_TO_MIMETYPES.get(extension, 'text/html')
            )
    except IOError:
        flask.abort(404)

if __name__ == '__main__':
    app.run(debug=True)

    print 'after'
