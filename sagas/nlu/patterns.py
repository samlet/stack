class Context(object):
    def __init__(self, meta, domains):
        self.meta=meta
        # self.chunks = {x[0]: x[4] for x in domains}
        self._chunks = [Chunk(x[0], x[4]) for x in domains]
        self.lemmas = {x[0]: x[3] for x in domains}
        self.feats = {x[0]: x[5] for x in domains}

    def get_chunks(self, key):
        return [c for c in self._chunks if c.key==key]

    def chunk_contains(self, key, val):
        chunks = self.get_chunks(key)
        for c in chunks:
            if val in c.children:
                return True
        return False

    def get_single_chunk_text(self, key):
        chunks=self.get_chunks(key)
        if len(chunks)>0:
            cnt = ' '.join(chunks[0].children)
            return cnt
        return ''

    def chunk_pieces(self, key):
        chunks = self.get_chunks(key)
        return [' '.join(c.children) for c in chunks]

class Inspector(object):
    def name(self):
        # type: () -> Text
        """Unique identifier of this simple inspector."""

        raise NotImplementedError("An inspector must implement a name")

    def run(self, key, ctx:Context):
        raise NotImplementedError("An inspector must implement its run method")

    def __str__(self):
        return "Inspector('{}')".format(self.name())

def check_item(feats, key, el, ctx):
    if key in feats:
        if isinstance(el, list) or isinstance(el, tuple):
            # print(el)
            # check 'or', so return true only requires one element to match
            for e in el:
                if e in feats[key]:
                    return True
        elif isinstance(el, Inspector):
            return el.run(key, ctx)
        else:
            return el in feats[key]
    return False


# c(domains).verb(nsubj='c_pron', obj='c_noun')
def verb_pattern_checker(domains):
    rel_feats = {x[0]: x[5] for x in domains}
    if (check_item(rel_feats, 'nsubj', 'c_pron', None) and
            check_item(rel_feats, 'obj', 'c_noun', None)):
        print('pattern: verb+nsubj(pron)+obj(noun)')

class Chunk(object):
    def __init__(self, key, children):
        self.key=key
        self.children=children

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
                opt_ret=check_item(self.meta, 'pos', args, ctx)
                if not opt_ret:
                    result = False
                options.append('{} is {}: {}'.format('pos', args, opt_ret))

            # rel_feats = {x[0]: x[5] for x in self.domains}
            rel_feats=ctx.feats

            for key, value in kwargs.items():
                key=key.replace('_', ':')
                key=trip_number_suffix(key)
                if key.startswith(':'):
                    opt_ret=check_item(self.meta, key[1:], value, ctx)
                else:
                    opt_ret = check_item(rel_feats, key, value, ctx)

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

from sagas.nlu.inspectors import NegativeWordInspector as negative
from sagas.nlu.inspectors import DateInspector as dateins
from sagas.nlu.inspectors import EntityInspector as entins

#⊕ [nmod](https://universaldependencies.org/u/dep/nmod.html)
def verb_patterns(meta, domains):
    agency=['c_pron', 'c_noun']
    pats=[Patterns(domains, meta, 1).verb(nsubj=agency, obj=agency),
          # 复合动词: Drengen har nederdelen på. (har..på是一个动词) ([en] The boy is wearing the skirt.)
          Patterns(domains, meta, 2).verb(compound_prt='c_adv', nsubj=agency, obj=agency),
          # 连接另一个动词: Pigerne spiser måltidet og drikker teen. ([en] The girls eat the meal and drink the tea.)
          Patterns(domains, meta).verb(nsubj=agency, obj=agency, conj='c_verb'),
          # nmod: nominal modifier
          # The nmod relation is used for nominal dependents of another noun or noun phrase and functionally corresponds to an attribute, or genitive complement.
          Patterns(domains, meta).verb(nsubj=agency, cop='c_aux', nmod=agency),
          # obl: oblique nominal
          # The obl relation is used for a nominal (noun, pronoun, noun phrase) functioning as a non-core (oblique) argument or adjunct. This means that it functionally corresponds to an adverbial attaching to a verb, adjective or other adverb.
          Patterns(domains, meta).verb(nsubj=agency, obl=agency),
          # advmod: adverbial modifier
          # An adverbial modifier of a word is a (non-clausal) adverb or adverbial phrase that serves to modify a predicate or a modifier word.
          Patterns(domains, meta).verb(nsubj=agency, advmod='c_adv'),
          # Wir können tanzen, wenn wir wollen. ([en] We can dance if we want. [zh] 如果我们想要，我们可以跳舞。)
          Patterns(domains, meta).verb(nsubj=agency, advcl='c_aux'),
          # Ben okuldayım. ([en] I'm in school.)
          Patterns(domains, meta).verb(nsubj=agency),
          # Φοράω το μάλλινο παλτό μου. ([en] I wear my wool coat.)
          Patterns(domains, meta).verb(obj=agency),
          # 关系parataxis用于一对可能是独立句子的东西，但它们被一起作为一个句子对待。
          # Diese Liga ist die beste Liga, glaube ich. ([en] This league is the best league, I think.)
          Patterns(domains, meta).verb(_rel='parataxis', nsubj=agency),

          # 匹配否定词: Han har ikke tøjet på.
          Patterns(domains, meta, 2).verb(nsubj=agency, obj=agency, advmod=negative()),
          # 匹配日期维: I was born in the spring of 1982.
          Patterns(domains, meta, 2).verb(nsubj_pass=agency, obl=dateins('time')),
          # 匹配实体: I was born in Beijing.
          Patterns(domains, meta, 2).verb(nsubj_pass=agency, obl=entins('GPE')),
          ]
    print_result(pats)

def aux_patterns(meta, domains):
    agency = ['c_pron', 'c_noun']
    pats=[Patterns(domains, meta).aux('pron', 'noun', nsubj=agency, cop='c_aux'),
          # Eine Teilnahme ist kostenlos. (Attendance is free of charge.)
          Patterns(domains, meta).aux('adj', nsubj=agency, cop='c_aux'),
          # Wir haben ihn zum Bürgermeister gewählt. ([en] We chose him as mayor.)
          Patterns(domains, meta).aux('pron', 'noun', nsubj_pass=agency, cop='c_aux'),
          # Dies war der erste Sieg seiner Karriere. ([en] This was the first victory of his career.)
          Patterns(domains, meta).aux('noun', nsubj=agency, cop='c_aux', amod='c_adj', nmod='c_noun'),
          # Ben kimim?
          Patterns(domains, meta).aux('pron', 'noun', aux_q='c_aux'),
          ]
    print_result(pats)

def subj_patterns(meta, domains):
    agency = ['c_pron', 'c_noun']
    pats=[Patterns(domains, meta).subj('pron', 'noun', nsubj=agency),
          # O nasıl? ([en] Who am I?)
          Patterns(domains, meta).subj('adv', nsubj=agency),
          # Tuvalette örümcek var. ([en] There's a spider in the bathroom.)
          Patterns(domains, meta).subj('adj', nsubj=agency, obl=agency),
          # Banyoda kadınlar var. ([en] There are women in the bathroom.)
          Patterns(domains, meta).subj('adj', nsubj=['x_nadj'], obl=agency),
          # Solda bir köpek var. ([en] There's a dog on the left. [ja] 左側に犬がいます。)
          Patterns(domains, meta).subj('adj', nsubj=agency, amod='c_adj'),
          # Ankara'da çok kedi var. ([en] There are many cats in Ankara. [ja] アンカラにはたくさんの猫がいます。)
          Patterns(domains, meta).subj('adj', nsubj=agency, obl='c_propn'),
          # Ne kadar sütümüz var? ([en] How much milk do we have?)
          Patterns(domains, meta).subj('adj', nsubj=agency),
          ]
    print_result(pats)


