
import contextlib
import flask
import mock
import testify as T
import time
import werkzeug.exceptions

from util.auto_namedtuple import auto_namedtuple
from util.decorators import cached_property
from util.decorators import require_internal

class TestRequireInternal(T.TestCase):
    """Tests the @require_internal decorator."""

    def _get_fake_request(self, remote_addr='127.0.0.1'):
        return auto_namedtuple('MockRequest', remote_addr=remote_addr)

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

    def test_non_decorator_with_internal_ip(self):
        """Tests that the non-decorator version of this call allows localhost.
        """
        mock_request = self._get_fake_request()
        with mock.patch.object(flask, 'request', mock_request):
            require_internal()

    def test_non_decorator_with_external_ip(self):
       mock_request = self._get_fake_request('192.168.0.1')
       with contextlib.nested(
           mock.patch.object(flask, 'request', mock_request),
           T.assert_raises(werkzeug.exceptions.Forbidden),
       ):
           require_internal()


class TestCachedProperty(T.TestCase):

    class Foo(object):
        @cached_property
        def foo(self):
            return "Foo" + str(time.time())

    def test_cached_property(self):
        instance = self.Foo()
        val = instance.foo
        val2 = instance.foo
        T.assert_is(val, val2)


if __name__ == '__main__':
    T.run()
