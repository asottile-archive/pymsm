
from jar_downloader.jar_downloader_base import JarDownloaderBase
from jar_downloader.vanilla_jar_downloader import RELEASE
from jar_downloader.vanilla_jar_downloader import SNAPSHOT
from schemaform.helpers import validate_schema_against_draft4

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
            RELEASE: release_version,
            SNAPSHOT: snapshot_version,
        }
    }

def get_fake_jar_downloader_cls(name=NO_ARG, config_schema=NO_ARG):
    if name is NO_ARG:
        name = 'FakeJarDownloader'

    if config_schema is NO_ARG:
        config_schema = {
            'type': 'object',
            'properties': {
                'foo': {},
                'bar': {},
            },
            'propertyOrder': ['foo', 'bar'],
        }

    # Validate arguments
    assert name
    validate_schema_against_draft4(config_schema)

    fake_jar_downloader_cls = type(
        name,
        (JarDownloaderBase,),
        {
            'get_config_schema': classmethod(lambda cls: config_schema),
        },
    )

    return fake_jar_downloader_cls
