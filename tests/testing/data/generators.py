import testify as T

from testing.assertions.version_json import assert_json_structure
from testing.data.generators import get_fake_versions_json

class TestGetFakeVersionsJson(T.TestCase):
    """Tests the get_fake_versions_json function."""
    def test_get_fake_versions_json(self):
        json_object = get_fake_versions_json()
        assert_json_structure(json_object)
