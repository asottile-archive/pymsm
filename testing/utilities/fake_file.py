
import mock

from util.iter import flatten

class FakeFile(object):
    """FakeFile is useful when you want to mock the return value of
    __builtin__.open
    """
    def __init__(self, contents=None):
        """Initialize a fake file.  For a write-only file, don't specify args

        Args:
            contents - The contents of the file (a string for now)
        """
        self.contents = contents
        self.write = mock.Mock(spec=lambda self, s: None)

    def read(self):
        if self.contents is None:
            raise AssertionError(
                'Tried to read a file that was not supposed to be readable'
            )
        return self.contents

    @property
    def _written_contents(self):
        return ''.join(flatten(
            self.write.call_args_list, acceptable_iterable_type=basestring
        ))

    def __enter__(self): return self
    def __exit__(self, *args): pass

