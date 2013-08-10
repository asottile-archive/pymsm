
import contextlib
import mock
import simplejson
import testify as T
import urllib2

from pymsm_server.jar_downloader.vanilla_jar_downloader import get_versions_json
from pymsm_server.jar_downloader.vanilla_jar_downloader import VanillaJarDownloader
from pymsm_server.jar_downloader.vanilla_jar_downloader import VERSIONS_ENDPOINT

class TestGetVersionsJson(T.TestCase):
    """Tests the get_versions_json method."""

    def test_get_versions_json(self):
        with contextlib.nested(
            mock.patch.object(simplejson, 'loads', autospec=True),
            mock.patch.object(urllib2, 'urlopen', autospec=True),
        ) as (
            loads_mock,
            urlopen_mock,
        ):
            retval = get_versions_json()
            urlopen_mock.assert_called_once_with(VERSIONS_ENDPOINT)
            loads_mock.assert_called_once_with(
                urlopen_mock.return_value.read.return_value
            )
            T.assert_equal(retval, loads_mock.return_value)

class TestVanillaJarDownloader(T.TestCase):
    pass
