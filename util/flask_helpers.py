
import flask

def is_internal():
    return flask.request.remote_addr == '127.0.0.1'

def render_template(template, **env):
    """Wrapper around flask.render_template to add our globally expected
    environment variables.
    """
    new_env = {
        'is_internal': is_internal(),
    }
    new_env.update(env)
    return flask.render_template(template, **new_env)
