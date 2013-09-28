
import flask
import simplejson

from jar_downloader.discovery import get_jar_downloader_map
from jar_downloader.discovery import get_user_jars
from util.decorators import require_internal
from util.flask_helpers import render_template
from presentation.user_jar import UserJar

jar = flask.Blueprint(
    'jar', __name__, template_folder='../templates/jar'
)

def get_jar_instance(jar_type, user_jar_name):
    jar_cls = get_jar_downloader_map()[jar_type]
    jar_path = get_user_jars()[jar_type][user_jar_name]
    return jar_cls(jar_path)

@jar.route('/jar/<jar_type>/<user_jar_name>', methods=['GET'])
@require_internal
def jar_home(jar_type, user_jar_name):
    instance = get_jar_instance(jar_type, user_jar_name)

    user_jar_presenter = UserJar.from_user_jar(
        instance,
        jar_type,
        user_jar_name,
    )

    return render_template('home.htm', user_jar=user_jar_presenter)

@jar.route('/jar/<jar_type>/<user_jar_name>/update', methods=['POST'])
@require_internal
def update(jar_type, user_jar_name):
    instance = get_jar_instance(jar_type, user_jar_name)

    instance.update()
    return simplejson.dumps({'success': True})

@jar.route('/jar/<jar_type>/<user_jar_name>/download', methods=['POST'])
@require_internal
def download(jar_type, user_jar_name):
    version = flask.request.form['version']

    instance = get_jar_instance(jar_type, user_jar_name)
    instance.download_specific_version(version)
    return simplejson.dumps({'success': True})
