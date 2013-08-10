
import contextlib
import mock
import simplejson
import testify as T
import urllib2

from jar_downloader.vanilla_jar_downloader import get_versions_json
from jar_downloader.vanilla_jar_downloader import VanillaJarDownloader
from jar_downloader.vanilla_jar_downloader import VERSIONS_ENDPOINT

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

    @T.suite('integration')
    @T.suite('external')
    def test_structure_of_external_json(self):
        json_object = get_versions_json()

        T.assert_equal(
            json_object,
            {
                'versions': mock.ANY, # Tested more explicitly below
                'latest': {
                    'release': mock.ANY,
                    'snapshot': mock.ANY,
                }
            }
        )

        # Versions should be a list of dict objects
        T.assert_isinstance(json_object['versions'], list)
        for version_dict in json_object['versions']:
            T.assert_equal(
                version_dict,
                {
                    'releaseTime': mock.ANY,
                    'type': mock.ANY,
                    'id': mock.ANY,
                    'time': mock.ANY,
                }
            )

class TestVanillaJarDownloader(T.TestCase):
    pass
