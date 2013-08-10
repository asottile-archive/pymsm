import re

def natural_sort(l):
    """Natural sort the given iterable.

    Args:
        l - An iterable (usually a list)

    Example:

    natural_sort(['b', '4 s', '40 s', '12 s'])
    ==> ['4 s', '12 s', '40 s', 'b']

    Or a more relevant example:
    natural_sort(['1.6', '1.0.3', '1.1', '1.0'])
    ==> ['1.0', '1.0.3', '1.1', '1.6']

    http://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [
        convert(c) for c in re.split('([0-9]+)', key)
    ]
    return sorted(l, key=alphanum_key)
