
import shutil
import tempfile
import testify as T

class TempdirTestCase(T.TestCase):
    """TempdirTestCase provides a temporary directory that is cleaned up
    automagically.
    """

    @T.setup_teardown
    def create_temp_dir(self):
        self.tempdir = tempfile.mkdtemp()
        try:
            yield
        finally:
            shutil.rmtree(self.tempdir)
