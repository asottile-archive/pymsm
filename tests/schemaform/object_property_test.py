
import itertools
import pyquery
import testify as T

from schemaform.form import Form
from schemaform.object_property import ObjectProperty
from util.auto_namedtuple import auto_namedtuple

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

    def get_object_property_pq(self, schema):
        object_property = self.get_object_property(schema)
        fieldset = object_property.__pq__()
        legend = [pyquery.PyQuery(el) for el in fieldset.children('legend')]
        labels = [pyquery.PyQuery(el) for el in fieldset.children('label')]
        others = [
            pyquery.PyQuery(el)
            for el in fieldset.children('*:not(legend):not(label)')
        ]
        return auto_namedtuple(
            fieldset=fieldset,
            legend=legend,
            labels=labels,
            others=others,
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

    def test_raises_with_empty_object(self):
        with T.assert_raises(ValueError):
            self.get_object_property({'type': 'object', 'properties': {}})

    def test_property_order(self):
        property_order = ['bar', 'foo']
        ret = self.get_object_property_pq({
            'type': 'object',
            'properties': {'foo': {}, 'bar': {}},
            'propertyOrder': property_order,
        })
        for label, property in itertools.izip(ret.labels, property_order):
            T.assert_equal(label.text(), property.title())

    def test_property_order_not_specified(self):
        properties = {'foo': {}, 'bar': {}}
        ret = self.get_object_property_pq({
            'type': 'object',
            'properties': properties,
        })
        for label, property in itertools.izip(ret.labels, properties.keys()):
            T.assert_equal(label.text(), property.title())

    def test_nested_object(self):
        ret = self.get_object_property_pq({
            'type': 'object',
            'properties': {
                'foo': {
                    'type': 'object',
                    'properties': {'bar': {}},
                },
            },
        })
        T.assert_equal(ret.others[0].find('legend').text(), 'Foo')
