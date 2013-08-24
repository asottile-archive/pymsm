import collections
import itertools
import pyquery

from schemaform.base_property import BaseProperty
from schemaform.helpers import el

class RadioInput(collections.namedtuple(
    'RadioInput', ['name', 'value', 'label', 'checked']
)):
    """Represents a <input type="radio" ...><label for...>"""

    @property
    def id(self):
        return 'id_%s_%s' % (self.name, self.value)

    def __pq__(self):
        """Returns the pyQuery representation."""
        input_attrs = {
            'id': self.id,
            'name': self.name,
            'value': self.value,
        }

        if self.checked:
            input_attrs['checked'] = 'checked'

        input_element = el('input', **input_attrs)
        label_element = el('label', text=self.label, **{'for': self.id})
        return input_element + label_element

class RadioEnumProperty(BaseProperty):
    """A RadioEnumProperty represents a property that represents an enum
    and results in radio elements.
    """

    def __init__(self, dotted_path_to_property, property_name, property_dict):
        """Constructs a RadioEnumProperty

        Args:
            dotted_path_to_property - Javascript-like dotted path to get to the
                object which contains this property (empty string if at root)
            property_name - name of this property
            property_dict - the portion of the json schema representing this
                property
        """
        super(RadioEnumProperty, self).__init__(
            dotted_path_to_property,
            property_name,
            property_dict,
        )

        self._validate_enum()

    def _validate_enum(self):
        if 'enum' not in self.property_dict:
            raise ValueError('Unexpected schema for enum property.')

        # Validate our labels extension
        if 'labels' in self.property_dict:
            if (
                len(self.property_dict['labels']) !=
                len(self.property_dict['enum'])
            ):
                raise ValueError(
                    'A label must be specified for all values.'
                    'Enum (%s) Labels (%s)' % (
                        self.property_dict['enum'],
                        self.property_dict['labels'],
                    )
                )

    def _get_inputs(self):
        name = self.get_input_name()
        values = self.property_dict['enum']
        labels = self.property_dict.get('labels', values)
        default_value = self.property_dict.get('default', values[0])

        for value, label in itertools.izip(values, labels):
            yield RadioInput(
                name,
                value,
                label,
                value == default_value,
            )

    def __pq__(self):
        """Returns the pyquery object representing this object."""
        inputs = [input.__pq__() for input in self._get_inputs()]
        inputs_as_pyquery = pyquery.PyQuery(list(itertools.chain(*inputs)))
        label = self.property_dict.get('label', self.get_input_name())
        legend = el('legend', text=label)
        radio_contents = legend + inputs_as_pyquery
        radio_contents.wrap(el('fieldset').__html__())
        return radio_contents
