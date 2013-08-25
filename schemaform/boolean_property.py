
from schemaform.base_property import BaseProperty
from schemaform.helpers import el
from schemaform.helpers import get_type_from_schema
from schemaform.types import Types

class BooleanProperty(BaseProperty):
    """A BooleanProperty represents a property that represents a boolean."""

    def __init__(self, dotted_path_to_property, property_name, property_dict):
        """Constructs a BooleanProperty

        Args:
            dotted_path_to_property - Javascript-like dotted path to get to the
                object which contains this property (empty string if at root)
            property_name - name of this property
            property_dict - the portion of the json schema representing this
                property
        """
        super(BooleanProperty, self).__init__(
            dotted_path_to_property,
            property_name,
            property_dict,
        )

        self._validate_boolean_property()

    def _validate_boolean_property(self):
        if get_type_from_schema(self.property_dict) != Types.BOOLEAN:
            raise ValueError('Unexpected schema for boolean property.')

    def __pq__(self):
        """Returns the pyquery object representing this object."""
        label_text = self.get_label_text()
        input_name = self.get_input_name()
        input_id = 'id_' + input_name

        input_attrs = {
            'name': input_name,
            'id': input_id,
        }

        if self.property_dict.get('default', False):
            input_attrs['checked'] = 'checked'

        input_element = el('input', **input_attrs)
        label_element = el('label', text=label_text, **{'for': input_id})
        return input_element + label_element
