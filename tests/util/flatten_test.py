
import testify as T

from util.flatten import flatten

class TestFlatten(T.TestCase):

    inputs_to_expected_outputs = (
        # Boring base case
        ([1, 2, 3], [1, 2, 3]),
        # A slightly more interesting case
        ([1, [2, 3]], [1, 2, 3]),
        # A more complicated case
        ([1, [2, [3,], [4, 5], 6]], [1, 2, 3, 4, 5, 6]),
    )

    def test_flatten(self):
        for input, expected_output in self.inputs_to_expected_outputs:
            T.assert_equal(list(flatten(input)), expected_output)

    def test_flatten_with_acceptable_iterable_type(self):
        ret = list(flatten(
            ['foo', ['bar', 'baz']],
            acceptable_iterable_type=basestring,
        ))
        T.assert_equal(ret,  ['foo', 'bar', 'baz'])

    def test_flatten_with_generator(self):
        def gen():
            yield 1
            yield 2
            yield 3

        ret = list(flatten([0, gen()]))
        T.assert_equal(ret, [0, 1, 2, 3])
