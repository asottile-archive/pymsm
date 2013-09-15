
import collections
import os
import os.path

import config.application
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

def get_jar_downloader_map():
    """Returns a dict that maps name to jar downloader class."""
    return dict((jar.__name__, jar) for jar in get_jar_downloaders())

def get_user_jars():
    """Returns a map mapping as follows: {
        'JarType': {
            'UserJarName': 'path/to/jar/directory',
        }
    }
    """
    ret = collections.defaultdict(dict)

    # Jars are stored in data/jars/[JarType]/[UserJarName]
    jar_type_directories = os.listdir(config.application.JARS_PATH)
    for jar_type in jar_type_directories:
        jar_type_dir = os.path.join(config.application.JARS_PATH, jar_type)
        user_jar_names = os.listdir(jar_type_dir)
        for user_jar_name in user_jar_names:
            ret[jar_type][user_jar_name] = os.path.join(
                jar_type_dir,
                user_jar_name,
            )

    return ret
