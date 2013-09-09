
import os
import os.path
import simplejson

import config.application

CONFIG_FILE = 'config.json'

def create_jar_directory(jar_name, user_jar_name, jar_config):
    """Sets up the jar directory for a jar.

    A jar is stored in JARS_DIRECTORY/JarClsName/UserJarName/

    Args:
        jar_name - The type of jar to create
        user_jar_name - Name given by the user for the jar (to allow multiple
            jars to be created with the same class name)
        jar_config - Configuration of the jar
    """
    jar_folder_path = os.path.join(
        config.application.JARS_DIRECTORY,
        jar_name,
        user_jar_name,
    )

    # Make sure that the jar directory doesn't already exist
    if os.path.exists(jar_folder_path):
        raise ValueError('Jar Folder Path already exists.')

    os.makedirs(jar_folder_path)
    config_file_path = os.path.join(jar_folder_path, CONFIG_FILE)

    with open(config_file_path, 'w') as config_file:
        simplejson.dump(jar_config, config_file)
