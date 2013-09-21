
import __builtin__

import contextlib
import jsonschema
import mock
import os.path
import simplejson
import testify as T

from jar_downloader.jar_downloader_base import CONFIG_FILE
from jar_downloader.jar_downloader_base import JarDownloaderBase

class TestJarDownloaderBaseConstructor(T.TestCase):
    """Tests the JarDownloaderBase."""

    directory = str(object())

    @T.setup_teardown
    def setup_mocks(self):
        with mock.patch.object(
            os.path, 'exists', autospec=True,
        ) as self.exists_mock:
            yield

    def test_constructor_raises_when_directory_does_not_exist(self):
        with T.assert_raises(AssertionError):
            self.exists_mock.return_value = False
            JarDownloaderBase(self.directory)
            self.exists_mock.assert_called_once_with(self.directory)

    def test_constructor_is_chill_with_existing_directory(self):
        jar_downloader = JarDownloaderBase(self.directory)
        self.exists_mock.assert_called_once_with(self.directory)
        T.assert_equal(jar_downloader.jar_directory, self.directory)

    def test_config(self):
        with contextlib.nested(
            mock.patch.object(__builtin__, 'open', autospec=True),
            mock.patch.object(simplejson, 'load', autospec=True),
            mock.patch.object(jsonschema, 'validate', autospec=True),
        ) as (
            open_mock,
            load_mock,
            validate_mock,
        ):
            jar_downloader = JarDownloaderBase(self.directory)
            T.assert_equal(jar_downloader.config, load_mock.return_value)
            open_mock.assert_called_once_with(
                os.path.join(jar_downloader.jar_directory, CONFIG_FILE),
                'r',
            )
            load_mock.assert_called_once_with(
                open_mock.return_value.__enter__.return_value
            )
            validate_mock.assert_called_once_with(
                load_mock.return_value, {'type': 'object'}
            )
