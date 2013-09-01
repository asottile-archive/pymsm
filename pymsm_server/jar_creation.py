
import flask
import simplejson

from jar_downloader.discovery import get_jar_downloaders
from jar_downloader.discovery import get_jar_downloader_map
from util.decorators import require_internal
from util.flask_helpers import render_template
from presentation.jar_downloader import JarDownloader

jar_creation = flask.Blueprint(
    'jar_creation', __name__, template_folder='templates'
)

def get_jar_downloader_presenters():
    return sorted(
        (
            JarDownloader(jar_downloader_cls)
            for jar_downloader_cls in get_jar_downloaders()
        ),
        lambda jar_downloader: jar_downloader.name
    )

def get_sorted_jar_names():
    return sorted(get_jar_downloader_map().keys())

@jar_creation.route('/available_jars')
@require_internal
def available_jars():
    jar_downloaders = get_jar_downloader_presenters()
    jar_downloader_names = [jar.name for jar in jar_downloaders]
    return simplejson.dumps(jar_downloader_names)

@jar_creation.route('/jar_list')
@require_internal
def jar_list():
    jar_downloaders = get_jar_downloader_presenters()
    return render_template('jar_list.htm', jar_downloaders=jar_downloaders)

@jar_creation.route('/new_jar/<jar_name>')
@require_internal
def new_jar(jar_name):
    return jar_name
