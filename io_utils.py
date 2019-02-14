import errno
import os
import io

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

def write_to_file(filename, text):
    # type: (Text, Text) -> None
    """Write a text to a file."""

    with io.open(filename, 'w', encoding="utf-8") as f:
        f.write(str(text))


def read_file(filename, encoding="utf-8-sig"):
    """Read text from a file."""
    with io.open(filename, encoding=encoding) as f:
        return f.read()
                                