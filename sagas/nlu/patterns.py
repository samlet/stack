def check_item(feats, key, el):
    if key in feats:
        if isinstance(el, list) or isinstance(el, tuple):
            # print(el)
            # check 'or', so return true only requires one element to match
            for e in el:
                if e in feats[key]:
                    return True
        else:
            return el in feats[key]
    return False


# c(domains).verb(nsubj='c_pron', obj='c_noun')
def verb_pattern_checker(domains):
    rel_feats = {x[0]: x[5] for x in domains}
    if (check_item(rel_feats, 'nsubj', 'c_pron') and
            check_item(rel_feats, 'obj', 'c_noun')):
        print('pattern: verb+nsubj(pron)+obj(noun)')


class Patterns(object):
    _name = None
    _fields = {}  # {field: field object}

    def __init__(self, domains=None, meta=None, track=True):
        super(Patterns, self).__init__()
        self.domains = domains
        self.meta=meta
        self.track = track

    def __getattr__(self, method):
        """Provide a dynamic access to a service method."""
        if method.startswith('_'):
            return super(Patterns, self).__getattr__(method)

        def service_method(*args, **kwargs):
            """Return the result of the check request."""
            result = True
            options = []

            if self.meta is not None:
                opt_ret=check_item(self.meta, 'pos', args)
                if not opt_ret:
                    result = False
                options.append('{} is {}: {}'.format('pos', args, opt_ret))

            rel_feats = {x[0]: x[5] for x in self.domains}

            for key, value in kwargs.items():
                opt_ret = check_item(rel_feats, key, value)
                if not opt_ret:
                    result = False
                options.append('{} is {}: {}'.format(key, value, opt_ret))
            if self.track:
                return "%s with %s" % (method, ', '.join(options)), result
            else:
                return result

        return service_method

def print_result(rs):
    from termcolor import colored
    for r in rs:
        clr='red' if r[1] else 'cyan'
        print('%s [%s]'%(colored('✔', clr) if r[1] else '✖',
                         colored(r[0], clr)))
#⊕ [nmod](https://universaldependencies.org/u/dep/nmod.html)
def verb_patterns(domains):
    agency=['c_pron', 'c_noun']
    pats=[Patterns(domains).verb(nsubj=agency, obj=agency),
          # nmod: nominal modifier
          # The nmod relation is used for nominal dependents of another noun or noun phrase and functionally corresponds to an attribute, or genitive complement.
          Patterns(domains).verb(nsubj=agency, cop='c_aux', nmod=agency),
          # obl: oblique nominal
          # The obl relation is used for a nominal (noun, pronoun, noun phrase) functioning as a non-core (oblique) argument or adjunct. This means that it functionally corresponds to an adverbial attaching to a verb, adjective or other adverb.
          Patterns(domains).verb(nsubj=agency, obl=agency),
          # advmod: adverbial modifier
          # An adverbial modifier of a word is a (non-clausal) adverb or adverbial phrase that serves to modify a predicate or a modifier word.
          Patterns(domains).verb(nsubj=agency, advmod='c_adv'),
          ]
    print_result(pats)

def aux_patterns(meta, domains):
    agency = ['c_pron', 'c_noun']
    pats=[Patterns(domains, meta).aux('pron', 'noun', nsubj=agency, cop='c_aux'),
          ]
    print_result(pats)

def subj_patterns(meta, domains):
    agency = ['c_pron', 'c_noun']
    pats=[Patterns(domains, meta).subj('pron', 'noun', nsubj=agency),
          ]
    print_result(pats)


