
from schemaform.base_property import BaseProperty

class StringProperty(BaseProperty):
    """A StringProperty represents a property in a schema of type string."""

    def __init__(self, dotted_path_to_property, property_name, property_dict):
        """Constructs a StringProperty

        Args:
            dotted_path_to_property - Javascript-like dotted path to get to the
                object which contains this property (empty string if at root)
            property_name - name of this property
            property_dict - the portion of the json schema representing this
                property
        """
        super(StringProperty, self).__init__(
            dotted_path_to_property,
            property_name,
            property_dict,
        )

    def __html__(self):
        """Returns the html representing this object."""
        pass
