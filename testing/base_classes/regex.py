
import testify as T

class BooleanMatchReTestBase(T.TestCase):
    """A base class for testing a matching regex."""
    __test__ = False

    # Assign regex
    regex = None

    # Assign expected outcomes, should be an iterable of tuples:
    # Example:
    # expected = (
    #    ('foo', True),
    #    ('bar', False),
    # )
    expected = None

    def test_regex(self):
        for test, expected in self.expected:
            match = self.regex.match(test)
            if bool(match) != expected:
                raise AssertionError(
                    'Failed test of regex {0}.\n'
                    'Test: {1}\n'
                    'Expected to match? {2}\n'.format(
                        self.regex.pattern, test, expected
                    )
                )

class ReplaceReTestBase(T.TestCase):
    """A base class for testing a replacing regex."""
    __test__ = False

    # Assign regex
    regex = None

    # Assign replacement string
    replacement = None

    # Assign expected outcomes, should be an iterable of tuples:
    # Example:
    # expected = (
    #     ('foo', 'boo'),
    #     ('abcdef', 'abcdeb')
    # )
    expected = None

    def test_regex(self):
        for test, expected in self.expected:
            replaced = self.regex.sub(self.replacement, test)
            if replaced != expected:
                raise AssertionError(
                    'Failed test of regex {0}.\n'
                    'Replace String: {1}\n'
                    'Test: {2}\n'
                    'Expected outcome: {3}\n'.format(
                        self.regex.pattern, self.replacement, test, expected
                    )
                )
