
import markupsafe

from schemaform.boolean_property import BooleanProperty
from schemaform.radio_enum_property import RadioEnumProperty
from schemaform.helpers import el
from schemaform.helpers import validate_schema_against_draft4
from schemaform.object_property import ObjectProperty
from schemaform.single_input_property import SingleInputProperty
from schemaform.types import Types

class Form(object):
    """The main object of the schemaform package.  A Form encapsulates how a
    schema is translated into both html and a form response validator.
    """

    def __init__(self, schema, **form_attrs):
        """Construct a Form.

        Args:
            schema - json schema for the form.
            **form_attrs - attributes passed to construction of the form element
        """
        validate_schema_against_draft4(schema)
        self.schema = schema
        self.form_attrs = form_attrs

    @classmethod
    def get_property_type_cls_map(cls):
        """Override if you want to change the behavior."""
        return {
            Types.BOOLEAN: BooleanProperty,
            Types.INTEGER: SingleInputProperty,
            Types.NUMBER: SingleInputProperty,
            Types.STRING: SingleInputProperty,
            Types.ENUM: RadioEnumProperty,
            Types.OBJECT: ObjectProperty,
        }

    def __pq__(self):
        """Returns the pyquery representation of this object."""
        contents = self.get_property_type_cls_map()[Types.OBJECT](
            '',
            '',
            self.schema,
            self.get_property_type_cls_map()
        ).__pq__()
        return contents.wrapAll(el('form', **self.form_attrs).__html__())

    @property
    def markup(self):
        """Returns blessed string of markup."""
        # At this point we trust our stuff.
        return markupsafe.Markup(self.__pq__().__html__())
