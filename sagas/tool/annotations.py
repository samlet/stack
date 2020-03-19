class lazy_property(object):
    """A @property that is only evaluated once.
    >>> @lazy_property
    >>> def receiver_connected(self):
    >>>    return Signal(doc="Emitted after a receiver connects.")
    """

    def __init__(self, deferred):
        self._deferred = deferred
        self.__doc__ = deferred.__doc__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = self._deferred(obj)
        setattr(obj, self._deferred.__name__, value)
        return value

