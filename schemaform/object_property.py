
from schemaform.base_property import BaseProperty
from schemaform.helpers import combine_pqables
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

        if not self.property_dict.get('properties'):
            raise ValueError('An object must specify at least one property.')

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

        base_path = [self.get_input_name()]
        for property_name in property_order:
            property = properties[property_name]
            property_type = get_type_from_schema(property)
            args = base_path + [property_name, property]

            # Objects are a special snowflake and need this map
            if property_type == Types.OBJECT:
                args += [self.property_type_cls_map]

            yield self.property_type_cls_map[property_type](*args)

    def __pq__(self):
        """Returns the pyquery object representing this object."""
        contents = combine_pqables(
            el('legend', text=self.get_label_text()),
            self._get_properties()
        )
        return contents.wrapAll(el('fieldset').__html__())
