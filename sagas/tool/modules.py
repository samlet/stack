def add_path(path):
    import sys
    sys.path.append(path)

def reload(x):
    # imp.reload won't work for the from m import X case?
    # if X is not a module, you can
    from importlib import reload  # Python 3.4+ only.
    import sys
    reload(sys.modules[x.__module__])

