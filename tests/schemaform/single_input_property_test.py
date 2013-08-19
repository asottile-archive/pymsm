
import pyquery
import testify as T

from schemaform.single_input_property import SingleInputProperty

class TestSingleInputProperty(T.TestCase):

    path = 'herp.derp'
    property_name = 'harp'

    def get_elements(self, property_dict):
        instance = SingleInputProperty(
            self.path,
            self.property_name,
            property_dict,
        )
        retval = instance.__pq__()
        label_element = pyquery.PyQuery(retval[0])
        input_element = pyquery.PyQuery(retval[1])
        return label_element, input_element

    def test_label_text_not_specified(self):
        label_element, _ = self.get_elements({})
        T.assert_equal(label_element.text(), self.property_name.title())

    def test_label_specified(self):
        label = 'womp womp womp'
        label_element, _ = self.get_elements({'label': label})
        T.assert_equal(label_element.text(), label)

    def test_label_for_and_input_id(self):
        label_element, input_element = self.get_elements({})
        T.assert_equal(label_element.attr('for'), input_element.attr('id'))
        T.assert_equal(
            label_element.attr('for'),
            'id_' + self.path + '.' + self.property_name,
        )

    def test_input_name(self):
        _, input_element = self.get_elements({})
        T.assert_equal(
            input_element.attr('name'),
            self.path + '.' + self.property_name,
        )

    def test_default_value_not_specified(self):
        _, input_element = self.get_elements({})
        T.assert_equal(input_element.attr('value'), '')

    def test_default_value_specified(self):
        default = 'herpderp'
        _, input_element = self.get_elements({'default': default})
        T.assert_equal(input_element.attr('value'), default)

