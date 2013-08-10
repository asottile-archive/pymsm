
import flask
import threading

from util.decorators import require_internal

app = flask.Flask(__name__)

servers_lock = threading.Lock()
servers = []

@app.route('/')
@require_internal
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()

    print 'after'
