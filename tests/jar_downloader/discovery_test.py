
import mock
import testify as T

import jar_downloader.discovery
from jar_downloader.discovery import get_jar_downloaders
from jar_downloader.discovery import get_jar_downloader_map
from jar_downloader.discovery import is_jar_downloader
from jar_downloader.jar_downloader_base import JarDownloaderBase

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

    def test_child_of_excluded_is_one(self):
        class ImNotAJarDownloader(JarDownloaderBase):
            __jar_downloader__ = False

        class ButIAm(ImNotAJarDownloader): pass

        T.assert_equal(is_jar_downloader(ButIAm), True)

class TestGetJarDownloaders(T.TestCase):
    # XXX: this method is pretty nuts so this is more of a smoke test
    def test_get_jar_downloaders(self):
        assert get_jar_downloaders()


class TestGetJarDownloaderMap(T.TestCase):
    def test_get_jar_downloader_map(self):
        class Foo: pass
        class Bar: pass

        with mock.patch.object(
            jar_downloader.discovery,
            'get_jar_downloaders',
            autospec=True,
        ) as get_jar_downloaders_mock:
            get_jar_downloaders_mock.return_value = set([Foo, Bar])
            ret = get_jar_downloader_map()
            T.assert_equal(ret, {'Foo': Foo, 'Bar': Bar})
