
import testify as T

from util.auto_namedtuple import auto_namedtuple

class TestAutoNamedtuple(T.TestCase):

    kwargs = {
        'foo': 'bar',
        'baz': 'asdf',
    }

    def test_classname_set(self):
        classname = 'herp'
        retval = auto_namedtuple(classname, **self.kwargs)
        T.assert_equal(type(retval).__name__, classname)

    def test_no_classname(self):
        retval = auto_namedtuple(**self.kwargs)
        T.assert_equal(type(retval).__name__, 'auto_namedtuple')

    def test_values(self):
        retval = auto_namedtuple(**self.kwargs)
        for key, value in self.kwargs.iteritems():
            T.assert_is(getattr(retval, key), value)
