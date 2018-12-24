import json
import warnings
import ruamel.yaml.error

warnings.simplefilter('ignore', ruamel.yaml.error.UnsafeLoaderWarning)

def dump(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    