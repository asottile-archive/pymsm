
import collections
import itertools

from schemaform.base_property import BaseProperty
from schemaform.helpers import combine_pqables
from schemaform.helpers import el
from schemaform.helpers import get_type_from_schema
from schemaform.types import Types

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
        if get_type_from_schema(self.property_dict) != Types.ENUM:
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
        labels = self.property_dict.get(
            'labels',
            [self.normalize_value(value).title() for value in values]
        )
        default_value = self.property_dict.get('default', values[0])

        for value, label in itertools.izip(values, labels):
            yield RadioInput(
                name,
                self.normalize_value(value),
                label,
                value == default_value,
            )

    def __pq__(self):
        """Returns the pyquery object representing this object."""
        contents = combine_pqables(
            el('legend', text=self.get_label_text()), self._get_inputs(),
            acceptable_iterable_type=RadioInput,
        )
        return contents.wrapAll(el('fieldset').__html__())

