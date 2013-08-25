
import collections

def flatten(iterable, acceptable_iterable_type=type(None)):
    """Flattens an iterable.

    Args:
        iterable - Some iterable.
        acceptable_iterable_type - An iterable type that won't be flattened
            such as basestring or pyquery.PyQuery.
    """
    for element in iterable:
        if (
            isinstance(element, collections.Iterable) and
            not isinstance(element, acceptable_iterable_type)
        ):
            for sub in flatten(
                element,
                acceptable_iterable_type=acceptable_iterable_type,
            ):
                yield sub
        else:
            yield element

