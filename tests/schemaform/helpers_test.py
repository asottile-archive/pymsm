
import collections
import pyquery
import jsonschema
import testify as T

from schemaform.helpers import combine_pqables
from schemaform.helpers import el
from schemaform.helpers import get_type_from_schema
from schemaform.helpers import validate_default_value
from schemaform.helpers import validate_enum_values
from schemaform.helpers import validate_schema_against_draft4

class TestEl(T.TestCase):
    """Some basic tests for the element helper."""

    def assert_is_pyquery(self, element):
        T.assert_isinstance(element, pyquery.PyQuery)

    def test_base_case(self):
        element = el('div')
        self.assert_is_pyquery(element)
        T.assert_equal(element.__html__(), '<div></div>')

    def test_classname(self):
        classname = 'herp fwerp'
        element = el('div', classname=classname)
        T.assert_equal(element.attr('class'), classname)

    def test_attrs(self):
        attrs = {
            'herp': 'derp',
            'id': 'foo',
        }
        element = el('div', **attrs)
        for attr, value in attrs.iteritems():
            T.assert_equal(element.attr(attr), value)

class TestSmokeValidateSchemaAgainstDraft4(T.TestCase):

    # XXX: admittedly these are kind of crappy smoke tests

    def test_failing_schema(self):
        with T.assert_raises(jsonschema.ValidationError):
            validate_schema_against_draft4({'type': 'not_a_real_type'})

    def test_passing_schema(self):
        validate_schema_against_draft4({'type': 'object'})

class TestValidateDefaultValue(T.TestCase):
    """Tests the validate_default_value function."""

    def test_valid_default_value(self):
        validate_default_value({'type': 'string', 'default': 'herp'})

    def test_no_default_value_specified(self):
        validate_default_value({})

    def test_none_as_default_value(self):
        with T.assert_raises(jsonschema.ValidationError):
            validate_default_value({'type': 'string', 'default': None})

    def test_wrong_type(self):
        with T.assert_raises(jsonschema.ValidationError):
            validate_default_value({'type': 'integer', 'default': 4.5})

    def test_not_in_enum(self):
        with T.assert_raises(jsonschema.ValidationError):
            validate_default_value({
                'type': 'integer',
                'enum': [1, 2, 3],
                'default': 4,
            })

class TestValidateEnumValues(T.TestCase):

    def test_not_an_enum(self):
        validate_enum_values({'type': 'string'})

    def test_valid_enum(self):
        validate_enum_values({'type': 'integer', 'enum': [1, 2, 3]})

    def test_invalid_enum(self):
        with T.assert_raises(jsonschema.ValidationError):
            validate_enum_values({'type': 'integer', 'enum': [1, 2.5, 3]})

class TestGetTypeFromschema(T.TestCase):

    def test_get_type_from_schema_enum(self):
        schema_type = get_type_from_schema({'enum': ['a', 'b', 'c']})
        T.assert_equal(schema_type, 'enum')

    def test_get_type_from_schema_not_specified(self):
        schema_type = get_type_from_schema({})
        T.assert_equal(schema_type, 'string')

    def test_get_type_from_schema_specified(self):
        schema_type = get_type_from_schema({'type': 'foo'})
        T.assert_equal(schema_type, 'foo')


class TestCombinePqableObjects(T.TestCase):
    class Pqable(object):
        def __pq__(self):
            return el('div', text='pqable')

    class IterablePqable(collections.namedtuple('Foo', ['bar'])):
        def __pq__(self):
            return el('div', text=self.bar)

    class IterablePqable2(collections.namedtuple('Bar', ['baz'])):
        def __pq__(self):
            return el('div', text=self.baz)

    def test_combine_pqables(self):
        ret = combine_pqables(
            pyquery.PyQuery('<div>'),
            [pyquery.PyQuery('<div>'), pyquery.PyQuery('<span>')],
            self.Pqable(),
            [self.Pqable(), self.Pqable()],
        )
        T.assert_equal(
            ret.__html__(),
            pyquery.PyQuery(
                '<div/><div/><span/><div>pqable</div><div>pqable</div><div>pqable</div>',
                parser='html_fragments',
            ).__html__(),
        )

    def test_combine_pqable_objects_with_acceptable_iterable_type(self):
        ret = combine_pqables(
            self.IterablePqable('foo'),
            acceptable_iterable_type=self.IterablePqable
        )
        T.assert_equal(ret.__html__(), '<div>foo</div>')

    def test_combine_pqable_objects_with_acceptable_iterable_types(self):
        ret = combine_pqables(
            self.IterablePqable('foo'),
            self.IterablePqable2('baz'),
            acceptable_iterable_type=[
                self.IterablePqable,
                self.IterablePqable2,
            ],
        )
        T.assert_equal(ret.__html__(), '<div>foo</div><div>baz</div>')
