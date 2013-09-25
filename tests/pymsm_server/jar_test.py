
import flask
import shutil
import testify as T

from jar_downloader.helpers import create_jar_directory
from jar_downloader.helpers import get_jar_directory
from jar_downloader.vanilla_jar_downloader import VanillaJarDownloader
from schemaform.form import Form
from testing.assertions.response import assert_no_response_errors
from testing.base_classes.pymsm_server_test_case import PymsmServerTestCase

class TestJar(PymsmServerTestCase):

    jar_type = VanillaJarDownloader.__name__
    user_jar_name = 'ReleaseJar'
    config = {'jar_type': 'release'}

    @T.setup_teardown
    def set_up_user_jar(self):
        create_jar_directory(self.jar_type, self.user_jar_name, self.config)
        try:
            yield
        finally:
            shutil.rmtree(get_jar_directory(self.jar_type, self.user_jar_name))

    @T.setup_teardown
    def become_internal(self):
        with self.client.patch_ip('127.0.0.1'):
            yield

    def test_data_is_sane(self):
        form = Form(VanillaJarDownloader.get_config_schema())
        values, errors = form.load_from_form(self.config)
        T.assert_equal(errors, {})

    def test_jar_home(self):
        resp = self.client.get(flask.url_for(
            'jar.jar_home',
            jar_type=self.jar_type,
            user_jar_name=self.user_jar_name,
        ))
        assert_no_response_errors(resp)
