
import testify as T

from testing.assertions.response import assert_no_response_errors
from util.auto_namedtuple import auto_namedtuple

class TestAssertNoResponseErrors(T.TestCase):

    def test_assertion_with_response_errors(self):
        with T.assert_raises(AssertionError):
            response = auto_namedtuple(
                response=auto_namedtuple(status_code=500),
            )
            assert_no_response_errors(response)

    def test_assertion_without_response_errors(self):
        response = auto_namedtuple(
            response=auto_namedtuple(status_code=200),
        )
        assert_no_response_errors(response)
