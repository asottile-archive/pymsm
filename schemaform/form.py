
from util.decorators import cached_property
from util.dicts import set_deep
from schemaform.boolean_property import BooleanProperty
from schemaform.radio_enum_property import RadioEnumProperty
from schemaform.helpers import flatten_schema
from schemaform.helpers import get_type_from_schema
from schemaform.helpers import el
from schemaform.helpers import transform_value
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

    @cached_property
    def _flattened_schema(self):
        return flatten_schema(self.schema)

    def _load_data_from_form(self, form):
        """For each value in our schema, we attempt to set it into values.

        Args:
            form - Dictlike
        """
        values = {}
        # For each value in our schema we'll attempt to set values
        for schema_path, schema in self._flattened_schema.iteritems():
            submitted_value = form.get(schema_path)
            # Fixes booleans, because when they are unchecked they do not send
            # a value
            if get_type_from_schema(schema) == Types.BOOLEAN:
                submitted_value = bool(submitted_value)

            if submitted_value is None:
                continue

            new_value = transform_value(submitted_value, schema)
            set_deep(values, schema_path, new_value)

        return values

    def _validate_iterative(self, values):
        errors = {}
        return errors

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

        values = self._load_data_from_form(form)
        errors = self._validate_iterative(values)
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

