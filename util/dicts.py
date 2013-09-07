
from util.iter import truthy

def get_deep(dictlike, path, default=None):
    """Retrieves deeply into a dict.

    For instance get_deep(dicta, 'a.b') is roughly equivalent to dicta['a']['b']

    Args:
        dictlike - Dictionary
        path - Dotted path to elements
        default - Default value if not found (defaults to None)
    """
    path_parts = path.split('.')

    try:
        for path_part in path_parts:
            dictlike = dictlike[path_part]
    except (KeyError, TypeError):
        dictlike = default

    return dictlike

def set_deep(dictlike, path, value):
    """Sets deeply into a dict.

    for insance set_deep(dicta, 'a.b', 'foo') is rougly equivalent to
    dicta['a']['b'] = 'foo'

    Args:
        dictlike - Dictionary
        path - Dotted path to element
        value - Value to set
    """
    path_parts = path.split('.')

    for path_part in path_parts[:-1]:
        try:
            dictlike = dictlike[path_part]
        except KeyError:
            dictlike[path_part] = dict()
            dictlike = dictlike[path_part]

    dictlike[path_parts[-1]] = value


def _flatten_helper(dict, path, outdict):
    try:
        for key, value in dict.iteritems():
            _flatten_helper(
                value,
                # This oddness prevents the leading '.' for keys
                # For example (without this):
                # {'.a.b': 'c'} from {'a': {'b': 'c'}}
                '.'.join(truthy([path, key])),
                outdict,
            )
    except AttributeError:
        outdict[path] = dict

def flatten(dict):
    outdict = {}
    _flatten_helper(dict, '', outdict)
    return outdict
