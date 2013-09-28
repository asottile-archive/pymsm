
import testify as T

from presentation.jar_downloader import JarDownloader
from web.start import app

class TestJarDownloader(T.TestCase):

    def test_name(self):
        instance = JarDownloader(JarDownloader)
        T.assert_equal(instance.name, JarDownloader.__name__)

    def test_url(self):
        with app.test_request_context():
            instance = JarDownloader(JarDownloader)
            T.assert_equal(
                instance.url,
                '/new_jar/JarDownloader',
            )
