
import os.path
import simplejson

from jar_downloader.discovery import get_jar_downloaders

SERVER_PROPERTIES_FILENAME = 'server.properties'

CONFIG_FILENAME = 'config.json'

CONFIG_SCHEMA = {
    'type': 'object',
    'properties': {
        'jar': {
            'type': 'object',
            'properties': {
                'jar_type': {
                    'type': 'string',
                    # jar_type is a choice of the types of jars defined
                    # This can be statically defined here because the jar types
                    # don't change at runtime, however user_jar_name cannot
                    # be checked in this way and must need a runtime check
                    'enum': [
                       jar_downloader_cls.__name__
                       for jar_downloader_cls in get_jar_downloaders()
                    ],
                },
                'user_jar_name': {
                    'type': 'string',
                },
            },
            'required': ['jar_type', 'user_jar_name'],
        },
    },
    'required': ['jar'],
}

class UserServer(object):
    """Class repesenting a user's server.  A server has settings to configure
    a jar for which the minecraft server runs on.
    """

    def __init__(self, server_dir):
        assert os.path.exists(server_dir)
        self.server_dir = server_dir

    @property
    def config_path(self):
        return os.path.join(self.server_dir, CONFIG_FILENAME)

    @property
    def config(self):
        with open(self.config_path, 'r') as config_file:
            return simplejson.load(config_file)
