from base64 import b64encode as _base64, b64decode as _unbase64
from six import string_types

join_args=lambda args: ' '.join([str(arg[0]) if isinstance(arg, tuple) else arg for arg in args])

def base64(s):
    return _base64(s.encode('utf-8')).decode('utf-8')

def unbase64(s):
    return _unbase64(s).decode('utf-8')

def is_str(s):
    return isinstance(s, string_types)

def abbrev(data, l=15):
    if data is None:
        return ""

    info = (data[:l] + '..') if len(data) > l else data
    return info

