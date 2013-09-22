
import collections

class UserJar(collections.namedtuple(
    'UserJar',
    [
        'jar_type',
        'name',
        'jar_directory',
        'available_versions',
        'downloaded_versions',
        'latest_downloaded_version',
    ],
)):
    __slots__ = ()

    @classmethod
    def from_user_jar(cls, instance, jar_type, name):
        # If there is no downloaded version we raise here
        try:
            latest_downloaded_version = instance.latest_downloaded_version
        # TODO: this is not a very specific exception type
        except Exception:
            latest_downloaded_version = 'No Jars Downloaded!'

        return cls(
            jar_type,
            name,
            instance.jar_directory,
            instance.available_versions,
            instance.downloaded_versions,
            latest_downloaded_version,
        )
