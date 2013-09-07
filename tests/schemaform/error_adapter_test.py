
import testify as T

from schemaform.error_adapter import ErrorAdapter
from util.auto_namedtuple import auto_namedtuple

class TestErrorAdapter(T.TestCase):

    def _get_error_adapter(self, validator, message, path):
        return ErrorAdapter.from_validation_error(auto_namedtuple(
            validator=validator,
            message=message,
            path=path,
        ))

    def test_error_adapter_normal_error(self):
        message = str(object())
        path = ['foo', 'bar']
        error = self._get_error_adapter('type', message, path)
        T.assert_is(error.message, message)
        T.assert_equal(error.dotted_path, '.'.join(path))

    def test_error_adapter_required_adapter(self):
        prop_name = 'herpaderp'
        message = "'%s' is a required property" % prop_name
        path = ['foo', 'bar']
        error = self._get_error_adapter('required', message, path)
        T.assert_is(error.message, message)
        T.assert_equal(error.dotted_path, '.'.join(path + [prop_name]))

    def test_error_adapter_required_root_parameter(self):
        prop_name = 'herpaderp'
        message = "'%s' is a required property" % prop_name
        path = []
        error = self._get_error_adapter('required', message, path)
        T.assert_is(error.message, message)
        T.assert_equal(error.dotted_path, prop_name)
