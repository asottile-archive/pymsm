
import contextlib
import mock
import os.path
import testify as T

import config.application
from testing.base_classes.flask_test_case import FlaskTestCase
from testing.base_classes.tempdir_test_case import TempdirTestCase
from web.app import app

@T.suite('integration')
class PymsmServerTestCase(FlaskTestCase, TempdirTestCase):
    __test__ = False

    FLASK_APPLICATION = app

    @T.setup_teardown
    def create_mock_environment(self):
        self.app_root = self.tempdir
        self.data_path = os.path.join(self.app_root, 'data')
        self.jars_path = os.path.join(self.data_path, 'jars')
        with contextlib.nested(
            mock.patch.object(
                config.application, 'APP_ROOT', self.app_root,
            ),
            mock.patch.object(
                config.application, 'DATA_PATH', self.data_path,
            ),
            mock.patch.object(
                config.application, 'JARS_PATH', self.jars_path,
            ),
        ):
            yield
