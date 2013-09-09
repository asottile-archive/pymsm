
import os.path

# This assumes this file is sitting at config/application.py
APP_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '../'
    )
)

DATA_PATH = os.path.join(APP_ROOT, 'data')
JARS_DIRECTORY = os.path.join(DATA_PATH, 'jars')
