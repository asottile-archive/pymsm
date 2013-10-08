
import os.path

from util.properties import Properties

SERVER_PROPERTIES_FILENAME = 'server.properties'

class UserServer(object):
    """Class repesenting a user's server.  A server has settings to configure
    a jar for which the minecraft server runs on.
    """

    def __init__(self, server_dir):
        assert os.path.exists(server_dir)
        self.server_dir = server_dir

    @property
    def server_properties_path(self):
        return os.path.join(self.server_dir, SERVER_PROPERTIES_FILENAME)

    @property
    def server_properties(self):
        with open(self.server_properties_path, 'r') as server_properties_file:
            return Properties.load(server_properties_file)
