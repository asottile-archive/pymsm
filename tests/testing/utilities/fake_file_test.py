
import testify as T

from testing.utilities.fake_file import FakeFile

class TestFakeFile(T.TestCase):

    def test_fake_file_asserts_when_not_given_contents(self):
        with T.assert_raises(AssertionError):
            FakeFile().read()
