
import testify as T

from testing.assertions.common import assert_issubclass

class TestIsSubclass(T.TestCase):

    class A(object): pass
    class B(A): pass
    class C(object): pass

    def test_issubclass_not_a_subclass(self):
        with T.assert_raises_such_that(
            AssertionError,
            lambda e:
                e.args == (
                    'Expected %s to be a subclass of %s' % (
                        self.C.__name__, self.A.__name__
                    ),
                )
        ):
            assert_issubclass(self.C, self.A)

    def test_issubclass_actually_a_subclass(self):
        assert_issubclass(self.B, self.A)

