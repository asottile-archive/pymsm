
from schemaform.base_property import BaseProperty
from schemaform.helpers import el
from schemaform.helpers import get_type_from_schema
from schemaform.types import Types

EXPECTED_PROPERTY_TYPES = [Types.INTEGER, Types.NUMBER, Types.STRING]

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

        self._validate_single_input_property()

    def _validate_single_input_property(self):
        if get_type_from_schema(self.property_dict) not in EXPECTED_PROPERTY_TYPES:
            raise ValueError(
                'Unexpected type for single input property.'
            )

    def __pq__(self):
        """Returns the pyquery object representing this object."""
        label_text = self.get_label_text()
        default_value = self.normalize_value(
            self.property_dict.get('default', ''),
        )
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
