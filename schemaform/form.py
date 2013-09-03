
from util.dicts import flatten
from util.dicts import get_deep
from util.dicts import set_deep
from schemaform.boolean_property import BooleanProperty
from schemaform.radio_enum_property import RadioEnumProperty
from schemaform.helpers import get_type_from_schema
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

    def load_from_form(self, form, tolerate_extra_keys=True):
        """Loads data from a form (or dictlike).

        The form should be like one you would get from a POST of the result of
        the __pq__ method.  Where the keys are paths (like 'foo.bar') and
        the values are the values.

        Returns:
            values, errors
            values - The dictionary retrieved from the processing of form
            errors - Any errors encountered while loading.

        Args:
            form - dictlike object where keys are paths like 'foo.bar'
            tolerate_extra_keys - Whether to allow stuff not in the schema
        """

        values = {}
        errors = {}

        for key, value in form.iteritems():
            value_schema = get_deep(self.schema, key)
            if not value_schema and not tolerate_extra_keys:
                errors[key] = 'Unexpected key'
            else:
                # TODO:
                # try:
                #     new_value = transform_value(value, value_schema)
                #     jsonschema.validate(new_value, value_schema)
                #     set_deep(values, key, new_value)
                # except jsonschema.ValidationError:
                #     errors[key] = 'Validation Error'
                pass

        # TODO: split this into another function
        # This oddness is because checkboxes pass no value if unchecked in forms
        # So we need to iterate through all of the boolean schemas in this
        # schema and if they are unset, we need to set them to False
        for sub_schema_path, sub_schema in flatten(self.schema):
            if (
                get_type_from_schema(sub_schema) == Types.BOOLEAN and
                get_deep(values, sub_schema_path) is None
            ):
                set_deep(values, sub_schema_path, False)

        # TODO: I think there's an iterative version of the following:
        # jsonschema.validate(values, self.schema)

        return values, errors

    def __pq__(self):
        """Returns the pyquery representation of this object."""
        contents = self.get_property_type_cls_map()[Types.OBJECT](
            '',
            '',
            self.schema,
            self.get_property_type_cls_map()
        ).__pq__()
        return contents.wrapAll(el('form', **self.form_attrs).__html__())

