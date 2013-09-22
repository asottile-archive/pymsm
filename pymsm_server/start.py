
import flask
import os.path

from pymsm_server.jar import jar
from pymsm_server.jar_creation import jar_creation
from util.flask_helpers import render_template

EXTENSIONS_TO_MIMETYPES = {
    '.js': 'application/javascript',
    '.css': 'text/css',
}

app = flask.Flask(__name__)
app.register_blueprint(jar_creation)
app.register_blueprint(jar)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.htm')

@app.route('/<path:path>')
def catch_all(path):
    # I assume there's a better way to serve static assets
    if not app.debug:
        flask.abort(404)

    # Don't want to serve files that aren't of the type we expect
    if not any(
        path.endswith(extension)
        for extension in EXTENSIONS_TO_MIMETYPES.keys()
    ):
        flask.abort(404)

    # Try and serve that file
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
