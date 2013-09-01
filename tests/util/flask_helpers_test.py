
import contextlib
import flask
import mock
import testify as T

from util.auto_namedtuple import auto_namedtuple
import util.flask_helpers
from util.flask_helpers import is_internal
from util.flask_helpers import render_template

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


class TestRenderTemplate(T.TestCase):

    @T.setup_teardown
    def setup_mocks(self):
        with contextlib.nested(
            mock.patch.object(util.flask_helpers, 'is_internal', autospec=True),
            mock.patch.object(flask, 'render_template', autospec=True),
        ) as (
            self.is_internal_mock,
            self.render_template_mock,
        ):
            yield

    def test_render_template(self):
        template = object()
        kwargs = {
            'foo': 'bar',
            'baz': 'womp',
        }
        ret = render_template(template, **kwargs)

        T.assert_equal(ret, self.render_template_mock.return_value)
        self.is_internal_mock.assert_called_once_with()
        self.render_template_mock.assert_called_once_with(
            template,
            is_internal=self.is_internal_mock.return_value,
            **kwargs
        )

if __name__ == '__main__':
    T.run()
