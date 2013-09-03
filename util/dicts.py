
def get_deep(value, path, default=None):
    path_parts = path.split('.')

    try:
        for path_part in path_parts:
            value = value[path_part]
    except (KeyError, TypeError):
        value = default

    return value

