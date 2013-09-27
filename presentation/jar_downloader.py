
import collections
import flask

class JarDownloader(collections.namedtuple(
    'JarDownloader',
    ['jar_downloader_cls'],
)):
    """A JarDownloader presenter represents a jar downloader."""
    __slots__ = ()

    @property
    def name(self):
        return self.jar_downloader_cls.__name__

    @property
    def url(self):
        return flask.url_for('jar_creation.new_jar', jar_type=self.name)
