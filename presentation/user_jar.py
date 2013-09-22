
import collections
import flask

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

    @property
    def update_url(self):
        return flask.url_for(
            'jar.update',
            jar_type=self.jar_type,
            user_jar_name=self.name,
        )

    @property
    def download_url(self):
        return flask.url_for(
            'jar.download',
            jar_type=self.jar_type,
            user_jar_name=self.name,
        )

    def has_version(self, version):
        return any(
            jar.short_version == version
            for jar in self.downloaded_versions
        )

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
