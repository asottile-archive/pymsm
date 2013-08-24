
import pyquery
import testify as T

from schemaform.radio_enum_property import RadioEnumProperty
from schemaform.radio_enum_property import RadioInput

class TestBooleanProperty(T.TestCase):

    path = 'herp.derp'
    property_name = 'harp'

    def get_elements(self, property_dict):
        instance = RadioEnumProperty(
            self.path,
            self.property_name,
            property_dict,
        )
        return instance.__pq__()

    def test_raises_on_non_enum_schema(self):
        with T.assert_raises(ValueError):
            self.get_elements({'type': 'string'})

    def test_does_not_raise_for_no_labels(self):
        self.get_elements({'type': 'string', 'enum': ['a', 'b', 'c']})

    def test_raises_on_labels_wrong_length(self):
        with T.assert_raises(ValueError):
            self.get_elements({
                'type': 'string',
                'enum': ['a', 'b', 'c'],
                'labels': ['Letter A', 'Letter B'],
            })

class TestRadioInput(T.TestCase):

    name = 'foo'
    value = 'value'
    label = 'label'

    def get_radio_input(self, checked=False):
        return RadioInput(self.name, self.value, self.label, checked)

    def get_radio_input_elements(self, **kwargs):
        radio, label = self.get_radio_input(**kwargs).__pq__()
        return pyquery.PyQuery(radio), pyquery.PyQuery(label)

    def test_id(self):
        radio_input = self.get_radio_input()
        expected_id = 'id_%s_value' % self.name
        T.assert_equal(radio_input.id, expected_id)
        input, label = radio_input.__pq__()
        input, label = pyquery.PyQuery(input), pyquery.PyQuery(label)
        T.assert_equal(input.attr('id'), expected_id)
        T.assert_equal(label.attr('for'), expected_id)

    def test_name(self):
        input, _ = self.get_radio_input_elements()
        T.assert_equal(input.attr('name'), self.name)

    def test_value(self):
        input, _ = self.get_radio_input_elements()
        T.assert_equal(input.attr('value'), self.value)

    def test_label(self):
        _, label = self.get_radio_input_elements()
        T.assert_equal(label.text(), self.label)

    def test_checked_is_checked(self):
        input, _ = self.get_radio_input_elements(checked=True)
        T.assert_equal(input.is_(':checked'), True)

    def test_checked_not_checked(self):
        input, _ = self.get_radio_input_elements(checked=False)
        T.assert_equal(input.is_(':checked'), False)

