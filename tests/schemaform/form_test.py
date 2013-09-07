
import jsonschema
import mock
import testify as T

from schemaform.form import Form
from schemaform.object_property import ObjectProperty
from schemaform.types import Types

class TestForm(T.TestCase):

    def test_validates_schema(self):
        with T.assert_raises(jsonschema.ValidationError):
            Form({'type': 'garbage'})

    def test_passes_on_attrs(self):
        attrs = {
            'action': 'foo.htm',
            'method': 'POST',
        }
        pq = Form(
            {'type': 'object', 'properties': {'foo': {}}},
            **attrs
        ).__pq__()

        for attr, value in attrs.iteritems():
            T.assert_equal(pq.attr(attr), value)

    def test_constructs_object_schema(self):
        ObjectProperty_mock = mock.Mock(spec=ObjectProperty)
        ObjectProperty_mock.return_value.__pq__ = mock.Mock(spec=lambda: None)
        schema = {'type': 'object', 'properties': {'foo': {}}}

        with mock.patch.object(
            Form,
            'get_property_type_cls_map',
            spec=Form.get_property_type_cls_map,
            return_value = {
                Types.OBJECT: ObjectProperty_mock,
            },
        ) as get_property_type_cls_map_mock:
            pq = Form(schema).__pq__()
            ObjectProperty_mock.assert_called_once_with(
                '', '', schema, get_property_type_cls_map_mock.return_value
            )
            T.assert_equal(pq, ObjectProperty_mock().__pq__().wrapAll())

    def test_flattened_schema(self):
        instance = Form({
            'type': 'object',
            'properties': {
                'foo': {
                    'type': 'object',
                    'properties': {'bar': {}, 'baz': {}},
                },
                'womp': {},
            }
        })
        T.assert_equal(
            instance._flattened_schema,
            {'foo.bar': {}, 'foo.baz': {}, 'womp': {}}
        )

    def test_load_data_from_form_missing_values_does_nothing(self):
        instance = Form({'type': 'object', 'properties': {'a': {}, 'b': {}}})
        T.assert_equal(instance._load_data_from_form({}), {})

    def test_load_data_from_form_missing_boolean_sets_false(self):
        instance = Form({
            'type': 'object',
            'properties': {'a': {'type': 'boolean'}},
        })
        T.assert_equal(instance._load_data_from_form({}), {'a': False})

    def test_load_data_from_form_loads_data(self):
        instance = Form({
            'type': 'object',
            'properties': {'a': {'type': 'integer'}},
        })
        T.assert_equal(instance._load_data_from_form({'a': '1'}), {'a': 1})
