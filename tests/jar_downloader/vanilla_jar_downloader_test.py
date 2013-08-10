
import contextlib
import mock
import os.path
import simplejson
import testify as T
import urllib2

import jar_downloader.vanilla_jar_downloader
from jar_downloader.vanilla_jar_downloader import get_versions_json
from jar_downloader.vanilla_jar_downloader import LATEST_FILE
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
        """A smoke test of the json data returned from the version service."""
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
    """Tests the vanilla jar downloader."""

    @T.setup_teardown
    def patch_out_base_init_verifying_directory(self):
        def fake_init(fakeself, jar_directory):
            """A fake init method to bypass os.path.exists check."""
            fakeself.jar_directory = jar_directory

        with mock.patch.object(
            jar_downloader.vanilla_jar_downloader.JarDownloaderBase,
            '__init__',
            fake_init,
        ):
            yield

    def test_latest_filename(self):
        path = str(object())
        T.assert_equal(
            VanillaJarDownloader(path)._latest_filename,
            os.path.join(path, LATEST_FILE)
        )
