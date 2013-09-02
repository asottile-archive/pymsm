
def assert_issubclass(cls, base_cls):
    if not issubclass(cls, base_cls):
        raise AssertionError(
            'Expected %s to be a subclass of %s' % (
                cls.__name__, base_cls.__name__,
            )
        )
