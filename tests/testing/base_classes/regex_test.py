
import re
import testify as T

from testing.base_classes.regex import BooleanSearchReTestBase
from testing.base_classes.regex import ReplaceReTestBase

class TestBooleanSearchReTestBase(T.TestCase):

    def test_passing(self):

        class PassingClass(BooleanSearchReTestBase):
            regex = re.compile('[A-Za-z]')
            expected = (
                ('A', True),
                ('0', False),
            )

        PassingClass().test_regex()

    def test_failing(self):

        class FailingClass(BooleanSearchReTestBase):
            regex = re.compile('[a-z]')
            expected = (
                ('A', True),
            )

        with T.assert_raises(AssertionError):
            FailingClass().test_regex()

class TestReplaceReTestBase(T.TestCase):

    def test_passing(self):

        class PassingClass(ReplaceReTestBase):
            regex = re.compile('f')
            replacement = 'b'
            expected = (
                ('foo', 'boo'),
                ('abcdef', 'abcdeb'),
                ('bar', 'bar'),
            )

        PassingClass().test_regex()

    def test_failing(self):

        class FailingClass(ReplaceReTestBase):
            regex = re.compile('[A-Z]')
            replacement = 'q'
            expected = (
                ('foo', 'qoo'),
            )

        with T.assert_raises(AssertionError):
            FailingClass().test_regex()
