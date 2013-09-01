
import flask
import mock
import testify as T

from util.auto_namedtuple import auto_namedtuple
from util.flask_helpers import is_internal

class TestIsInternal(T.TestCase):
    """Tests the @require_internal decorator."""

    def _get_fake_request(self, remote_addr='127.0.0.1'):
        return auto_namedtuple('MockRequest', remote_addr=remote_addr)

    def test_is_internal_with_internal_ip(self):
        with mock.patch.object(flask, 'request', self._get_fake_request()):
            T.assert_equal(is_internal(), True)

    def test_is_internal_with_external_ip(self):
        with mock.patch.object(
            flask,
            'request',
            self._get_fake_request('192.168.0.1'),
        ):
            T.assert_equal(is_internal(), False)

if __name__ == '__main__':
    T.run()
