import mock
import testify as T

def assert_json_structure(json_object):
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

