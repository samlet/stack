from typing import Text

def resource_path(file_name) -> Text:
    """
    >>> from sagas.conf import resource_path
    >>> resource_path('sagas_conf.json')

    :param file_name:
    :return:
    """
    import pkg_resources
    return pkg_resources.resource_filename(__name__, file_name)

def resource_json(file_name):
    import json_utils
    return json_utils.read_json_file(resource_path(file_name))

def resource_dir(fn_match):
    """
    >>> from sagas.conf import resource_dir
    >>> from fnmatch import fnmatch
    >>> resource_dir(lambda f: fnmatch(f, 'mod_*.json'))

    :param fn_match:
    :return:
    """
    from pkg_resources import resource_listdir
    rs=[]
    for file in resource_listdir(__name__, ''):
        if fn_match(file):
            rs.append(file)
    return rs

def resource_files(pat):
    """
    >>> from sagas.conf import resource_files, resource_path
    >>> mod_files=[resource_path(f) for f in resource_files('mod_*.json')]

    :param pat:
    :return:
    """
    from fnmatch import fnmatch
    return resource_dir(lambda f: fnmatch(f, pat))

