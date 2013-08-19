
from schemaform.base_property import BaseProperty
from schemaform.helpers import el

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

    def __pq__(self):
        """Returns the pyquery object representing this object."""
        label_text = self.property_dict.get('label', self.property_name.title())
        default_value = self.property_dict.get('default', '')
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
