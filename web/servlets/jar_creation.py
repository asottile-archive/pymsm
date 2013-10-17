
import flask
import markupsafe
import re

from jar_downloader.discovery import get_jar_downloaders
from jar_downloader.discovery import get_jar_downloader_map
from jar_downloader.discovery import get_user_jars
from jar_downloader.helpers import create_jar_directory
from util.decorators import require_internal
from presentation.jar_downloader import JarDownloader
from schemaform.form import Form
from schemaform.helpers import el
from schemaform.single_input_property import SingleInputProperty
from web.flask_helpers import render_template_mako

jar_creation = flask.Blueprint(
    'jar_creation', __name__, template_folder='../templates/jar_creation'
)

USER_JAR_NAME_REGEX = re.compile('^[a-zA-Z-_]+$')

def get_jar_downloader_presenters():
    """Returns JarDownloader presenters for each jar downloader installed."""
    return sorted(
        (
            JarDownloader(jar_downloader_cls)
            for jar_downloader_cls in get_jar_downloaders()
        ),
        key=lambda jar_downloader: jar_downloader.name
    )

def get_jar_create_form(jar_type):
    """Returns a form for creating a jar given its name.  The returned form
    has (in addition to the form elements retrieved from the jar itself) a
    hidden element denoting the name of the jar.  It also has an input for the
    user to add a name to jar and a submit button.
    """
    # TODO: validate the jar name and redirect back if nonsense, for now error
    jar_presenter = JarDownloader(get_jar_downloader_map()[jar_type])

    # Need to add a hidden field for the jar name and a text entry for
    # what the name they are giving it
    form_pq = Form(
        jar_presenter.jar_downloader_cls.get_config_schema(),
        method='POST',
        action=flask.url_for('jar_creation.create_jar', jar_type=jar_type),
    ).__pq__()
    user_jar_name_input = SingleInputProperty(
        '',
        'user_jar_name',
        {'type': 'string', 'label': 'Your Jar Name'},
    )
    form_pq.prepend(user_jar_name_input.__pq__())
    form_pq.append(el('input', type='submit', value='Submit',))
    jar_form_markup = markupsafe.Markup(form_pq.__html__())

    return jar_form_markup


@jar_creation.route('/jar_list', methods=['GET'])
@require_internal
def jar_list():
    jar_downloaders = get_jar_downloader_presenters()
    user_jars = get_user_jars()
    return render_template_mako(
        'jar_creation/jar_list.mako',
        jar_downloaders=jar_downloaders,
        user_jars=user_jars,
    )

@jar_creation.route('/new_jar/<jar_type>', methods=['GET'])
@require_internal
def new_jar(jar_type):
    jar_form_markup = get_jar_create_form(jar_type)
    return render_template_mako(
        'jar_creation/new_jar.mako',
        jar_form_markup=jar_form_markup,
    )

@jar_creation.route('/create_jar/<jar_type>', methods=['POST'])
@require_internal
def create_jar(jar_type):
    jar_downloader_cls = get_jar_downloader_map()[jar_type]
    form = Form(jar_downloader_cls.get_config_schema())
    values, errors = form.load_from_form(flask.request.form)

    user_jar_name = flask.request.form['user_jar_name']
    if not USER_JAR_NAME_REGEX.match(user_jar_name):
        # TODO: need to do something wtih reporting this as an error
        assert False

    if errors:
        # TODO: need to do something with validating errors
        assert False

    # TODO: there is a ValueError to catch here for already created jar
    # directory.  Should really make this a more specific exception and also
    # handle it appropriately here.
    create_jar_directory(jar_type, user_jar_name, values)

    # TODO: redirect to Jars List with success message
    return 'Jar created successfully.'
