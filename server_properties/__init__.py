
# This interface roughly follows that of the interface for simplejson
# The implementation attempts to follow as closely to that of
# java.util.Properties but differs in several key aspects:
# - The load/loads methods read in ASCII (the spec denotes ISO 8859-1)
# - The dump/dumps methods write in ASCII (the spec denotes ISO 8859-1)

# TODO: support unicode (reading and writing ISO 8859-1)
# The reason it is not simple to support unicode is when writing out,
# unicode.encode('string_escape') prints '\x7f' instead of '\u007f' which is
# what the java implementation expects.  As of now, using the load(s) methods
# will not convert the unicode character to it's representation and will leave
# it as \u####.  The dump(s) methods will throw a UnicodeDecodeError if given
# unicode with non-ascii characters.  This is sad and I hope to fix this.

from ._load import load
from ._load import loads

# Make pyflakes happy
load, loads
