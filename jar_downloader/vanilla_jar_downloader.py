
import fnmatch
import re
import os
import os.path
import simplejson
import urllib2

from jar_downloader.jar_downloader_base import Jar
from jar_downloader.jar_downloader_base import JarDownloaderBase
from util.natural_sort import natural_sort

VERSIONS_ENDPOINT = 'https://s3.amazonaws.com/Minecraft.Download/versions/versions.json'
DOWNLOAD_PATH = 'https://s3.amazonaws.com/Minecraft.Download/versions/{version}/minecraft_server.{version}.jar'

VERSION_REGEX = re.compile('minecraft_server.(.+).jar')
JAR_MATCH = 'minecraft_server.*.jar'
JAR_FILENAME = 'minecraft_server.%s.jar'

LATEST_FILE = 'latest.txt'

RELEASE = 'release'
SNAPSHOT = 'snapshot'


class InvalidVersionFileError(ValueError): pass


def get_versions_json():
    """Returns the versions json for vanilla minecraft.

    Note: this is potentially slow and/or flaky because it hits an external
    endpoint
    """
    return simplejson.loads(
        # TODO: add a reasonable timeout here
        urllib2.urlopen(VERSIONS_ENDPOINT).read()
    )


class VanillaJarDownloader(JarDownloaderBase):
    """The vanilla jar downloader downloads the vanilla version of
    minecraft-server.jar
    """

    @property
    def _latest_filename(self):
        return os.path.join(self.jar_directory, LATEST_FILE)

    @classmethod
    def _to_jar(cls, filename):
        """Returns a Jar object from the filename."""
        return Jar(
            filename,
            VERSION_REGEX.match(filename).groups()[0],
        )

    @classmethod
    def get_config_schema(cls):
        """The config schema for vanilla jar downloader is whether or not they
        are on the release channel.
        """
        return {
            'type': 'object',
            'properties': {
                'jar_type': {
                    'title': 'Jar Type',
                    'enum': [RELEASE, SNAPSHOT],
                    'labels': [RELEASE.title(), SNAPSHOT.title()],
                    'default': RELEASE,
                },
            },
            'required': ['jar_type',],
        }

    @property
    def downloaded_versions(self):
        """Lists all of the files in the directory and returns Jar objects of
        them.
        """
        return [
            self._to_jar(filename)
            for filename in os.listdir(self.jar_directory)
            if fnmatch.fnmatch(filename, JAR_MATCH)
        ]

    def _try_to_get_latest_version(self):
        """Attempts to get the latest version from the LATEST_FILE.

        On failure raises InvalidVersionFileError.
        """
        if not os.path.exists(self._latest_filename):
            raise InvalidVersionFileError('No jars have been downloaded.')

        with open(self._latest_filename, 'r') as file:
            latest_jarfile = file.read().strip()

        if not os.path.exists(os.path.join(self.jar_directory, latest_jarfile)):
            raise InvalidVersionFileError('Latest jar does not exist.')

        return latest_jarfile

    @property
    def latest_downloaded_version(self):
        """Returns the latest version that is downloaded."""
        try:
            latest_jarfile = self._try_to_get_latest_version()
        except InvalidVersionFileError:
            # If we didn't get a valid version at least clean up the version
            # file
            if os.path.exists(self._latest_filename):
                os.remove(self._latest_filename)

            raise

        return self._to_jar(latest_jarfile)

    @property
    def available_versions(self):
        """Returns a list of all available downloadable versions.

        Note: this is potentially expensive and flaky because it hits an
        external endpoint.
        """
        versions_json = get_versions_json()

        version_dict_filter_types = set([RELEASE])
        if self.config['jar_type'] == SNAPSHOT:
            version_dict_filter_types.add(SNAPSHOT)

        return natural_sort([
            version_dict['id']
            for version_dict in versions_json['versions']
            if version_dict['type'] in version_dict_filter_types
        ])

    def download_specific_version(self, version):
        """Downloads a specific version of minecraft_server.jar

        Note: this function is probably slow because it downloads a jar
        """
        # TODO: maybe log a warning here if the file already exists
        # but for now just overwrite it if it exists.
        # This is probably a good approach as this method could be used for
        # "fixing" corrupted files if such a thing were to happen
        if not version in self.available_versions:
            raise AssertionError('Not a valid version number.')

        jar_filename = os.path.join(self.jar_directory, JAR_FILENAME % version)
        with open(jar_filename, 'wb') as jar_file:
            jar_file.write(
                urllib2.urlopen(
                    DOWNLOAD_PATH.format(version=version)
                ).read()
            )

    def _get_latest_version(self):
        versions_json = get_versions_json()
        return versions_json['latest'][self.config['jar_type']]

    def update(self):
        """Downloads the latest version if we haven't already downloaded it."""
        latest_version = self._get_latest_version()

        # Try and see what the current downloaded version is
        # This may fail, this is ok
        current_latest_version = None
        try:
           current_latest_version = self.latest_downloaded_version
        except InvalidVersionFileError: pass

        # If the latest version is in fact new download it and write to our
        # version file
        # Return the new version number to indicate it was updated
        if latest_version != current_latest_version:
            self.download_specific_version(latest_version)
            latest_jar_filename = JAR_FILENAME % latest_version
            with open(self._latest_filename, 'w') as latest_file:
                latest_file.write(latest_jar_filename)
            return self._to_jar(latest_jar_filename)

