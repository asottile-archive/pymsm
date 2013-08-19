import mock
import testify as T

from jar_downloader.vanilla_jar_downloader import RELEASE
from jar_downloader.vanilla_jar_downloader import SNAPSHOT

def assert_json_structure(json_object):
    T.assert_equal(
        json_object,
        {
            'versions': mock.ANY, # Tested more explicitly below
            'latest': {
                RELEASE: mock.ANY,
                SNAPSHOT: mock.ANY,
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

