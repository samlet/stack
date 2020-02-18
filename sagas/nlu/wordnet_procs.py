from nltk.corpus import wordnet as wn

hypo = lambda s: s.hyponyms()
hyper = lambda s: s.hypernyms()

def names(rs):
    return [r.name() for r in rs]

def ensure(s):
    return '_' if s is None else str(s)

def check_chains(synsets: list, kind):
    kind_set = set(kind.split('/'))
    for index, c in enumerate(synsets):
        # c = wn.synset(synset)
        chain = {}
        chain_keys=[]
        for c_c in [c] + list(c.closure(hyper)):
            key = c_c.name().split('.')[0]
            if key in chain:
                print('!! duplicated key %s' % c_c.name())
            chain[key] =c_c.name()
            chain_keys.append(key)
        container = set(chain.keys())
        check_r = kind_set.issubset(container)
        # print(index, check_r, container)
        if check_r:
            return True, {'index': 0, 'keys': chain_keys, 'maps': chain}
    return False, None

def predicate_chain(word_candicates, kind, lang='en', pos='n'):
    # from sagas.nlu.locales import iso_locales
    # print('.. checking %s is %s'%(word,kind))
    # loc, _ = iso_locales.get_code_by_part1(lang)
    # sets = wn.synsets(word, lang=loc, pos=None if pos == '*' else pos)
    from sagas.nlu.omw_extended import get_synsets
    for word in word_candicates.split('/'):
        sets = get_synsets(lang, word, pos)
        # ret = False
        if len(sets) > 0:
            # c=[s.name() for s in sets]
            ok,r= check_chains(sets, kind)
            if ok:
                return ok,r
    return False, None

def get_chains(word, lang='en', pos=None):
    # from sagas.nlu.locales import iso_locales
    # loc, _ = iso_locales.get_code_by_part1(lang)
    # synsets = wn.synsets(word, lang=loc, pos=None if pos == '*' else pos)
    from sagas.nlu.omw_extended import get_synsets
    synsets = get_synsets(lang, word, pos)

    chains = []
    for index, c in enumerate(synsets):
        print(c.offset(), c.name())
        chain_keys = []
        for c_c in [c] + list(c.closure(hyper)):
            key = c_c.name()
            chain_keys.append(key)
        chains.append({'offset':c.offset(), 'name':c.name(), 'chain':chain_keys})
    return chains

class WordNetProcs(object):
    def __init__(self):
        from sagas.nlu.omw_extended import omw_ext
        from sagas.conf.conf import cf
        self.omw = omw_ext
        self.default_langs=cf.ensure('default_word_sets_langs')

    def all_langs(self, part1_format=False):
        """
        $ python -m sagas.nlu.wordnet_procs all_langs
        :return:
        """
        from sagas.nlu.locales import iso_locales
        langs = wn.langs()
        if part1_format:
            print(', '.join(sorted(iso_locales.iso_map.keys())))
        else:
            print('total', len(langs))
            print(', '.join(sorted(langs)))
            print(', '.join(sorted(iso_locales.iso_map.keys())))

    def get_word_sets(self, word, lang='en', pos='*'):
        """
        $ python -m sagas.nlu.wordnet_procs get_word_sets menina pt
        $ python -m sagas.nlu.wordnet_procs get_word_sets ложь ru
        $ python -m sagas.nlu.wordnet_procs get_word_sets piti hr

        :param word:
        :param lang:
        :return:
        """
        # from sagas.nlu.locales import iso_locales
        # loc, _ = iso_locales.get_code_by_part1(lang)
        # sets = wn.synsets(word, pos=pos, lang=loc)
        from sagas.nlu.omw_extended import get_synsets
        from sagas.nlu.wordnet_explore import get_word_lemmas
        sets=get_synsets(lang, word, pos)
        rs=[]
        for s in sets:
            # print("%s -> %s"%(colored(s.name(), 'green'), s.definition()))
            rec={'name':s.name(), 'definition':s.definition(),
                 'examples':[str(exa) for exa in s.examples()]}
            domains = {'topic': names(s.topic_domains()),
                       'region': names(s.region_domains()),
                       'usage': names(s.usage_domains())}
            lemmas={}
            # for lang in ['en', 'zh', 'ja']:
            for lang in self.default_langs:
                lemmas[lang]=get_word_lemmas(s, lang)
            rec['domains']=domains
            rec['lemmas']=lemmas
            rs.append(rec)
        return rs

    def get_all_keys(self, synsets:list):
        keys = []
        for synset in synsets:
            c = wn.synset(synset)
            for c_c in [c]+list(c.closure(hyper)):
                # print(c_c.name(), c_c.lemma_names('eng'), c_c.lemma_names('cmn'))
                keys.extend(c_c.lemma_names('eng'))
                keys.extend(c_c.lemma_names('cmn'))
        return (keys)

    def predicate_chain(self, word, kind, lang='en', pos='n'):
        """
        $ python -m sagas.nlu.wordnet_procs predicate_chain koran print_media id n
        $ python -m sagas.nlu.wordnet_procs predicate_chain koran/jjj print_media id n
        $ python -m sagas.nlu.wordnet_procs predicate_chain pije/piti drink hr v

        :param word:
        :param kind:
        :param lang:
        :param pos:
        :return:
        """
        return predicate_chain(word, kind, lang, pos)

    def predicate(self, word, kind, lang='en', pos='n', only_first=True):
        """
        $ python -m sagas.nlu.wordnet_procs predicate wolf animal en n
            True
        $ python -m sagas.nlu.wordnet_procs predicate wolf mammal en n
            True
        $ python -m sagas.nlu.wordnet_procs predicate wolf color en n
            False
        $ python -m sagas.nlu.wordnet_procs predicate blue color en n
            True
        $ python -m sagas.nlu.wordnet_procs predicate amarelo color pt n
        $ python -m sagas.nlu.wordnet_procs predicate koran print_media id n False

        :param word:
        :param kind:
        :param lang:
        :param pos:
        :param only_first:
        :return:
        """
        # from sagas.nlu.locales import iso_locales
        # loc, _ = iso_locales.get_code_by_part1(lang)
        # sets = wn.synsets(word, lang=loc, pos=None if pos=='*' else pos)
        from sagas.nlu.omw_extended import get_synsets
        sets = get_synsets(lang, word, pos)

        ret=False
        if len(sets)>0:
            if only_first:
                c=[sets[0].name()]
            else:
                c=[s.name() for s in sets]
            ret=kind in self.get_all_keys(c)
        return ret

    def word_sets(self, word, lang='en', pos='*'):
        """
        $ python -m sagas.nlu.wordnet_procs word_sets 犬 ja
        $ python -m sagas.nlu.wordnet_procs word_sets code
        $ python -m sagas.nlu.wordnet_procs word_sets denied

        $ python -m sagas.nlu.wordnet_procs word_sets menina pt
        $ python -m sagas.nlu.wordnet_procs word_sets lobo pt
        $ python -m sagas.nlu.wordnet_procs word_sets wolf en n

        $ word здоровый ru
        :param word:
        :param lang:
        :return:
        """
        from termcolor import colored
        from sagas.nlu.wordnet_explore import get_word_lemmas

        # from sagas.nlu.locales import iso_locales
        # loc, _=iso_locales.get_code_by_part1(lang)
        # print('.. query {} in language {}'.format(word, loc))
        # sets=wn.synsets(word, lang=loc, pos=None if pos=='*' else pos)
        from sagas.nlu.omw_extended import get_synsets
        sets = get_synsets(lang, word, pos)
        print(sets)
        for s in sets:
            if s is not None:
                print("%s -> %s"%(colored(ensure(s.name()), 'green'), ensure(s.definition())))
                for exa in s.examples():
                    print('\t', exa)
                domains={'topic': names(s.topic_domains()),
                         'region': names(s.region_domains()),
                         'usage': names(s.usage_domains())}
                print('\t', domains)
                for l in ['en', 'fr', 'pt', 'zh', 'ja']:
                    lemmas = get_word_lemmas(s, l)
                    if len(lemmas)>0:
                        lemmas_t=', '.join(lemmas)
                        print('\t', l, lemmas_t[:25]+'..' if len(lemmas_t)>25 else lemmas_t)

    def lemmas(self, word, lang, to_lang):
        """
        $ python -m sagas.nlu.wordnet_procs lemmas 犬 ja ja
        $ python -m sagas.nlu.wordnet_procs lemmas dog en zh
        :param word:
        :param lang:
        :param to_lang:
        :return:
        """
        from sagas.nlu.locales import iso_locales
        loc, _ = iso_locales.get_code_by_part1(lang)
        to_loc, _=iso_locales.get_code_by_part1(to_lang)
        if loc=='' or to_loc=='':
            print('from %s to %s is not supported.'%(lang, to_lang))
            print('supported languages:', ', '.join(sorted(iso_locales.iso_map.keys())))
            return

        sets = wn.synsets(word, lang=loc)
        for s in sets:
            names=s.lemma_names(to_loc)
            if len(names)>0:
                print(s, names)

    def word_morph(self, word):
        """
        $ python -m sagas.nlu.wordnet_procs word_morph denied
        :param word:
        :return:
        """
        # Morphy uses a combination of inflectional ending rules and exception lists to handle a variety of different possibilities
        # see: http://www.nltk.org/howto/wordnet.html
        nform=wn.morphy(word, wn.NOUN)
        vform=wn.morphy(word, wn.VERB)
        print('n.', '_' if nform is None else nform)
        print('v.', '_' if vform is None else vform)

    def hypernyms(self, pos='n'):
        """
        $ python -m sagas.nlu.wordnet_procs hypernyms n
        :param pos:
        :return:
        """
        from itertools import islice
        for synset in islice(wn.all_synsets(pos), 5):
            print(synset, synset.hypernyms())

    def list_hypo(self, word, pos):
        """
        $ python -m sagas.nlu.wordnet_procs list_hypo dog n

        >>> list(dog.closure(hypo, depth=1)) == dog.hyponyms()
        True
        >>> list(dog.closure(hyper, depth=1)) == dog.hypernyms()
        True
        :param word: English word
        :param pos: Part-of-speech constants, ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
        :return:
        """
        sets=wn.synsets(word, pos)
        for s in sets:
            ss=list(s.closure(hypo))
            if len(ss)>0:
                print('♥', s.name(), '->', ', '.join([w.name() for w in ss]))

    def list_hyper(self, word, pos):
        """
        $ python -m sagas.nlu.wordnet_procs list_hyper dog n
        $ python -m sagas.nlu.wordnet_procs list_hyper kick v
        $ python -m sagas.nlu.wordnet_procs list_hyper sweater n

        :param word:
        :param pos:
        :return:
        """
        sets=wn.synsets(word, pos)
        for s in sets:
            ss=list(s.closure(hyper))
            if len(ss)>0:
                print('♥', s.name(), '->', ', '.join([w.name() for w in ss]))

    def desc_hyper(self, synset):
        """
        $ python -m sagas.nlu.wordnet_procs desc_hyper 'dog.n.01'

        * 步骤:
        1. 查询出synset: python -m sagas.nlu.wordnet_procs list_hyper sweater n
        2. 获取synset的详细信息:
            python -m sagas.nlu.wordnet_procs desc_hyper 'sweater.n.01'
            python -m sagas.nlu.wordnet_procs desc_hyper 'clothing.n.01'
        3. 获取继承树上的词汇解释(lemma):
            python -m sagas.nlu.wordnet_procs word_sets artifact
        4. 形容词没有继承链, 名词才有:
            $ python -m sagas.nlu.wordnet_procs desc_hyper yellow.s.01
            $ python -m sagas.nlu.wordnet_procs desc_hyper yellow.n.01

        :param synset:
        :return:
        """
        c = wn.synset(synset)
        keys = []
        for c_c in [c]+list(c.closure(hyper)):
            print(c_c.name(), c_c.lemma_names('eng'), c_c.lemma_names('cmn'))
            keys.extend(c_c.lemma_names('eng'))
            keys.extend(c_c.lemma_names('cmn'))
        print(keys)

    def get_inherited(self, word, pos, clo):
        rs=[]
        sets = wn.synsets(word, pos)
        for s in sets:
            ss = list(s.closure(clo))
            if len(ss) > 0:
                rs.extend([w.name() for w in ss])
        return set(rs)

    def get_hyper(self, word, pos):
        """
        $ python -m sagas.nlu.wordnet_procs get_hyper dog n
        :param word:
        :param pos:
        :return:
        """
        return self.get_inherited(word, pos, hyper)

    def get_hypo(self, word, pos):
        """
        $ python -m sagas.nlu.wordnet_procs get_hypo dog n
        :param word:
        :param pos:
        :return:
        """
        return self.get_inherited(word, pos, hypo)

    def print_lemmas(self, synsets, target_langs):
        from sagas.nlu.omw_extended import langsets
        from sagas.nlu.locales import is_available

        for idx, c in enumerate(synsets):
            print('%d.' % idx, c.name())
            for c_c in [c] + list(c.closure(hyper)):
                print('\t', c_c.name(), c_c.offset(), c_c.pos())
                for lang in target_langs:
                    if not is_available(lang):
                        les=[w['word'] for w in self.omw.get_word(lang, c_c.offset(), c_c.pos())]
                    else:
                        les = c_c.lemma_names(langsets[lang])
                    if len(les) > 0:
                        print('\t\t[%s]' % lang, ', '.join(les))

    def print_definition(self, word):
        """
        $ python -m sagas.nlu.wordnet_procs print_definition dog
        :param word:
        :return:
        """
        from sagas.nlu.omw_extended import langsets
        sets = wn.synsets(word, pos=None, lang=langsets['en'])
        # self.print_lemmas(sets, ['en', 'fr', 'ja', 'zh'])
        self.print_lemmas(sets, ['en', 'ja', 'de', 'ru'])

if __name__ == '__main__':
    import fire
    fire.Fire(WordNetProcs)
