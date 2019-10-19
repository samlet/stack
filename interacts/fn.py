from inspect import getfullargspec, isfunction

NONE = object()  # use to signal the absence of a default


def fa_e(**ann):
    def annotate(f):
        f.__annotations__ = ann
        return f

    return annotate


class pairs(object):
    def __init__(self, **kwargs):
        self.vars = kwargs


def def_act(**kwargs):
    def runner():
        print('.................')
        for k, v in kwargs.items():
            print(k, v)

    return runner


@fa_e(
    patterns_loc=("Path to gazetteer", "positional", None, str),
    text_loc=("Path to Reddit corpus file", "positional", None, str),
    n=("Number of texts to read", "option", "n", int),
    lang=("Language class to initialise", "option", "l", str),
    lang_ex=("Language extension to initialise", "option", def_act(x=1), pairs(value=18)),
)
def fun_e(patterns_loc, text_loc, n, lang, lang_ex='...'):
    print(f".. (in fn) loc: {patterns_loc}, text: {text_loc}, n: {n}, lang: {lang}, ex: {lang_ex}")
    # print(kwargs)


def fparse(obj):
    f = getfullargspec(obj)
    defaults = f.defaults or ()
    n_args = len(f.args)
    n_defaults = len(defaults)
    alldefaults = (NONE,) * (n_args - n_defaults) + defaults
    # func = obj
    print('..', obj.__name__)
    for name, default in zip(f.args, alldefaults):
        ann = f.annotations.get(name, ())
        print(ann, 'default->', type(default))
        if isfunction(ann[2]):
            print('\t.. callable')
            ann[2]()


def fcall(obj):
    f = getfullargspec(obj)

    # call function
    extraopts = []
    if f.varkw:
        kwargs = f.varkw
    else:
        kwargs = {}
    print('-' * 10)
    print('**', f.args, kwargs)
    obj(*(f.args + extraopts), **kwargs)

class FnCli(object):
    def tests(self):
        """
        $ python -m interacts.fn tests
        :return:
        """
        print('@ parse @')
        fparse(fun_e)
        print('@ call @')
        fcall(fun_e)

if __name__ == '__main__':
    import fire
    fire.Fire(FnCli)

