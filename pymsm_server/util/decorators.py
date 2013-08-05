
import flask
import functools

_NONE_PASSED = object()

def require_internal(func=_NONE_PASSED):
    """Requires that the user is viewing from localhost.

    Usage:

    @app.route('/')
    @require_internal
    def foo():

    Or use as a plain method

    def foo():
        require_internal()

    Args:
        func - Function to be wrapped. If it is none this was just called
            directly and should just check the assertion.
    """
    if func is _NONE_PASSED:
        if flask.request.remote_addr != '127.0.0.1':
            flask.abort(403)
        return

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        require_internal()
        return func(*args, **kwargs)
    return wrapper
