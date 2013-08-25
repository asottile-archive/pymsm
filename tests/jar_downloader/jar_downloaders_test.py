
import testify as T

from jar_downloader.discovery import get_jar_downloaders
from schemaform.form import Form
from schemaform.helpers import validate_schema_against_draft4

class TestAllJarDownloadersHaveValidSchemas(T.TestCase):
    def test_all_have_valid_schemas(self):
        for jar_downloader_cls in get_jar_downloaders():
            validate_schema_against_draft4(
                jar_downloader_cls.get_config_schema()
            )

    def test_all_have_valid_object_schemas(self):
        for jar_downloader_cls in get_jar_downloaders():
            assert Form(jar_downloader_cls.get_config_schema()).__pq__()
