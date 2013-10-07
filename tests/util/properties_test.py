# -*- coding: utf-8 -*-

import os.path
import re
import testify as T

import config.application
import util.properties
from util.properties import InvalidPropertiesFileError
from testing.base_classes.regex import BooleanSearchReTestBase
from testing.base_classes.regex import ReplaceReTestBase
from testing.base_classes.tempdir_test_case import TempdirTestCase

class TestCommentRe(BooleanSearchReTestBase):

    regex = util.properties.COMMENT_RE

    expected = (
        ('!this is a comment', True),
        ('# this is a comment', True),
        (' ! this is a comment', True),
        (' # this is a comment', True),
        ('foo=bar#this is not a comment', False),
        ('foo=bar!this is not a comment', False),
    )

class TestLineContinuationRe(BooleanSearchReTestBase):

    regex = util.properties.LINE_CONTINUATION_RE

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
        util.properties.UNESCAPE_RE_SKELETON.format(':'),
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

class TestUnescapeReWithSpaceWeirdness(ReplaceReTestBase):
    regex = re.compile(
        util.properties.UNESCAPE_RE_SKELETON.format(' '),
        re.VERBOSE,
    )
    replacement = r'\1 '

    expected = (
        (r'\=', '\='),
        (r'\ ', ' '),
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
            list(util.properties._line_continuation_helper([
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
            key, value = util.properties.KeySplitter(input).split()
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
        ret = util.properties._decode_chars(input, ('=',))
        T.assert_equal(ret, 'foo=bar=baz')

    def test_decode_chars_multiple_chars(self):
        input = r'foo\=\:bar\=\:baz'
        ret = util.properties._decode_chars(input, ('=', ':'))
        T.assert_equal(ret, 'foo=:bar=:baz')

class TestEncodeChars(T.TestCase):

    def test_encode_chars_single_char(self):
        input = 'foo=bar=baz'
        ret = util.properties._encode_chars(input, ('=',))
        T.assert_equal(ret, 'foo\=bar\=baz')

    def test_encode_chars_multiple_chars(self):
        input = 'foo=:bar=:baz'
        ret = util.properties._encode_chars(input, ('=', ':'))
        T.assert_equal(ret, 'foo\=\:bar\=\:baz')

class TestEncodeDecodeRoundTrip(T.TestCase):

    strs = (
        'foo=bar',
        'foo:bar',
        'foo=:bar',
        ':=:=====:::',
    )

    chars = ('=', ':',)

    def test_encode_decode_round_trip(self):
        for s in self.strs:
            encoded = util.properties._encode_chars(s, self.chars)
            decoded = util.properties._decode_chars(encoded, self.chars)
            T.assert_equal(decoded, s)

class TestEncodeUnicodeEscapes(T.TestCase):

    expected = (
        ('\x1f', r'\u001f'),
        ('\x20', ' ',),
        ('\x21', '!',),
        ('\x7e', '~',),
        ('\x7f', r'\u007f'),
    )

    def test_encode_unicode_escapes(self):
        for input, output in self.expected:
            T.assert_equal(
                output,
                util.properties._encode_unicode_escapes(input),
            )

class TestDecodeKeyValue(T.TestCase):

    def test_decode_unicode(self):
        key, value = util.properties._decode_key_value(
            r'\u2603', r'\u2603',
        )
        T.assert_equal(key, u'☃')
        T.assert_equal(value, u'☃')

    def test_decode_escaped_characters(self):
        key, value = util.properties._decode_key_value(
            r'\\\=\ \:\#\!', 'bar'
        )
        T.assert_equal(key, r'\= :#!')
        T.assert_equal(value, 'bar')


class TestEncodeKeyValue(T.TestCase):

    def test_encode_unicode(self):
        key, value = util.properties._encode_key_value(
            u'☃\x1f', u'☃\x1f',
        )
        T.assert_equal(key, r'\u2603\u001f')
        T.assert_equal(value, r'\u2603\u001f')

    def test_encode_escape_characters(self):
        key, value = util.properties._encode_key_value(
            '\= :#!', 'foo bar',
        )
        T.assert_equal(key, r'\\\=\ \:\#\!')
        T.assert_equal(value, 'foo bar')


class TestBlankLineStrippingHelper(T.TestCase):

    def test_blank_line_stripping_helper(test):
        lines = [
            'foo',
            '',
            'bar',
            '\t',
            'baz',
        ]
        ret = list(util.properties._blank_line_stripping_helper(lines))
        T.assert_equal(ret, ['foo', 'bar', 'baz'])

class TestCommentStrippingHelper(T.TestCase):

    def test_comment_stripping_helper(self):
        lines = [
            'foo=bar',
            '# I\'m a comment',
            'herp=derp',
        ]

        ret = list(util.properties._comment_stripping_helper(lines))
        T.assert_equal(ret, [lines[0], lines[2]])

class TestLineContinuationHelper(T.TestCase):

    def test_no_continued_lines(self):
        lines = ['foo', 'bar']
        ret = list(util.properties._line_continuation_helper(lines))
        T.assert_equal(ret, lines)

    def test_continued_line(self):
        lines = ['foo\\', 'bar']
        ret = list(util.properties._line_continuation_helper(lines))
        T.assert_equal(ret, ['foobar'])

    def test_multiple_continued_lines(self):
        lines = ['foo\\', 'bar\\', 'baz']
        ret = list(util.properties._line_continuation_helper(lines))
        T.assert_equal(ret, ['foobarbaz'])

    def test_strips_leading_whitespace_on_continued_lines(self):
        lines = ['foo\\', '       bar']
        ret = list(util.properties._line_continuation_helper(lines))
        T.assert_equal(ret, ['foobar'])

    def test_nonterminated_line_errors(self):
        lines = ['foo\\']
        with T.assert_raises(InvalidPropertiesFileError):
            list(util.properties._line_continuation_helper(lines))

@T.suite('integration')
class TestPropertiesLoadIntegration(T.TestCase):

    expected_data = {
        'generator-settings': '',
        'allow-nether': 'true',
        'level-name': 'world',
        'enable-query': 'false',
        'allow-flight': 'false',
        'server-port': '25565',
        'foo ': 'bar',
    }

    def _get_file_path(self):
        return os.path.join(
            config.application.APP_ROOT,
            'testing/data/files/sample_server.properties',
        )

    def test_load_from_given_file(self):
        with open(self._get_file_path(), 'r') as file:
            ret = util.properties.Properties.load(file)

        T.assert_equal(ret, self.expected_data)

    def test_load_from_file_string(self):
        with open(self._get_file_path(), 'r') as file:
            file_contents = file.read()

        ret = util.properties.Properties.loads(file_contents)
        T.assert_equal(ret, self.expected_data)

@T.suite('integration')
class TestPropertiesDumpIntegration(TempdirTestCase):

    data = util.properties.Properties({
        'generator-settings': '',
        'allow-nether': 'true',
        'foo': 'bar',
    })

    def _get_file_path(self):
        return os.path.join(self.tempdir, 'temp.properties')

    def test_dump_to_file(self):
        with open(self._get_file_path(), 'w') as tempfile:
            self.data.dump(tempfile)

        with open(self._get_file_path(), 'r') as tempfile:
            props = util.properties.Properties.load(tempfile)
            T.assert_equal(props, self.data)

    def test_dump_to_string(self):
        data_str = self.data.dumps()
        props = util.properties.Properties.loads(data_str)
        T.assert_equal(props, self.data)
