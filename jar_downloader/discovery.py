
import fnmatch
import inspect
import os
import os.path
import sys

from jar_downloader.jar_downloader_base import JarDownloaderBase

JAR_DOWNLOADER_DIRECTORY = os.path.dirname(__file__)

def get_module_name(root, filename):
    if not filename.endswith('.py'):
        raise ValueError('filename must end with .py')

    if root.startswith('./'):
        root = root[2:]

    filename = filename[:-3]
    # XXX: should really use pathsep here
    return os.path.join(root, filename).replace('/', '.')

def is_jar_downloader(cls):
    return (
        cls is not JarDownloaderBase and
        issubclass(cls, JarDownloaderBase) and
        getattr(cls, '__jar_downloader__', True)
    )

def get_jar_downloaders():
    """Returns a list of classes that are JarDownloaders."""

    jar_downloaders = set()

    # Look for all python files in the jar downloader directory
    for root, _, filenames in os.walk(JAR_DOWNLOADER_DIRECTORY):
        for filename in filenames:
            if fnmatch.fnmatch(filename, '*.py'):
                module_name = get_module_name(root, filename)
                # Import the module
                __import__(module_name)
                module = sys.modules[module_name]

                # Check all the classes in that module
                for name, _ in inspect.getmembers(module, inspect.isclass):
                    imported_class = getattr(module, name)

                    if is_jar_downloader(imported_class):
                        jar_downloaders.add(imported_class)

    return jar_downloaders
