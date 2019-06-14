import re

"""
Usage:
from sagas.util.str_converters import to_camel_case, to_snake_case
"""

lower_first = lambda s: s[:1].lower() + s[1:] if s else ''
cap_first = lambda s: s[:1].upper() + s[1:] if s else ''

# Adapted from this response in Stackoverflow
# http://stackoverflow.com/a/19053800/1072990
def to_camel_case(snake_str, capfirst=False):
    components = snake_str.split("_")
    # We capitalize the first letter of each component except the first one
    # with the 'capitalize' method and join them together.
    if capfirst:
        return "".join(x.capitalize() if x else "_" for x in components[:])
    return components[0] + "".join(x.capitalize() if x else "_" for x in components[1:])


# From this response in Stackoverflow
# http://stackoverflow.com/a/1176023/1072990
def to_snake_case(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

def to_words(snake_str, capfirst=False):
    components = snake_str.split("_")
    # We capitalize the first letter of each component except the first one
    # with the 'capitalize' method and join them together.
    if capfirst:
        return " ".join(x.capitalize() if x else "_" for x in components[:])
    return components[0] + " ".join(x.capitalize() if x else "_" for x in components[1:])

def to_const(string):
    return re.sub("[\W|^]+", "_", string).upper()  # noqa
