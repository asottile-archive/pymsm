
import mock
import os.path
import testify as T

from jar_downloader.jar_downloader_base import JarDownloaderBase

class TestJarDownloaderBaseConstructor(T.TestCase):
    """Tests the JarDownloaderBase."""

    directory = str(object())

    @T.setup_teardown
    def setup_mocks(self):
        with mock.patch.object(os.path, 'exists', autospec=True) as self.exists_mock:
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
