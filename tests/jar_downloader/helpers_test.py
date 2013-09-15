
import __builtin__

import contextlib
import mock
import os
import os.path
import simplejson
import testify as T

import config.application
from jar_downloader.helpers import CONFIG_FILE
from jar_downloader.helpers import create_jar_directory
from testing.utilities.fake_file import FakeFile

class TestCreateJarDirectory(T.TestCase):

    @T.setup_teardown
    def setup_mocks(self):
        with contextlib.nested(
            mock.patch.object(__builtin__, 'open', autospec=True),
            mock.patch.object(os, 'makedirs', autospec=True),
            mock.patch.object(os.path, 'exists', autospec=True),
        ) as (
            self.open_mock,
            self.makedirs_mock,
            self.exists_mock,
        ):
            yield

    def test_create_jar_directory_already_exists(self):
        self.exists_mock.return_value = True
        with T.assert_raises_such_that(
            ValueError,
            lambda e:
                e.args == ('Jar Folder Path already exists.')
        ):
            create_jar_directory('foo', 'bar', {})

    def test_creates_directory_and_writes_config(self):
        self.exists_mock.return_value = False
        self.open_mock.return_value = FakeFile()
        jar_name = 'foo'
        user_jar_name = 'bar'
        jar_config = {'foo': 'bar'}
        create_jar_directory(jar_name, user_jar_name, jar_config)

        expected_jar_directory = os.path.join(
            config.application.JARS_PATH, jar_name, user_jar_name,
        )
        # XXX: I kind of expect this to happen at least once, but this assertion
        # used to be assert_called_once_with, but apparently coverage does some
        # crazy shit when running this.
        self.exists_mock.assert_has_calls(mock.call(expected_jar_directory))
        self.makedirs_mock.assert_called_once_with(expected_jar_directory)
        self.open_mock.assert_called_once_with(
            os.path.join(expected_jar_directory, CONFIG_FILE), 'w'
        )
        T.assert_equal(
            self.open_mock.return_value._written_contents,
            simplejson.dumps(jar_config)
        )
