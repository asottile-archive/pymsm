
import itertools
import pyquery
import testify as T

from schemaform.radio_enum_property import RadioEnumProperty
from schemaform.radio_enum_property import RadioInput
from util.auto_namedtuple import auto_namedtuple

class TestRadioEnumProperty(T.TestCase):

    path = 'herp.derp'
    property_name = 'harp'

    def get_elements(self, property_dict):
        instance = RadioEnumProperty(
            self.path,
            self.property_name,
            property_dict,
        )

        fieldset = instance.__pq__()
        legend = fieldset.find('legend')
        inputs = [pyquery.PyQuery(input) for input in fieldset.find('input')]
        labels = [pyquery.PyQuery(label) for label in fieldset.find('label')]
        return auto_namedtuple(
            fieldset=fieldset,
            legend=legend,
            inputs=inputs,
            labels=labels,
        )

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

    def test_radios(self):
        values = ['a', 'b', 'c']
        elements = self.get_elements({
            'type': 'string',
            'enum': values,
        })
        for input, value in itertools.izip(elements.inputs, values):
            T.assert_equal(input.attr('value'), value)
            T.assert_equal(input.attr('name'), 'herp.derp.harp')

    def test_radios_with_ints(self):
        values = [1, 2, 3]
        elements = self.get_elements({
            'type': 'integer',
            'enum': values,
        })
        for input, value in itertools.izip(elements.inputs, values):
            T.assert_equal(input.attr('value'), unicode(value))

    def test_labels_not_specified(self):
        values = ['herp', 'derp', 'darp']
        elements = self.get_elements({
            'type': 'string',
            'enum': values,
        })
        for label, value in itertools.izip(elements.labels, values):
            T.assert_equal(label.text(), value.title())

    def test_labels_specified(self):
        labels = ['herp', 'derp', 'darp']
        elements = self.get_elements({
            'type': 'string',
            'enum': ['a', 'b', 'c'],
            'labels': labels,
        })
        for label, label_text in itertools.izip(elements.labels, labels):
            T.assert_equal(label.text(), label_text)

    def test_legend_no_text(self):
        elements = self.get_elements({'enum': ['a', 'b', 'c']})
        T.assert_equal(elements.legend.text(), self.property_name.title())

    def test_legend_specified(self):
        label = 'foo'
        elements = self.get_elements({'enum': ['a', 'b', 'c'], 'label': label})
        T.assert_equal(elements.legend.text(), label)

    def test_default_value_none_specified(self):
        values = ['herp', 'derp', 'darp']
        elements = self.get_elements({'enum': values})
        T.assert_equal(elements.fieldset.find(':checked').val(), values[0])

    def test_default_value_specified(self):
        values = ['herp', 'derp', 'darp']
        default = values[2]
        elements = self.get_elements({'enum': values, 'default': default})
        T.assert_equal(elements.fieldset.find(':checked').val(), default)

    def test_all_are_radios(self):
        elements = self.get_elements({'enum': ['herp', 'derp']})
        for input in elements.inputs:
            T.assert_equal(input.attr('type'), 'radio')


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

