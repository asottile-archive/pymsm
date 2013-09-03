
import testify as T

from util.dicts import get_deep

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
