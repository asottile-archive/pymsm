
import fnmatch
import re
import os
import os.path
import simplejson
import urllib2

from pymsm_server.jar_downloader.jar_downloader_base import Jar
from pymsm_server.jar_downloader.jar_downloader_base import JarDownloaderBase

VERSIONS_ENDPOINT = 'https://s3.amazonaws.com/Minecraft.Download/versions/versions.json'
DOWNLOAD_PATH = 'https://s3.amazonaws.com/Minecraft.Download/versions/{version}/minecraft_server.{version}.jar'

VERSION_REGEX = re.compile('minecraft_server.(.+).jar')
JAR_MATCH = 'minecraft_server.*.jar'

LATEST_FILE = 'latest.txt'


class InvalidVersionFileError(ValueError): pass


def get_versions_json():
    """Returns the versions json for vanilla minecraft."""
    return simplejson.loads(
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

    def _try_to_get_latest_version_file(self):
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
            latest_jarfile = self._try_to_get_latest_version_file()
        except InvalidVersionFileError:
            # If we didn't get a valid version at least clean up the version
            # file
            if os.path.exists(self._latest_filename):
                os.remove(self._latest_filename)

            raise

        return self._to_har(latest_jarfile)