
import collections
import itertools
import pyquery
import jsonschema
import jsonschema._utils

from schemaform.types import Types
from util.flatten import flatten

def el(element_name, **attrs):
    """Constructs a pyquery element.

    Args:
        element_name - element name such as div
        text - kwarg only.  Text for element
        classname - kwarg only.  Class to set on element
        **attrs - attributes to set
    """
    text = attrs.pop('text', '')
    classname = attrs.pop('classname', '')

    element = pyquery.PyQuery('<%s>' % element_name)
    if text:
        element.text(text)
    if classname:
        element.attr('class', classname)
    if attrs:
        element.attr(**attrs)
    return element

draft4_schema = jsonschema._utils.load_schema('draft4')

def validate_schema_against_draft4(schema):
    jsonschema.validate(schema, draft4_schema)

NO_VALUE = object()

def validate_default_value(schema):
    """Validates that the default value conforms to itself."""
    if schema.get('default', NO_VALUE) is not NO_VALUE:
        jsonschema.validate(schema['default'], schema)

def validate_enum_values(schema):
    """Validates the possible values in the enum conform to itself."""
    if 'enum' in schema:
        for value in schema['enum']:
            jsonschema.validate(value, schema)

def get_type_from_schema(schema):
    """Returns the type from the schema."""
    if 'enum' in schema:
        return Types.ENUM

    return schema.get('type', Types.STRING)

def combine_pqables(*args, **kwargs):
    """Combines pyquery object or objects which implement __pq__ into a single
    pyquery object.

    Args:
        *args - Positional arguments will be converted flattened
        acceptable_iterable_type - Optional list of additionally allowable
            iterable types (for example: to exclude a specific namedtuple)
    """
    additional_acceptable_iterable_type = kwargs.pop(
        'acceptable_iterable_type', []
    )
    # Don't expect any other kwargs
    assert not kwargs
    # needs to be a tuple because this is passed to isinstance
    acceptable_iterable_type = tuple(
        [pyquery.PyQuery] + (
            # This allows both type and iterable of type to be passed in
            list(additional_acceptable_iterable_type)
            if isinstance(additional_acceptable_iterable_type, collections.Iterable)
            else [additional_acceptable_iterable_type]
        )
    )

    to_pyquery = (
        obj if isinstance(obj, pyquery.PyQuery) else obj.__pq__()
        for obj in flatten(
            args,
            acceptable_iterable_type=acceptable_iterable_type,
        )
    )
    return pyquery.PyQuery(list(itertools.chain(*to_pyquery)))
