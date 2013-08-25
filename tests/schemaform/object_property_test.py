
import testify as T

from schemaform.form import Form
from schemaform.object_property import ObjectProperty

class TestObjectProperty(T.TestCase):

    path = 'herp.derp'
    property_name = 'harp'
    property_cls_map = Form.get_property_type_cls_map()

    def get_object_property(self, schema):
        return ObjectProperty(
            self.path,
            self.property_name,
            schema,
            self.property_cls_map,
        )

    def test_raises_on_incorrect_type(self):
        with T.assert_raises(ValueError):
            self.get_object_property({'type': 'string'})

    def test_raises_on_bad_property_order(self):
        with T.assert_raises(ValueError):
            self.get_object_property({
                'type': 'object',
                'properties': {'foo': {}, 'bar': {}},
                'propertyOrder': ['bar'],
            })

    def test_raises_with_incorrect_property_name(self):
        with T.assert_raises(ValueError):
            self.get_object_property({
                'type': 'object',
                'properties': {'foo': {}, 'bar': {}},
                'propertyOrder': ['bar', 'baz'],
            })
