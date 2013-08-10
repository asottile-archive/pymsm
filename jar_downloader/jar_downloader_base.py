
import collections

class Jar(collections.namedtuple('Jar', ['filename', 'short_version'])):
    """A Jar represents a single file of a jar inside the jar_directory.

    Properties:
        filename - The filename of the jar inside the jar_directory
        short_version - Version that the jar downloader uses to identify the
            jar.
    """
    pass

class JarDownloaderBase(object):
    """Base class for Jar Downloaders.  A Jar Downloader is responsible for
    managing a directory of downloaded jars and for updating to the latest
    version.
    """

    def __init__(self, jar_directory):
        """Initialize the Jar Downloader.

        Args:
            jar_directory - Directory where the jars will be downloaded to and
                managed.
        """
        self.jar_directory = jar_directory

    @property
    def downloaded_versions(self):
        """Implement to return an iterable of Jar objects representing the
        downloaded jars for this JarDownloader.
        """
        raise NotImplementedError

    @property
    def latest_downloaded_version(self):
        """Implement to return a Jar object of the latest downloaded version."""
        raise NotImplementedError

    @property
    def available_versions(self):
        """Return a list of all available downloadable versions."""
        raise NotImplementedError

    def download_specific_version(self, version):
        """Downloads the specified version.

        Args:
            version - short version string.
        """
        raise NotImplementedError

    def update(self):
        """Retrieves the latest jar version and returns a Jar object of it.

        Note: this may not actually download any new jars.
        """
        raise NotImplementedError
