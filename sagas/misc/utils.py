import json
import warnings
import ruamel.yaml.error

warnings.simplefilter('ignore', ruamel.yaml.error.UnsafeLoaderWarning)

def dump(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))

#⊕ [Convert a list to a dictionary in Python - Stack Overflow](https://stackoverflow.com/questions/4576115/convert-a-list-to-a-dictionary-in-python)
def map_list(a):
    b = {a[i]: a[i+1] for i in range(0, len(a), 2)}
    return b

def to_std_dicts(value):
    """Convert nested ordered dicts to normal dicts for better comparison."""
    if isinstance(value, dict):
        return {k: to_std_dicts(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [to_std_dicts(v) for v in value]
    else:
        return value

