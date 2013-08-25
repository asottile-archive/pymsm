
from schemaform.base_property import BaseProperty
from schemaform.helpers import el
from schemaform.helpers import get_type_from_schema
from schemaform.types import Types

class ObjectProperty(BaseProperty):
    """An ObjectProperty represents a property that represents a
    collection of properties.
    """

    def __init__(
        self,
        dotted_path_to_property,
        property_name,
        property_dict,
        property_type_cls_map,
    ):
        """Constructs an ObjectProperty

        Args:
            dotted_path_to_property - Javascript-like dotted path to get to the
                object which contains this property (empty string if at root)
            property_name - name of this property
            property_dict - the portion of the json schema representing this
                property
            property_type_cls_map - Maps property types to the classes that
               construct them.
        """
        super(ObjectProperty, self).__init__(
            dotted_path_to_property,
            property_name,
            property_dict,
        )

        self.property_type_cls_map = property_type_cls_map

        self._validate_object_property()

    def _validate_object_property(self):
        if get_type_from_schema(self.property_dict) != Types.OBJECT:
            raise ValueError('Unexpected schema for object property.')

        if 'propertyOrder' in self.property_dict:
            if (
                len(self.property_dict['propertyOrder']) !=
                len(self.property_dict['properties'].keys())
            ):
                raise ValueError('propertyOrder must represent all properties.')

            for property_name in self.property_dict['propertyOrder']:
                if not property_name in self.property_dict['properties']:
                    raise ValueError(
                        'propertyOrder specified a property not on this schema. '
                        'Property: %s' % property_name
                    )

    def _get_properties(self):
        properties = self.property_dict['properties']
        property_order = self.property_dict.get(
            'propertyOrder',
            properties.keys(),
        )

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
