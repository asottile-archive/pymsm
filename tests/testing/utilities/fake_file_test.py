
import testify as T

from testing.utilities.fake_file import FakeFile

class TestFakeFile(T.TestCase):

    def test_fake_file_asserts_when_not_given_contents(self):
        with T.assert_raises(AssertionError):
            FakeFile().read()

    def test_written_contents(self):
        fake_file = FakeFile()
        writes = ['foo', 'bar', 'baz', '\n', 'womp']
        for write in writes:
            fake_file.write(write)

        T.assert_equal(fake_file._written_contents, ''.join(writes))
