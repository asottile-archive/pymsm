
# This interface roughly follows that of the interface for simplejson
# The implementation attempts to follow as closely to that of
# java.util.Properties
# http://docs.oracle.com/javase/6/docs/api/java/util/Properties.html

from ._load import load
from ._load import loads

# Make pyflakes happy
load, loads
