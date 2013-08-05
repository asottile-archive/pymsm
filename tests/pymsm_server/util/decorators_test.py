
import collections
import contextlib
import flask
import mock
import testify as T
import werkzeug.exceptions


from pymsm_server.util.decorators import require_internal

class TestRequireInternal(T.TestCase):
    """Tests the @require_internal decorator."""

    def _get_fake_request(self, remote_addr='127.0.0.1'):
        return (
            collections.namedtuple(
                'MockRequest', ['remote_addr'],
            )(remote_addr)
        )

    def _get_callable_mock(self):
        mock_callable = mock.Mock()
        mock_callable.__name__ = 'foo'
        return mock_callable

    def test_ok_with_internal_ip(self):
        """Tests that the method is called as usual with localhost."""
        mock_request = self._get_fake_request()
        arg = object()
        callable = self._get_callable_mock()

        with mock.patch.object(flask, 'request', mock_request):
            require_internal(callable)(arg)

        callable.assert_called_once_with(arg)

    def test_not_ok_with_external_ip(self):
        """Tests that we get an exception without localhost."""
        mock_request = self._get_fake_request('192.168.0.1')
        callable = self._get_callable_mock()

        with contextlib.nested(
            mock.patch.object(flask, 'request', mock_request),
            T.assert_raises(werkzeug.exceptions.Forbidden),
        ):
            require_internal(callable)()

if __name__ == '__main__':
    T.run()
