
from schemaform.base_property import BaseProperty
from schemaform.helpers import el

STRING_TYPE = 'string'
INTEGER_TYPE = 'integer'
NUMBER_TYPE = 'number'
EXPECTED_PROPERTY_TYPES = [INTEGER_TYPE, NUMBER_TYPE, STRING_TYPE]

class SingleInputProperty(BaseProperty):
    """A SingleInputProperty represents a property that represents a single
    input such as a string or number.
    """

    def __init__(self, dotted_path_to_property, property_name, property_dict):
        """Constructs a SingleInputProperty

        Args:
            dotted_path_to_property - Javascript-like dotted path to get to the
                object which contains this property (empty string if at root)
            property_name - name of this property
            property_dict - the portion of the json schema representing this
                property
        """
        super(SingleInputProperty, self).__init__(
            dotted_path_to_property,
            property_name,
            property_dict,
        )

        self._property_type = property_dict.get('type', STRING_TYPE)
        self._validate_property_type()

    def _validate_property_type(self):
        if self._property_type not in EXPECTED_PROPERTY_TYPES:
            raise ValueError(
                'Unexpected type for single input property: %s' % (
                    self._property_type,
                )
            )

    def _get_default_value(self):
        """Returns the default value for the input element."""
        default_value = self.property_dict.get('default', '')
        if not isinstance(default_value, basestring):
            default_value = unicode(default_value)
        return default_value

    def __pq__(self):
        """Returns the pyquery object representing this object."""
        label_text = self.get_label_text()
        default_value = self._get_default_value()
        input_name = self.get_input_name()
        input_id = 'id_' + input_name

        label_element = el('label', text=label_text, **{'for': input_id})
        input_element = el(
            'input',
            name=input_name,
            id=input_id,
            value=default_value,
        )
        return label_element + input_element
