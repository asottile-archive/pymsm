
import os
import os.path

from jar_downloader.jar_downloader_base import JarDownloaderBase
from util.discovery import discover

JAR_DOWNLOADER_DIRECTORY = os.path.dirname(__file__)

def is_jar_downloader(cls):
    return (
        cls is not JarDownloaderBase and
        issubclass(cls, JarDownloaderBase) and
        cls.__dict__.get('__jar_downloader__', True)
    )

def get_jar_downloaders():
    """Returns a list of classes that are JarDownloaders."""
    return discover(JAR_DOWNLOADER_DIRECTORY, is_jar_downloader)
