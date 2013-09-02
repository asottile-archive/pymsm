
import flask
import markupsafe
import simplejson

from jar_downloader.discovery import get_jar_downloaders
from jar_downloader.discovery import get_jar_downloader_map
from util.decorators import require_internal
from util.flask_helpers import render_template
from presentation.jar_downloader import JarDownloader
from schemaform.form import Form
from schemaform.helpers import el
from schemaform.single_input_property import SingleInputProperty

jar_creation = flask.Blueprint(
    'jar_creation', __name__, template_folder='templates/jar_creation'
)

def get_jar_downloader_presenters():
    """Returns JarDownloader presenters for each jar downloader installed."""
    return sorted(
        (
            JarDownloader(jar_downloader_cls)
            for jar_downloader_cls in get_jar_downloaders()
        ),
        key=lambda jar_downloader: jar_downloader.name
    )

def get_jar_create_form(jar_name):
    """Returns a form for creating a jar given its name.  The returned form
    has (in addition to the form elements retrieved from the jar itself) a
    hidden element denoting the name of the jar.  It also has an input for the
    user to add a name to jar and a submit button.
    """
    # TODO: validate the jar name and redirect back if nonsense, for now error
    jar_presenter = JarDownloader(get_jar_downloader_map()[jar_name])

    # Need to add a hidden field for the jar name and a text entry for
    # what the name they are giving it
    form_pq = Form(
        jar_presenter.jar_downloader_cls.get_config_schema(),
        method='POST',
        action=flask.url_for('jar_creation.create_jar'),
    ).__pq__()
    jar_name_input = el('input', type='hidden', name='jar_name', value=jar_name)
    user_jar_name_input = SingleInputProperty(
        '',
        'user_jar_name',
        {'type': 'string', 'label': 'Your Jar Name'},
    )
    form_pq.prepend(jar_name_input + user_jar_name_input.__pq__())
    form_pq.append(el('input', type='submit', value='Submit',))
    jar_form_markup = markupsafe.Markup(form_pq.__html__())

    return jar_form_markup

@jar_creation.route('/available_jars', methods=['GET'])
@require_internal
def available_jars():
    jar_downloaders = get_jar_downloader_presenters()
    jar_downloader_names = [jar.name for jar in jar_downloaders]
    return simplejson.dumps(jar_downloader_names)

@jar_creation.route('/jar_list', methods=['GET'])
@require_internal
def jar_list():
    jar_downloaders = get_jar_downloader_presenters()
    return render_template('jar_list.htm', jar_downloaders=jar_downloaders)

@jar_creation.route('/new_jar/<jar_name>')
@require_internal
def new_jar(jar_name):
    jar_form_markup = get_jar_create_form()
    return render_template('new_jar.htm', jar_form_markup=jar_form_markup)

@jar_creation.route('/create_jar', methods=['POST'])
@require_internal
def create_jar():
    return 'Hello World'
