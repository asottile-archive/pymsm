
import flask
import mako.lookup

# TODO: this file belongs in web

template_lookup = mako.lookup.TemplateLookup(
    directories=['web/templates'],
)

def is_internal():
    return flask.request.remote_addr == '127.0.0.1'

def render_template_mako(template, **env):
    """Renders a mako template."""
    new_env = {
        'is_internal': is_internal(),
    }
    new_env.update(env)

    template = template_lookup.get_template(template)
    return template.render(**new_env)
