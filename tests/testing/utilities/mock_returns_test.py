
import testify as T

from testing.utilities.mock_returns import MockReturns

class TestMockReturnsAppender(T.TestCase):

    class FakeMock(object):
        def __init__(self, value):
            self._return_values = [value]

    def test_then_appends(self):
        fake_mock = self.FakeMock('foo')
        mock_returns_appender = MockReturns._Appender(fake_mock)
        mock_returns_appender.then('bar')
        T.assert_equal(fake_mock._return_values, ['foo', 'bar'])

    def test_then_chains(self):
        fake_mock = self.FakeMock('foo')
        mock_returns_appender = MockReturns._Appender(fake_mock)
        mock_returns_appender.then('bar').then('baz')
        T.assert_equal(fake_mock._return_values, ['foo', 'bar', 'baz'])

class TestMockReturns(T.TestCase):

    def test_can_pass_return_values_in_constructor(self):
        mock = MockReturns(return_values=['foo', 'bar'])
        T.assert_equal(mock(), 'foo')
        T.assert_equal(mock(), 'bar')

    def test_return_value_returns_NotImplementedError(self):
        mock = MockReturns()
        ret = mock.return_value
        T.assert_equal(ret.args, ('Use return_values instead',))

    def test_chaining_thens(self):
        mock = MockReturns()
        mock.returns('foo').then('bar').then('baz')
        T.assert_equal(mock(), 'foo')
        T.assert_equal(mock(), 'bar')
        T.assert_equal(mock(), 'baz')

    def test_error_when_return_values_exhausted(self):
        mock = MockReturns()
        mock.returns('foo').then('bar').then('baz')
        mock()
        mock()
        mock()
        with T.assert_raises(IndexError):
            mock()
