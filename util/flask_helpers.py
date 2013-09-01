
import flask

def is_internal():
    return flask.request.remote_addr == '127.0.0.1'
