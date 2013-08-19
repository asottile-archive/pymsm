
from schemaform.boolean_property import BooleanProperty
from schemaform.helpers import validate_schema_against_draft4
from schemaform.single_input_property import SingleInputProperty

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
            'boolean': BooleanProperty,
            'integer': SingleInputProperty,
            'number': SingleInputProperty,
            'string': SingleInputProperty,
            # 'enum': EnumProperty,
            # 'object': ObjectProperty,
        }
