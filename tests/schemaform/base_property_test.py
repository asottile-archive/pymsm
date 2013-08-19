
import testify as T

from schemaform.base_property import BaseProperty

class TestBaseProperty(T.TestCase):

    def test_get_input_name_no_path(self):
         instance = BaseProperty('', 'foo', {})
         retval = instance.get_input_name()
         T.assert_equal(retval, 'foo')

    def test_get_input_name_with_path(self):
        instance = BaseProperty('foo.bar', 'baz', {})
        retval = instance.get_input_name()
        T.assert_equal(retval, 'foo.bar.baz')
