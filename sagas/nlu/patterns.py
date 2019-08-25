from sagas.nlu.inspector_common import Inspector, Context

import logging
logger = logging.getLogger('inspector')

def check_item(feats, key, el, ctx):
    if key in feats:
        if isinstance(el, list) or isinstance(el, tuple):
            # print(el)
            # check 'or', so return true only requires one element to match
            for e in el:
                if e in feats[key]:
                    return True
        elif isinstance(el, Inspector):
            return el.check(key, ctx)
        else:
            return el in feats[key]
    return False


# c(domains).verb(nsubj='c_pron', obj='c_noun')
def verb_pattern_checker(domains):
    rel_feats = {x[0]: x[5] for x in domains}
    if (check_item(rel_feats, 'nsubj', 'c_pron', None) and
            check_item(rel_feats, 'obj', 'c_noun', None)):
        print('pattern: verb+nsubj(pron)+obj(noun)')

def trip_number_suffix(k):
    if k[-2]=='_' and k[-1].isdigit():
        return k[:-2]
    return k

class Patterns(object):
    _name = None
    _fields = {}  # {field: field object}

    def __init__(self, domains=None, meta=None, priority=0,  track=True):
        super(Patterns, self).__init__()
        self.domains = domains
        self.meta=meta
        self.track = track
        self.priority=priority
        # self.engine=meta['engine']

        self.funcs={'aux':self.check_args,
                    'subj':self.check_args,
                    'verb': self.execute_args_lemma,
                    'cop': self.execute_args_head,
                    'entire': self.execute_args_entire,
                    }

    def check_args(self, args, ctx, options):
        result=True
        opt_ret = check_item(self.meta, 'pos', args, ctx)
        if not opt_ret:
            result = False
        options.append('{} is {}: {}'.format('pos', args, opt_ret))
        return result

    def execute_args(self, args, ctx:Context, options, meta_key):
        result=True
        for arg in args:
            if isinstance(arg, Inspector):
                opt_ret = arg.check(ctx.meta[meta_key], ctx)
                if not opt_ret:
                    result = False
                options.append('{} is {}: {}'.format('pos', arg, opt_ret))
            else:
                raise Exception('Unsupported argument class %s'%type(arg))
        return result

    def execute_args_lemma(self, args, ctx:Context, options):
        return self.execute_args(args, ctx, options, 'lemma')

    def execute_args_head(self, args, ctx:Context, options):
        return self.execute_args(args, ctx, options, 'head')

    def execute_args_entire(self, args, ctx:Context, options):
        return self.execute_args(args, ctx, options, 'sents')

    def __getattr__(self, method):
        """Provide a dynamic access to a service method."""
        if method.startswith('_'):
            return super(Patterns, self).__getattr__(method)

        def service_method(*args, **kwargs):
            """Return the result of the check request."""
            result = True
            options = []

            ctx = Context(self.meta, self.domains)
            # the args has been checked as pos
            if self.meta is not None and len(args)>0:
                # opt_ret=check_item(self.meta, 'pos', args, ctx)
                # if not opt_ret:
                #     result = False
                # options.append('{} is {}: {}'.format('pos', args, opt_ret))
                if not self.funcs[method](args, ctx, options):
                    result=False

            # rel_feats = {x[0]: x[5] for x in self.domains}
            rel_feats=ctx.feats

            for key, value in kwargs.items():
                key=key.replace('_', ':')
                key=trip_number_suffix(key)
                if key.startswith('::'):
                    # starts with '__', likes '__engine'
                    opt_name=key[2:]
                    opt_ret=self.meta[opt_name]==value
                    if not opt_ret:
                        logger.debug('%s=%s checker fail, skip this pattern.'%(key, value))
                elif key.startswith(':'):
                    opt_ret=check_item(self.meta, key[1:], value, ctx)
                else:
                    opt_ret = check_item(rel_feats, key, value, ctx)

                if not opt_ret:
                    result = False
                options.append('{} is {}: {}'.format(key, value, opt_ret))
            if self.track:
                return "%s with %s" % (method, ', '.join(options)), result, self.priority
            else:
                return result

        return service_method

# print_not_matched=False
def print_result(rs):
    from termcolor import colored
    from sagas.conf.conf import cf

    print_not_matched=cf.is_enabled('print_not_matched')
    for r in rs:
        ok_clr='red' if r[2]==5 else 'blue'
        clr=ok_clr if r[1] else 'cyan'
        if not print_not_matched and not r[1]:
            pass
        else:
            print('%s [%s]'%(colored('✔', clr) if r[1] else '✖',
                             colored(r[0], clr)))




