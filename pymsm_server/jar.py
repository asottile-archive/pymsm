
import flask
import simplejson

from jar_downloader.discovery import get_jar_downloader_map
from jar_downloader.discovery import get_user_jars
from util.decorators import require_internal
from util.flask_helpers import render_template
from presentation.user_jar import UserJar

jar = flask.Blueprint(
    'jar', __name__, template_folder='templates/jar'
)

@jar.route('/jar/<jar_type>/<user_jar_name>', methods=['GET'])
@require_internal
def jar_home(jar_type, user_jar_name):
    jar_cls = get_jar_downloader_map()[jar_type]
    jar_path = get_user_jars()[jar_type][user_jar_name]
    instance = jar_cls(jar_path)

    user_jar_presenter = UserJar.from_user_jar(
        instance,
        jar_type,
        user_jar_name,
    )

    return render_template('jar_home.htm', user_jar=user_jar_presenter)

@jar.route('/jar/<jar_type>/<user_jar_name>/update', methods=['POST'])
@require_internal
def jar_update(jar_type, user_jar_name):
    jar_cls = get_jar_downloader_map()[jar_type]
    jar_path = get_user_jars()[jar_type][user_jar_name]
    instance = jar_cls(jar_path)

    try:
        instance.update()
        return simplejson.dumps({'succes': True})
    except Exception:
        return simplejson.dumps({'success': False})

@jar.route('/jar/<jar_type>/<user_jar_name>/download', methods=['POST'])
@require_internal
def jar_download(jar_type, user_jar_name):
    pass
