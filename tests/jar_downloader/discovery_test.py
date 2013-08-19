
import testify as T

from jar_downloader.discovery import get_jar_downloaders
from jar_downloader.discovery import get_module_name
from jar_downloader.discovery import is_jar_downloader
from jar_downloader.jar_downloader_base import JarDownloaderBase

class TestGetModuleName(T.TestCase):
    """Tests the get_module_name function."""

    def test_get_module_name(self):
        module_name = get_module_name('foo', 'bar.py')
        T.assert_equal(module_name, 'foo.bar')

    def test_raises_on_non_python_file(self):
        with T.assert_raises(ValueError):
            get_module_name('foo', 'bar')

    def test_more_complicated_directory(self):
        module_name = get_module_name('foo/bar', 'baz.py')
        T.assert_equal(module_name, 'foo.bar.baz')

    def test_strips_prefixing_dot_slash(self):
        module_name = get_module_name('./foo', 'bar.py')
        T.assert_equal(module_name, 'foo.bar')

class TestIsJarDownloader(T.TestCase):
    """Tests the is_jar_downloader method."""

    def test_jar_downloader_base_is_not_one(self):
        T.assert_equal(is_jar_downloader(JarDownloaderBase), False)

    def test_excluded_jar_downloader_is_not_one(self):
        class ImNotAJarDownloader(JarDownloaderBase):
            __jar_downloader__ = False

        T.assert_equal(is_jar_downloader(ImNotAJarDownloader), False)

    def test_some_randomass_class_is_not_a_jar_downloader(self):
        T.assert_equal(is_jar_downloader(object), False)

    def test_some_object_that_should_be_a_jar_downloader(self):
        class ImAJarDownloader(JarDownloaderBase): pass
        T.assert_equal(is_jar_downloader(ImAJarDownloader), True)

class TestGetJarDownloaders(T.TestCase):
    # XXX: this method is pretty nuts so this is more of a smoke test
    def test_get_jar_downloaders(self):
        assert get_jar_downloaders()
