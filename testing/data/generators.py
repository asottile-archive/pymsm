
NO_ARG = object()

def get_fake_versions_json(
    versions=NO_ARG,
    release_version=NO_ARG,
    snapshot_version=NO_ARG,
):
    """Gets fake data for versions.

    Args:
        versions - list of strings for versions,
        release_version - version to set as the release version
        snapshot_version - version to set as the snapshot version
    """

    if versions is NO_ARG:
        versions = [str(object()), str(object()), str(object())]

    if release_version is NO_ARG:
        release_version = versions[0]

    if snapshot_version is NO_ARG:
        snapshot_version = versions[1]

    assert versions
    assert release_version in versions
    assert snapshot_version in versions

    return {
        'versions': [
            {
                'id': version,
                'time': '2013-08-06T14:00:00+02:00',
                'releaseTime': '2013-08-06T15:00:00+02:00',
                'type': 'release',
            }
            for version in versions
        ],
        'latest': {
            'release': release_version,
             'snapshot': snapshot_version,
        }
    }
