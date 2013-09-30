
import re

from server_properties.exceptions import InvalidPropertiesFileError

# This attempts to satisfy the spec of java.util.Properties
# Basing implementation off of http://docs.oracle.com/javase/6/docs/api/java/util/Properties.html

# From java.util.Properties:
# A comment line has an ASCII '#' or '!' as its first non-white space
# character; comment lines are also ignored and do not encode key-element
# information.
COMMENT_RE = re.compile('^\s*[!#]')

# Line continuation regex matches an odd number of backslashes terminating a
# line
LINE_CONTINUATION_RE = re.compile(
    r'''
        # beginning of string
        ^.*
        # A non-backslash character
        [^\\]
        # An odd number of backslashes
        (
            # A backslash character
            [\\]
            # Chunk of even number of backslashes
            (\\\\)*
        )
        # Terminating the string
        $
    ''',
    re.VERBOSE,
)

# Whitespace charactesr:
# From java.util.Properties:
# ... this format considers the characters space (' ', '\u0020'),
# tab ('\t', '\u0009'), and form feed ('\f', '\u000C') to be white space.
# From java.util.Properties:
# ... the first unescaped '=', ':', or white space character other than a line
# terminator. All of these key termination characters may be included in the
# key by escaping them with a preceding backslash character
CUSTOM_ESCAPE_SEQUENCES = (
    (r'\\=', '='),
    (r'\\:', ':'),
    (r'\\ ', ' '),
    ('\\\\\t', '\t'),
    ('\\\\\f', '\f'),
)

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
        if not COMMENT_RE.match(line):
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

        while LINE_CONTINUATION_RE.match(next):
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
