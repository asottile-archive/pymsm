
from schemaform.base_property import BaseProperty
from schemaform.helpers import el

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

        if property_dict['type'] != 'boolean':
            raise ValueError('Unexpected type for boolean property.')

    def __pq__(self):
        """Returns the pyquery object representing this object."""
        label_text = self.property_dict.get('label', self.property_name.title())
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
