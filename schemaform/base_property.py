

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

    def get_input_name(self):
        """Returns a dotted path that will be used as the <input> name"""
        parts = [self.property_name]
        if self.dotted_path_to_property:
            parts.insert(0, self.dotted_path_to_property)
        return '.'.join(parts)

    def __html__(self):
        raise NotImplementedError
