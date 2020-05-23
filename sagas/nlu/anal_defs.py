terms_list=['ent', 'srv', 'fld', 'ref', 'typ',
            'loc']

def make_registrar():
    registry = {}
    def registrar(func):
        fname=func.__name__
        if fname.startswith('_'):
            fname=fname[1:]
        registry[fname] = func
        return func  # normally a decorator returns a wrapped function,
                     # but here we return func unmodified, after registering it
    registrar.all = registry
    return registrar

vtable = make_registrar()

