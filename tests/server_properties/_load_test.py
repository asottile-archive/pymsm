
import testify as T

import server_properties._load
from server_properties.exceptions import InvalidPropertiesFileError
from testing.base_classes.regex import BooleanMatchReTestBase

class TestCommentRe(BooleanMatchReTestBase):

    regex = server_properties._load.COMMENT_RE

    expected = (
        ('!this is a comment', True),
        ('# this is a comment', True),
        (' ! this is a comment', True),
        (' # this is a comment', True),
        ('foo=bar#this is not a comment', False),
        ('foo=bar!this is not a comment', False),
    )

class TestLineContinuationRe(BooleanMatchReTestBase):

    regex = server_properties._load.LINE_CONTINUATION_RE

    backslash = '\\'

    expected = (
        ('', False),
        ('foo', False),
        ('foo' + backslash * 1, True),
        ('foo' + backslash * 2, False),
        ('foo' + backslash * 3, True),
    )

class TestBlankLineStrippingHelper(T.TestCase):

    def test_blank_line_stripping_helper(test):
        lines = [
            'foo',
            '',
            'bar',
            '\t',
            'baz',
        ]
        ret = list(server_properties._load._blank_line_stripping_helper(lines))
        T.assert_equal(ret, ['foo', 'bar', 'baz'])

class TestCommentStrippingHelper(T.TestCase):

    def test_comment_stripping_helper(self):
        lines = [
            'foo=bar',
            '# I\'m a comment',
            'herp=derp',
        ]

        ret = list(server_properties._load._comment_stripping_helper(lines))
        T.assert_equal(ret, [lines[0], lines[2]])

class TestLineContinuationHelper(T.TestCase):

    def test_no_continued_lines(self):
        lines = ['foo', 'bar']
        ret = list(server_properties._load._line_continuation_helper(lines))
        T.assert_equal(ret, lines)

    def test_continued_line(self):
        lines = ['foo\\', 'bar']
        ret = list(server_properties._load._line_continuation_helper(lines))
        T.assert_equal(ret, ['foobar'])

    def test_multiple_continued_lines(self):
        lines = ['foo\\', 'bar\\', 'baz']
        ret = list(server_properties._load._line_continuation_helper(lines))
        T.assert_equal(ret, ['foobarbaz'])

    def test_strips_leading_whitespace_on_continued_lines(self):
        lines = ['foo\\', '       bar']
        ret = list(server_properties._load._line_continuation_helper(lines))
        T.assert_equal(ret, ['foobar'])

    def test_nonterminated_line_errors(self):
        lines = ['foo\\']
        with T.assert_raises(InvalidPropertiesFileError):
            list(server_properties._load._line_continuation_helper(lines))
