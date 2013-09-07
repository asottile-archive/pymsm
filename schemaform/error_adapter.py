
import collections
import re

from util.iter import truthy

REQUIRED_VALIDATOR = 'required'
REQUIRED_RE = re.compile("^'(.+)' is a required property$")

class ErrorAdapter(collections.namedtuple(
    'ErrorAdapter',
    ['dotted_path', 'message'],
)):
    """An ErrorAdapter adapts a ValidationError into a form that is useful for
    generating an errors dict in schemaform.form.Form
    """

    @classmethod
    def from_validation_error(cls, validation_error):
        dotted_path = '.'.join(validation_error.path)
        message = validation_error.message
        # Currently I only know of the 'required' validation error being a
        # special snowflake
        if validation_error.validator == REQUIRED_VALIDATOR:
            dotted_path = '.'.join(truthy([
                dotted_path,
                REQUIRED_RE.match(message).group(1),
            ]))

        return cls(dotted_path, message)
