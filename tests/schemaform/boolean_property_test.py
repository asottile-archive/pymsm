
import pyquery
import testify as T

from schemaform.boolean_property import BooleanProperty

class TestBooleanProperty(T.TestCase):

    path = 'herp.derp'
    property_name = 'harp'

    def get_elements(self, property_dict):
        instance = BooleanProperty(
            self.path,
            self.property_name,
            property_dict,
        )
        retval = instance.__pq__()
        input_element = pyquery.PyQuery(retval[0])
        label_element = pyquery.PyQuery(retval[1])
        return label_element, input_element

    def test_label_for_and_input_id(self):
        label_element, input_element = self.get_elements({'type': 'boolean'})
        T.assert_equal(label_element.attr('for'), input_element.attr('id'))
        T.assert_equal(
            label_element.attr('for'),
            'id_' + self.path + '.' + self.property_name,
        )

    def test_input_name(self):
        _, input_element = self.get_elements({'type': 'boolean'})
        T.assert_equal(
            input_element.attr('name'),
            self.path + '.' + self.property_name,
        )

    def test_default_value_not_specified(self):
        _, input_element = self.get_elements({'type': 'boolean'})
        T.assert_equal(input_element.is_(':checked'), False)

    def test_default_value_specified(self):
        _, input_element = self.get_elements({'default': True, 'type': 'boolean'})
        T.assert_equal(input_element.is_(':checked'), True)

    def test_raises_on_invalid_property_type(self):
        with T.assert_raises(ValueError):
            self.get_elements({'type': 'string'})
