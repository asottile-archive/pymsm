import testify as T

from util.natural_sort import natural_sort

class TestNaturalSort(T.TestCase):
    expected = [
        (
            ['1.6', '1.0.3', '1.1', '1.0', '1.2a'],
            ['1.0', '1.0.3', '1.1', '1.2a', '1.6'],
        ),
        (
            ['booklet', '4 sheets', '48 sheets', '12 sheets'],
            ['4 sheets', '12 sheets', '48 sheets', 'booklet'],
        ),
        (
            ['1', '2', '3', 'a', 'b', 'c'],
            ['1', '2', '3', 'a', 'b', 'c'],
        ),
        (
            ['c', 'b', 'a', '3', '2', '1'],
            ['1', '2', '3', 'a', 'b', 'c'],
        ),
    ]

    def test_natural_sort(self):
        for input, output in self.expected:
            T.assert_equal(output, natural_sort(input))

if __name__ == '__main__':
    T.run()

