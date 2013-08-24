
from schemaform.helpers import validate_default_value
from schemaform.helpers import validate_enum_values

class BaseProperty(object):
    """Base class for all properties."""

    def __init__(self, dotted_path_to_property, property_name, property_dict):
        """Constructs the BaseProperty

        Args:
            dotted_path_to_property - Javascript-like dotted path to get to the
                object which contains this property (empty string if at root)
            property_name - name of this property
            property_dict - the portion of the json schema representing this
                property
        """
        self.dotted_path_to_property = dotted_path_to_property
        self.property_name = property_name
        self.property_dict = property_dict

        validate_default_value(self.property_dict)
        validate_enum_values(self.property_dict)

    def get_input_name(self):
        """Returns a dotted path that will be used as the <input> name"""
        parts = [self.property_name]
        if self.dotted_path_to_property:
            parts.insert(0, self.dotted_path_to_property)
        return '.'.join(parts)

    def get_label_text(self):
        return self.property_dict.get('label', self.property_name.title())

    def __pq__(self):
        raise NotImplementedError
