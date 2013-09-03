
import testify as T

from util.dicts import get_deep
from util.dicts import set_deep

class TestGetDeep(T.TestCase):
    sample_dict = {
        'a': {
            'b': {
                'c': 'd',
                'e': [1, 2, 3],
            },
        },
    }

    def test_get_deep_returns_none_by_default_for_missing_value(self):
        T.assert_is(get_deep({}, 'foo'), None)

    def test_get_deep_returns_dict_value_correctly(self):
        T.assert_is(
            get_deep(self.sample_dict, 'a.b'),
            self.sample_dict['a']['b'],
        )

    def test_get_deep_returns_value(self):
        T.assert_is(
            get_deep(self.sample_dict, 'a.b.c'),
            self.sample_dict['a']['b']['c'],
        )

    def test_returns_default_on_failed_key(self):
        sentient = object()
        T.assert_is(
            get_deep(self.sample_dict, 'notakey', sentient),
            sentient,
        )

    def test_returns_default_on_indexing_into_string(self):
        sentient = object()
        T.assert_is(
            get_deep(self.sample_dict, 'a.b.c.d', sentient),
            sentient,
        )

    def test_returns_default_on_indexing_into_list(self):
        sentient = object()
        T.assert_is(
            get_deep(self.sample_dict, 'a.b.e.d', sentient),
            sentient,
        )


class TestSetDeep(T.TestCase):
    def test_set_deep_simple(self):
        foo = {}
        value = 'bar'
        set_deep(foo, 'a', value)
        T.assert_is(foo['a'], value)

    def test_set_deep_deeper(self):
        foo = {}
        value = 'bar'
        set_deep(foo, 'a.b.c', value)
        T.assert_is(foo['a']['b']['c'], value)

    def test_set_deep_value_exists(self):
        foo = {
            'a': {
                'b': 'c',
            },
        }
        value = 'd'
        set_deep(foo, 'a.b', value)
        T.assert_is(foo['a']['b'], value)

if __name__ == '__main__':
    T.run()
