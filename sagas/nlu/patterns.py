from typing import Text, Any, Dict, List, Union
from sagas.nlu.inspector_common import Inspector, Context
import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)

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
    if len(k)==1:
        return k
    if k[-2]=='_' and k[-1].isdigit():
        return k[:-2]
    return k

class Patterns(object):
    # _name = None
    _fields = {}  # {field: field object}

    def __init__(self, domains=None, meta=None, priority=0, track=True, name='', doc=None):
        super(Patterns, self).__init__()
        self.domains = domains
        self.meta=meta
        self.track = track
        self.priority=priority
        self.name=name
        self.doc=doc

        # self.engine=meta['engine']

        self.funcs={'aux':self.check_args,
                    'subj':self.check_args,
                    'verb': self.execute_args_word,
                    'cop': self.execute_args_head,
                    'entire': self.execute_args_entire,
                    'root': self.execute_args_word,
                    }
        self.after_evs=[]

    def check_args(self, args, ctx, options):
        result=True
        opt_ret = check_item(self.meta, 'pos', args, ctx)
        if not opt_ret:
            result = False
        options.append('{} is {}: {}'.format('pos', args, opt_ret))
        return result

    def execute_args(self, args, ctx:Context, options, meta_key:Union[Text, List[Text]]):
        result=True
        for arg in args:
            if isinstance(arg, Inspector):
                if isinstance(meta_key, list):
                    key_val='/'.join([ctx.meta[k] for k in meta_key])
                else:
                    key_val=ctx.meta[meta_key] if meta_key in ctx.meta else ''

                if arg.after:
                    self.after_evs.append((arg, key_val))
                else:
                    opt_ret = arg.check(key_val, ctx)
                    # 这样的写法是希望当result=False之后, 不再被True值置换,
                    # 也就是说一旦result=False之后, 就一直保持False值
                    if not opt_ret:
                        result = False
                    options.append('{} is {}: {}'.format('pos', arg, opt_ret))
            elif callable(arg):
                opt_ret=arg(self.doc, self.meta)
                if not opt_ret:
                    result = False
                options.append(f"{arg.__name__} is {opt_ret}")
            else:
                raise Exception('Unsupported argument class %s'%type(arg))
        return result

    def execute_args_lemma(self, args, ctx:Context, options):
        return self.execute_args(args, ctx, options, 'lemma')

    def execute_args_word(self, args, ctx:Context, options):
        return self.execute_args(args, ctx, options, ['word', 'lemma'])

    def execute_args_head(self, args, ctx:Context, options):
        return self.execute_args(args, ctx, options=options, meta_key='head')

    def execute_args_entire(self, args, ctx:Context, options):
        return self.execute_args(args, ctx, options, 'sents')

    def prepare(self, method):
        """Provide a dynamic access to a service method."""
        if method.startswith('_'):
            return super(Patterns, self).__getattr__(method)

        def service_method(*args, **kwargs):
            """Return the result of the check request."""
            result = True
            options = []

            ctx = Context(self.meta, self.domains, name=self.name)
            # the args has been checked as pos
            if self.meta is not None and len(args) > 0:
                # opt_ret=check_item(self.meta, 'pos', args, ctx)
                # if not opt_ret:
                #     result = False
                # options.append('{} is {}: {}'.format('pos', args, opt_ret))
                if not self.funcs[method](args, ctx, options):
                    result = False

            # rel_feats = {x[0]: x[5] for x in self.domains}
            rel_feats = ctx.feats

            for key, value in kwargs.items():
                if not key.startswith('head_'):
                    key = key.replace('_', ':')
                key = trip_number_suffix(key)
                if key.startswith('::'):
                    # starts with '__', likes '__engine'
                    opt_name = key[2:]
                    opt_ret = self.meta[opt_name] == value
                    if not opt_ret:
                        logger.debug('%s=%s checker fail, skip this pattern.' % (key, value))
                elif key.startswith(':'):
                    opt_ret = check_item(self.meta, key[1:], value, ctx)
                else:
                    opt_ret = check_item(rel_feats, key, value, ctx)

                if not opt_ret:
                    result = False
                options.append('{} is {}: {}'.format(key, value, opt_ret))

            if len(self.after_evs) > 0:
                logger.debug(f".. after_evs {[(el[0].name(), el[1]) for el in self.after_evs]}")
                for arg, key_val in self.after_evs:
                    opt_ret = arg.check(key_val, ctx)
                    # 这样的写法是希望当result=False之后, 不再被True值置换,
                    # 也就是说一旦result=False之后, 就一直保持False值
                    if not opt_ret:
                        result = False
                    options.append('{} is {}: {}'.format('pos', arg, opt_ret))

                self.after_evs.clear()

            if self.track:
                return "%s with %s" % (method, ', '.join(options)), \
                       result, \
                       self.priority, \
                       ctx
            else:
                return result, ctx

        return service_method

    def __getattr__(self, method):
        return self.prepare(method)

# print_not_matched=False
def print_result(rs):
    # from termcolor import colored
    from sagas.conf.conf import cf
    from pprint import pprint
    # from sagas.tool.misc import color_print

    print_not_matched=cf.is_enabled('print_not_matched')
    print_detail=cf.is_enabled('print_detail')

    # print(f'.. print_not_matched: {print_not_matched}')
    for r in rs:
        priority=r[2]
        ok_clr='red' if abs(priority)==5 else 'blue'
        clr=ok_clr if r[1] else 'yellow'

        if priority>-1 and not print_not_matched and not r[1]:
            pass
        else:
            # tc.info('%s [%s]'%(colored('✔', clr) if r[1] else '✖',
            #                 colored(r[0], clr)))
            pat_name='' if r[3].name=='' else f"({r[3].name}) "
            tc.emp(clr, '✔' if r[1] else '✖', f"{pat_name}{r[0]}")  # r[0] is info

    if cf.is_enabled('print_inspector_result'):
        # results = [el for r in rs for el in r[3].results]
        results = [el for r in rs for el in r[3].results if r[1]] # r[1] is true/false
        if len(results) > 0:
            # .. results
            # ('ins_rasa', 'vob', {'intent': 'how_many', 'confidence': 0.9721028208732605})
            tc.emp('green', f'.. results {len(results)}')
            # tc.info([f"{r[0]}/{r[1]}/{r[2]}" for r in results])
            tc.emp('yellow', {f"{r['inspector']}/{r['provider']}/{r['part']}" for r in results})
            # color_print('blue', json.dumps(results, indent=2, ensure_ascii=False))

            # 以前3个元素作为键去重显示
            from sagas.nlu.content_representers import content_represent
            if not print_detail:
                # color_print('cyan', {(r[0], r[1], r[2]):content_represent(r[1], r[3]) for r in results})
                # tc.emp('cyan', {(r[0], r[1], r[2]): content_represent(r[1], r[3]) for r in results})
                tc.write({f"{r['inspector']}/{r['provider']}/...":
                              content_represent(r['provider'], r['value'])
                          for r in results})

            else:
                results = [el for r in rs for el in r[3].results if r[1]]  # r[1] is true/false
                pprint(results)
