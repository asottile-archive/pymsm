
import re
import testify as T

import server_properties._load
from server_properties.exceptions import InvalidPropertiesFileError
from testing.base_classes.regex import BooleanSearchReTestBase
from testing.base_classes.regex import ReplaceReTestBase

class TestCommentRe(BooleanSearchReTestBase):

    regex = server_properties._load.COMMENT_RE

    expected = (
        ('!this is a comment', True),
        ('# this is a comment', True),
        (' ! this is a comment', True),
        (' # this is a comment', True),
        ('foo=bar#this is not a comment', False),
        ('foo=bar!this is not a comment', False),
    )

class TestLineContinuationRe(BooleanSearchReTestBase):

    regex = server_properties._load.LINE_CONTINUATION_RE

    backslash = '\\'

    expected = (
        ('', False),
        (backslash, True),
        ('foo', False),
        ('foo' + backslash * 1, True),
        ('foo' + backslash * 2, False),
        ('foo' + backslash * 3, True),
    )

class TestUnescapeReSkeleton(ReplaceReTestBase):
    regex = re.compile(
        server_properties._load.UNESCAPE_RE_SKELETON.format(':'),
        re.VERBOSE,
    )
    replacement = r'\1~'

    expected = (
        (r'\:', '~'),
        (r'aa\:', 'aa~'),
        (r'\\\:', r'\\~'),
        # Sadface, I can't get this one to replace correctly, I'll have to
        # replace in a loop instead it appears
        # (r'\:\:', '~~'),
        # No replace here!
        (r'\\\\:', r'\\\\:'),
        (':', ':'),
    )

class TestKeySplitter(T.TestCase):

    # Tuple of tuples of (input, output_key, output_value)
    expected = (
        ('foo=bar', 'foo', 'bar'),
        ('foo:bar', 'foo', 'bar'),
        ('foo bar', 'foo', 'bar'),

        ('foo\ bar=baz', 'foo\ bar', 'baz'),
        ('foo\=bar=baz', 'foo\=bar', 'baz'),
        ('foo\:bar=baz', 'foo\:bar', 'baz'),

        # Some examples from minecraft's server.properties
        ('generator-settings=', 'generator-settings', ''),
        ('server-port=25565', 'server-port', '25565'),
        ('motd=A Minecraft Server', 'motd', 'A Minecraft Server'),

        # From java.util.Properties:
        ('Truth = Beauty', 'Truth', 'Beauty'),
        ('        Truth:Beauty', 'Truth', 'Beauty'),
        ('Truth             :Beauty', 'Truth', 'Beauty'),

        # This next one also comes from java.util.Properties but I'll simplify
        # it to how we would expect to process it
        (
            list(server_properties._load._line_continuation_helper([
                'fruits                    apple, banana, pear, \\',
                '                          cantaloupe, watermelon, \\',
                '                          kiwi, mango',
            ]))[0],
            'fruits', 'apple, banana, pear, cantaloupe, watermelon, kiwi, mango'
        ),

        # This is one of the examples they use for a key with no value
        ('cheeses', 'cheeses', ''),
    )

    def test_expected(self):
        for input, expected_key, expected_value in self.expected:
            key, value = server_properties._load.KeySplitter(input).split()
            if key != expected_key or value != expected_value:
                raise AssertionError(
                    'KeySplitter did not yield the expected key/value\n'
                    'Input: {0}\n'
                    'Key (Expected): {1}\n'
                    'Key (Actually): {2}\n'
                    'Value (Expected): {3}\n'
                    'Value (Actually): {4}\n'.format(
                        input, expected_key, key, expected_value, value
                    )
                )

class TestDecodeChars(T.TestCase):

    def test_decode_chars_single_char(self):
        input = 'foo\=bar\=baz'
        ret = server_properties._load._decode_chars(input, ('=',))
        T.assert_equal(ret, 'foo=bar=baz')

    def test_decode_chars_multiple_chars(self):
        input = r'foo\=\:bar\=\:baz'
        ret = server_properties._load._decode_chars(input, ('=', ':'))
        T.assert_equal(ret, 'foo=:bar=:baz')

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
