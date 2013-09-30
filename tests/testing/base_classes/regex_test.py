
import re
import testify as T

from testing.base_classes.regex import BooleanMatchReTestBase

class TestBooleanMatchReTestBase(T.TestCase):

    def test_passing(self):

        class PassingClass(BooleanMatchReTestBase):
            regex = re.compile('[A-Za-z]')
            expected = (
                ('A', True),
                ('0', False),
            )

        PassingClass().test_regex()

    def test_failing(self):

        class FailingClass(BooleanMatchReTestBase):
            regex = re.compile('[a-z]')
            expected = (
                ('A', True),
            )

        with T.assert_raises(AssertionError):
            FailingClass().test_regex()

