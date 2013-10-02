
import re

from server_properties.exceptions import InvalidPropertiesFileError

# This attempts to satisfy the spec of java.util.Properties
# Basing implementation off of http://docs.oracle.com/javase/6/docs/api/java/util/Properties.html

# Line continuation regex matches an odd number of backslashes terminating a
# line
LINE_CONTINUATION_RE = re.compile(
    r'''
        # beginning of string or non backslash character
        (\A|[^\\])
        # An odd number of backslashes
        [\\](\\\\)*
        # Terminating the string
        $
    ''',
    re.VERBOSE,
)

# From java.util.Properties:
# A comment line has an ASCII '#' or '!' as its first non-white space
# character; comment lines are also ignored and do not encode key-element
# information.
COMMENT = ('#', '!')

COMMENT_RE = re.compile('^\s*[{0}]'.format(''.join(COMMENT)))

# From java.util.Properties:
# ... this format considers the characters space (' ', '\u0020'),
# tab ('\t', '\u0009'), and form feed ('\f', '\u000C') to be white space.
WHITESPACE = (' ', '\t', '\f')

# From java.util.Properties:
# The key contains all of the characters in the line starting with the first
# non-white space character and up to, but not including, the first unescaped
# '=', ':', or white space character other than a line terminator.
ASSIGNMENT = ('=', ':')

END_OF_ASSIGNMENT = set(
    WHITESPACE + ASSIGNMENT
)

# From java.util.Properties:
# ... by escaping them with a preceding backslash character
# Comment characters...
# From java.util.Properties:
# The key and element characters #, !, =, and : are written with a preceding
# backslash to ensure that they are properly loaded.
SPECIALLY_ESCAPED_CHARACTERS = set(
    COMMENT + WHITESPACE + ASSIGNMENT
)

UNESCAPE_RE_SKELETON = r'''
    (
        # Beginning of string or a non-backslash character
        (?:\A|[^\\])
        # A chunk of even regexes
        (?:\\\\)*
    )
    # Our replace character is 0
    \\{0}
'''

class KeySplitter(object):
    """A KeySplitter is for splitting up lines for loading properties."""

    def __init__(self, line):
        # From java.util.Properties:
        # The key contains all of the characters in the line starting with the
        # first non-white space character
        self.line = line.lstrip()
        self.position = 0
        self.in_escape = False

    def _advance(self):
        """Advances position and sets whether or not the current position is in
        a character escape.
        """
        if not self.in_escape and self.line[self.position] == '\\':
            self.in_escape = True
        else:
            self.in_escape = False
        self.position += 1

    @property
    def _is_end_of_key(self):
        """The current position is the end of the key if the character is not in
        an escape sequence and is at a key terminating character.

        Alternately the end of key could be the end of the string (leading to a
        key with a value of an empty string.

        From java.util.Properties:
            As a third example, the line:

            cheeses


            specifies that the key is "cheeses" and the associated element is
            the empty string "".
        """
        return (
            self.position == len(self.line)
        ) or (
            not self.in_escape and
            self.line[self.position] in END_OF_ASSIGNMENT
        )

    def _get_key_and_value(self):
        """Call after _is_end_of_key returns True."""
        key = self.line[:self.position]

        # From java.util.Properties:
        # Any white space after the key is skipped; if the first non-white
        # space character after the key is '=' or ':', then it is ignored and
        # any white space characters after it are also skipped. All remaining
        # characters on the line become part of the associated element string;
        # if there are no remaining characters, the element is the empty string
        # "".
        value = self.line[self.position:].lstrip()
        if len(value) and value[0] in ASSIGNMENT:
            value = value[1:].lstrip()
        return key, value

    def split(self):
        """Splits the line into key, value.  Note these are still encoded."""
        while not self._is_end_of_key:
            self._advance()
        return self._get_key_and_value()


def _decode_chars(s, chars):
    """Decodes characters in chars escaped by a \."""
    def unescape_char(str_to_replace, char_to_replace):
        """Unescapes a single character on a string."""
        unescape_re = re.compile(
            UNESCAPE_RE_SKELETON.format(char_to_replace),
            re.VERBOSE,
        )
        unescape_replace = r'\1{0}'.format(char_to_replace)
        while unescape_re.search(str_to_replace):
            str_to_replace = unescape_re.sub(unescape_replace, str_to_replace)
        return str_to_replace

    for char in chars:
        s = unescape_char(s, char)

    return s

def _blank_line_stripping_helper(iterable):
    """Skips blank lines as described in java.util.Properties:
        A natural line that contains only white space characters is considered
        blank and is ignored.

    Args:
        iterable - An iterable of lines
    """
    for line in iterable:
        if line.strip():
            yield line

def _comment_stripping_helper(iterable):
    """Generator to strip comments from a properties file.

    Args:
        iterable - An iterable of lines
    """
    for line in iterable:
        if not COMMENT_RE.search(line):
            yield line

def _line_continuation_helper(iterable):
    """Generator to assist with line continuation as described in
    java.util.Properties:
        A logical line holds all the data of a key-element pair, which may be
        spread out across several adjacent natural lines by escaping the line
        terminator sequence with a backslash character \.

    Args:
        gen - A Generator object
    """
    gen = iter(iterable)

    while True:
        try:
            next = gen.next()
        except StopIteration:
            return

        while LINE_CONTINUATION_RE.search(next):
            # Strip of end line character
            next = next[:-1]
            # Add the next line
            try:
                next += gen.next().lstrip()
            except StopIteration:
                raise InvalidPropertiesFileError('Unexpected EOF')

        yield next

def load(file_like_object):
    """Loads a minecraft configuration from a file-like object."""
    print 'hello world'

def loads(s):
    """Loads a minecraft configuration from a string."""
    return load(s.splitlines())
