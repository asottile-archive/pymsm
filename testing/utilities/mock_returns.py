
import mock


class MockReturns(mock.Mock):
    """A mock helper class that allows you to chain the return values.

    Basic Usage:
        >> my_mock = MockReturns()
        >> my_mock.returns('foo').then('bar').then('baz')
        >> my_mock()
        'foo'
        >> my_mock()
        'bar'
        >> my_mock()
        'baz'
    """

    class _Appender(object):
        """Appender helper class so that someone can make a call like:
        foo = MockReturns()
        foo.returns('foo').then('bar').then('baz')
        This class handles the '.then' part.
        """
        def __init__(self, mock):
            self._mock = mock

        def then(self, value):
            self._mock._return_values.append(value)
            return self

    def __init__(self, *args, **kwargs):
        return_values = kwargs.pop('return_values', [])
        super(MockReturns, self).__init__(*args, **kwargs)
        self._return_values = list(return_values)

    def returns(self, value):
        """Sets the return values of the MockReturns object."""
        self._return_values = [value]
        return self._Appender(self)

    @property
    def return_value(self):
        # Note: not raising becaues base class calls this
        return NotImplementedError('Use return_values instead')

    @property
    def return_values(self):
        return tuple(self._return_values)

    def __call__(self, *args, **kwargs):
        return_value = self._return_values[self.call_count]
        super(MockReturns, self).__call__(*args, **kwargs)
        return return_value
