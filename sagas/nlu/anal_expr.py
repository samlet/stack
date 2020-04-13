from typing import Text, Any, Dict, List, Union, Optional, Tuple, Iterable
from sagas.nlu.anal_data_types import behave_, desc_, phrase_, rel_, path_, _, Carrier


class NoDefaultType:
    pass
NoDefault = NoDefaultType()

class MatchError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class BoxedArgs:
    def __init__(self, obj):
        self.obj = obj

    def get(self):
        return self.obj

def pairwise(l):
    i = 0
    while i < len(l):
        yield l[i], l[i + 1]
        i += 2

def get_lambda_args_error_msg(action, var, err):
    import inspect
    try:
        code = inspect.getsource(action)
        return "Error passing arguments %s here:\n%s\n%s" % (var, code, err)
    except OSError:
        return "Error passing arguments %s:\n%s" % (var, err)

def run(action, var):
    if callable(action):
        if isinstance(var, Iterable):
            try:
                return action(*var)
            except TypeError as err:
                raise MatchError(get_lambda_args_error_msg(action, var, err))
        elif isinstance(var, BoxedArgs):
            return action(var.get())
        else:
            return action(var)
    else:
        return action

def match(var, *args, default=NoDefault, strict=True):
    if len(args) % 2 != 0:
        raise MatchError("Every guard must have an action.")

    if default is NoDefault and strict is False:
        default = False

    pairs = list(pairwise(args))
    patterns = [patt for (patt, action) in pairs]

    for patt, action in pairs:
        matched_as_value, args = match_value(patt, var)

        if matched_as_value:
            lambda_args = args if len(args) > 0 else BoxedArgs(var)
            Carrier.clean_all_reqs()  # clear all carrier
            return run(action, lambda_args)

    Carrier.clean_all_reqs()  # clear all carrier

    if default is NoDefault:
        if _ not in patterns:
            raise MatchError("'_' not provided. This case is not handled:\n%s" % str(var))
    else:
        return default

def match_value(pattern, value) -> Tuple[bool, List]:
    result, data= value.do_match(pattern)
    args=[x for x in data] if isinstance(data, List) or isinstance(data, Tuple) else [data]
    args.extend(Carrier.availables())
    Carrier.clean_all_resp()
    return result, args




