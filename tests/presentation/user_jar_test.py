
import mock
import testify as T

from jar_downloader.jar_downloader_base import Jar
from presentation.user_jar import UserJar
from web.app import app

class TestUserJar(T.TestCase):

    def _get_instance(self):
        return UserJar(
            'jar_type',
            'name',
            '/jar/directory',
            ['foo', 'bar'],
            [Jar('foo.jar', 'foo'),],
            [Jar('foo.jar', 'foo'),],
        )

    def test_update_url(self):
        with app.test_request_context():
            instance = self._get_instance()
            T.assert_equal(
                instance.update_url,
                '/jar/jar_type/name/update',
            )

    def test_download_url(self):
        with app.test_request_context():
            instance = self._get_instance()
            T.assert_equal(
                instance.download_url,
                '/jar/jar_type/name/download',
            )

    def test_has_version(self):
        instance = self._get_instance()
        T.assert_equal(instance.has_version('foo'), True)
        T.assert_equal(instance.has_version('bar'), False)

    def test_from_user_jar_latest_version_excepts(self):
        # No latest downloaded version
        fake_user_jar = mock.Mock()
        type(fake_user_jar).latest_downloaded_version = mock.PropertyMock(
            side_effect=Exception,
        )
        instance = UserJar.from_user_jar(fake_user_jar, 'jar_type', 'name')
        T.assert_equal(
            instance.latest_downloaded_version,
            'No Jars Downloaded!',
        )

