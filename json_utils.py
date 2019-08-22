import os
import json
import simplejson
from io_utils import read_file, write_to_file

## dumped = json_to_string({"ok": 'JSON posted'})
def json_to_string(obj, **kwargs):
    indent = kwargs.pop("indent", 2)
    ensure_ascii = kwargs.pop("ensure_ascii", False)
    return json.dumps(obj, indent=indent, ensure_ascii=ensure_ascii, **kwargs)

def read_json_file(filename):
    """Read json from a file."""
    content = read_file(filename)
    try:
        return simplejson.loads(content)
    except ValueError as e:
        raise ValueError("Failed to read json from '{}'. Error: "
                         "{}".format(os.path.abspath(filename), e))

def write_json_to_file(filename, obj, **kwargs):
    # type: (Text, Any) -> None
    """Write an object as a json string to a file."""

    write_to_file(filename, json_to_string(obj, **kwargs))

def json_object(obj):
    return json.dumps(obj, default=lambda o: o.__dict__,
               sort_keys=True, indent=4)

write_json=lambda f,o: write_json_to_file(f,o)
pretty_json=lambda o: json.dumps(o, indent=2, ensure_ascii=False)
