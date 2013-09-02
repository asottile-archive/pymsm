import testify as T

from jar_downloader.jar_downloader_base import JarDownloaderBase
from jar_downloader.vanilla_jar_downloader import RELEASE
from jar_downloader.vanilla_jar_downloader import SNAPSHOT
from schemaform.helpers import validate_schema_against_draft4
from testing.assertions.version_json import assert_json_structure
from testing.assertions.common import assert_issubclass
from testing.data.generators import get_fake_versions_json
from testing.data.generators import get_fake_jar_downloader_cls

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

class TestGetFakeJarDownloaderCls(T.TestCase):
    def test_default_is_instance_of_JarDownloader(self):
        ret_cls = get_fake_jar_downloader_cls()
        assert_issubclass(ret_cls, JarDownloaderBase)

    def test_default_config_schema_is_valid(self):
        ret_cls = get_fake_jar_downloader_cls()
        validate_schema_against_draft4(ret_cls.get_config_schema())

    def test_default_name_is_valid(self):
        ret_cls = get_fake_jar_downloader_cls()
        assert ret_cls.__name__
