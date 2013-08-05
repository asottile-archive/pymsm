
import flask
import functools

def require_internal(func):
    """Requires that the user is viewing from localhost."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if flask.request.remote_addr != '127.0.0.1':
            flask.abort(403)
        return func(*args, **kwargs)
    return wrapper
