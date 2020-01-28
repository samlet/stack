import errno
import os
import io

def exists(file):
    """
    Check file or director whether exists; other related methods:
        os.path.isfile()
        os.path.isdir()
    :param file:
    :return:
    """
    from os import path
    return path.exists(file)

def create_dir(dir_path):
    # type: (Text) -> None
    """Creates a directory and its super paths.

    Succeeds even if the path already exists."""

    try:
        os.makedirs(dir_path)
    except OSError as e:
        # be happy if someone already created the path
        if e.errno != errno.EEXIST:
            raise


def create_dir_for_file(file_path):
    # type: (Text) -> None
    """Creates any missing parent directories of this files path."""

    try:
        os.makedirs(os.path.dirname(file_path))
    except OSError as e:
        # be happy if someone already created the path
        if e.errno != errno.EEXIST:
            raise

def list_directory(path):
    # type: (Text) -> List[Text]
    """Returns all files and folders excluding hidden files.

    If the path points to a file, returns the file. This is a recursive
    implementation returning files in any depth of the path."""

    import six
    if not isinstance(path, six.string_types):
        raise ValueError("Resourcename must be a string type")

    if os.path.isfile(path):
        return [path]
    elif os.path.isdir(path):
        results = []
        for base, dirs, files in os.walk(path):
            # remove hidden files
            goodfiles = filter(lambda x: not x.startswith('.'), files)
            results.extend(os.path.join(base, f) for f in goodfiles)
        return results
    else:
        raise ValueError("Could not locate the resource '{}'."
                         "".format(os.path.abspath(path)))


def list_files(path):
    # type: (Text) -> List[Text]
    """Returns all files excluding hidden files.

    If the path points to a file, returns the file."""

    return [fn for fn in list_directory(path) if os.path.isfile(fn)]


def list_subdirectories(path):
    # type: (Text) -> List[Text]
    """Returns all folders excluding hidden files.

    If the path points to a file, returns an empty list."""

    import glob
    return [fn
            for fn in glob.glob(os.path.join(path, '*'))
            if os.path.isdir(fn)]

def write_to_file(filename, text, auto_create_dir=False):
    # type: (Text, Text) -> None
    """Write a text to a file."""
    if auto_create_dir:
        create_dir_for_file(filename)

    with io.open(filename, 'w', encoding="utf-8") as f:
        f.write(str(text))


def read_file(filename, encoding="utf-8-sig"):
    """Read text from a file."""
    with io.open(filename, encoding=encoding) as f:
        return f.read()

def remove_dir(target_dir):
    import shutil
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

def lines(filename):
    with open(filename) as f:
        lines = f.readlines()
        return lines

def list_with_suffix(dir, suffix):
    import os
    rs=[]
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(suffix):
                rs.append(os.path.join(root, file))
    return rs

def list_match(dir, pat):
    """
    >>> io_utils.list_match('.', 'mod_*.json')
    :param dir:
    :param pat:
    :return:
    """
    import os
    from fnmatch import fnmatch
    rs=[]
    for root, dirs, files in os.walk(dir):
        for file in files:
            if fnmatch(file, pat):
                rs.append(os.path.join(root, file))
    return rs

def list_files_with_basename(dir_pattern):
    import glob
    import ntpath
    files = glob.glob(dir_pattern)
    bases = []
    for f in files:
        bases.append(ntpath.basename(f))
    return bases

