
import contextlib
import mock
import os.path
import shutil
import tempfile
import testify as T

import config.application
from pymsm_server.start import app
from testing.base_classes.flask_test_case import FlaskTestCase

@T.suite('integration')
class PymsmServerTestCase(FlaskTestCase):
    __test__ = False

    FLASK_APPLICATION = app

    @T.setup_teardown
    def create_mock_environment(self):
        self.app_root = tempfile.mkdtemp()
        self.data_path = os.path.join(self.app_root, 'data')
        self.jars_path = os.path.join(self.data_path, 'jars')
        try:
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
        finally:
            shutil.rmtree(self.app_root)
