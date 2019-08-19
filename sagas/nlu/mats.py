class Cats(object):
    def __init__(self, name):
        self.name = name
        self.mats = []

    def __str__(self):
        return self.name


class Mats(object):
    _name = None
    _fields = {}  # {field: field object}

    def __init__(self, cat):
        cat.mats.append(self)
        self.cat = cat
        self.cnt = []

    def __getattr__(self, method):
        """Provide a dynamic access to a service method."""
        if method.startswith('_'):
            return super(Mats, self).__getattr__(method)

        def service_method(*args, **kwargs):
            print(f"{self.cat}.{method}")
            for key, value in kwargs.items():
                print('\t', key, value)

            self.cnt.append({'type': method, 'items': kwargs})
            return self

        return service_method

