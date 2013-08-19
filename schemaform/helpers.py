
import pyquery
import jsonschema
import jsonschema._utils

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
