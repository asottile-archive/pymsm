
from jar_downloader.vanilla_jar_downloader import RELEASE
from jar_downloader.vanilla_jar_downloader import SNAPSHOT

NO_ARG = object()

REASONABLE_VERSIONS = {
    '1.6.2': RELEASE,
    '1.5': RELEASE,
    '1.0': RELEASE,
    '13w19a': SNAPSHOT,
    '13w17a': SNAPSHOT,
    '13w16b': SNAPSHOT,
}

def get_fake_versions_json(
    versions_to_types=NO_ARG,
    release_version=NO_ARG,
    snapshot_version=NO_ARG,
):
    """Gets fake data for versions.

    Args:
        versions - list of strings for versions,
        release_version - version to set as the release version
        snapshot_version - version to set as the snapshot version
    """
    if versions_to_types is NO_ARG:
        versions_to_types = REASONABLE_VERSIONS

    if release_version is NO_ARG:
        release_version = versions_to_types.keys()[0]
    else:
       versions_to_types[release_version] = RELEASE

    if snapshot_version is NO_ARG:
        snapshot_version = versions_to_types.keys()[1]
    else:
        versions_to_types[snapshot_version] = SNAPSHOT

    assert versions_to_types
    assert release_version in versions_to_types
    assert versions_to_types[release_version] == RELEASE
    assert snapshot_version in versions_to_types
    assert versions_to_types[snapshot_version] in set([RELEASE, SNAPSHOT])

    return {
        'versions': [
            {
                'id': version,
                'time': '2013-08-06T14:00:00+02:00',
                'releaseTime': '2013-08-06T15:00:00+02:00',
                'type': release_type,
            }
            for version, release_type in versions_to_types.iteritems()
        ],
        'latest': {
            'release': release_version,
             'snapshot': snapshot_version,
        }
    }
