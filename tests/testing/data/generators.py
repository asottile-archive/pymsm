import testify as T

from jar_downloader.vanilla_jar_downloader import RELEASE
from jar_downloader.vanilla_jar_downloader import SNAPSHOT
from testing.assertions.version_json import assert_json_structure
from testing.data.generators import get_fake_versions_json

class TestGetFakeVersionsJson(T.TestCase):
    """Tests the get_fake_versions_json function."""
    def test_get_fake_versions_json(self):
        json_object = get_fake_versions_json()
        assert_json_structure(json_object)

    def test_has_some_release_and_some_snapshot(self):
        json_object = get_fake_versions_json()
        types_of_version_dicts = set([
            version_dict['type']
            for version_dict in json_object['versions']
        ])
        T.assert_in(RELEASE, types_of_version_dicts)
        T.assert_in(SNAPSHOT, types_of_version_dicts)
