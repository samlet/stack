from typing import Text, Any, Dict, List
from cachetools import cached

from sagas.nlu.inspector_common import Inspector, Context
from sagas.nlu.inspectors import InspectorFixture, DateInspector, EntityInspector
from sagas.nlu.patterns import Patterns, print_result
import requests
from sagas.conf.conf import cf
import logging

logger = logging.getLogger(__name__)

feat_pos_mappings={'c_adj':'a', 'c_adv':'r', 'c_noun':'n', 'c_verb':'v'}
# feat_pos_mappings={'c_adj':['n','a','s'], 'c_adv':'r', 'c_noun':'n', 'c_verb':'v'}


@cached(cache={})
def predicate(kind:Text, word:Text, lang:Text, pos:Text ):
    # if '/' in kind or '/' in word:
    data = {'word': word, 'lang': lang, 'pos': pos,
            'kind': kind}
    response = requests.post(f'{cf.ensure("words_servant")}/predicate_chain',
                             json=data)
    # else:
    #     data = {'word': word, 'lang': lang, 'pos': pos,
    #             'kind': kind, 'only_first': only_first}
    #     response = requests.post(f'{cf.ensure("words_servant")}/predicate',
    #                              json=data)
    if response.status_code == 200:
        r = response.json()
        return r['result']
    return False

class WordInspector(Inspector):
    def __init__(self, kind, pos_indicator='~', **kwargs):
        """
        Init a predicate inspector
        :param kind:
        :param pos_indicator: 如果是'~'就表示按照当前要测试chunk性质来决定要查找的继承链, 名词可以追溯继承链,
                形容词可以做直接匹配(用英语词干). 如果是'*'表示查找所有的词性, 这样有可能导致混乱; 如果是指定的词性,
                比如'n', 那么就会查询名词的继承链.
        :param only_first:
        """
        self.kind = kind
        # self.only_first=only_first
        self.pos_indicator=pos_indicator
        self.subs=None
        self.parameters=kwargs

    def name(self):
        return "kind_of"

    def get_pos_by_feat(self, feats):
        """
        Get POS by feature
        :param feats:
        :return: '*' represent any pos
        """
        # Part-of-speech constants, ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
        att=feats[0] # the first feature is word pos
        if att in feat_pos_mappings:
            return feat_pos_mappings[att]
        return '*'

    def substitute(self, word, lang, pos):
        from sagas.nlu.synonyms import synonyms
        r=synonyms.match(word, lang)
        # print(f'... retrieve substitute with {word}({lang})')
        if r is None:
            # return self.process(word, lang, pos)
            return predicate(self.kind, word, lang, pos)
        # print(f'... substitute with {r}(en), {pos}')
        # return self.process(r, 'en', pos)
        self.subs=r

        return predicate(self.kind, r, 'en', pos)

    @property
    def result_base(self) -> Dict[Text, Any]:
        results={'category': self.kind}
        if self.subs is not None:
            results['subs']=self.subs
        return results

    def __str__(self):
        return "{}({},{})".format(self.name(), self.kind, self.pos_indicator)


class PredicateWordInspector(WordInspector):
    """
    # $ se 'That spider flies.'
    # $ sid 'Burung dan kupu-kupu terbang.'
    # $ sid 'Laba-laba tersebut terbang.'  (这个句子使用的是单词原型'Laba-laba', 而不是词干lemma)
    >>> Patterns(domains, meta, 5, name='describe_animal_behave')
            .verb(behaveof('travel', 'v'), nsubj=kindof('animal', 'n')),
    # $ sid 'Burung itu suka makan serangga.' (zh="鸟喜欢吃虫子。")
    >>> Patterns(domains, meta, 5, name='describe_animal_hobby')
            .verb(behaveof('like', 'v'), nsubj=kindof('animal', 'n')),
    """

    def extract_word(self, key:Text, ctx:Context):
        if 'extract' in self.parameters:
            return self.parameters['extract'](key, ctx)
        return f"{ctx.words[key]}/{ctx.lemmas[key]}"

    def run(self, key, ctx:Context):
        # result=False
        lang=ctx.meta['lang']
        # word=ctx.lemmas[key]
        word = self.extract_word(key, ctx)
        # print(f".. predicate {word}")
        if self.pos_indicator=='~':
            pos=self.get_pos_by_feat(ctx.feats[key])
        else:
            pos=self.pos_indicator

        # result= predicate(self.kind, word, lang, pos, self.only_first)
        result=self.substitute(word, lang, pos)
        logger.debug(f"result base: {self.result_base}")
        if result:
            ctx.add_result(self.name(), 'default', key,
                           {**self.result_base, 'pos': pos, 'word': word},
                           delivery_type='sentence')
        return result

    def __str__(self):
        return "{}({},{})".format(self.name(), self.kind, self.pos_indicator)

class VerbInspector(WordInspector):
    """
    # $ ses '¿Te duelen las piernas?' (zh="你的腿受伤了吗？")
    >>> Patterns(domains, meta, 5).verb(behaveof('suffer', 'v'), nsubj=kindof('body_part', 'n')),
    # $ sz "吸烟对你的健康有害。"
    >>> Patterns(domains, meta, 5).verb(behaveof('consume', 'v'), cmp='c_adp'),
    # $ se 'Do it correctly.'
    >>> Patterns(domains, meta, 5, name='command_do').verb(behaveof('make', 'v'), advmod='c_adv'),
    """
    # def process(self, word, lang, pos):
    #     data = {'word': word, 'lang': lang, 'pos': pos,
    #             'kind': self.kind}
    #     # print('..', word)
    #     response = requests.post(f'{cf.ensure("words_servant")}/predicate_chain',
    #                              json=data)
    #
    #     if response.status_code == 200:
    #         r = response.json()
    #         return r['result']
    #     return False

    def extract_word(self, key:Text, ctx:Context):
        if 'extract' in self.parameters:
            return self.parameters['extract'](key, ctx)
        return key

    def run(self, key, ctx:Context):
        lang=ctx.meta['lang']
        # word=key  # the key == word
        word=self.extract_word(key, ctx)
        if self.pos_indicator=='~':
            pos='v'
        else:
            pos=self.pos_indicator

        result= self.substitute(word, lang, pos)
        logger.debug(f"check word {word} against {self.kind}, result is {result}")
        if result:
            ctx.add_result(self.name(), 'default', 'predicate',
                           {**self.result_base, 'pos': pos, 'word': word},
                           delivery_type='sentence')
        return result

    def name(self):
        return "behave_of"

    def __str__(self):
        return "{}({},{})".format(self.name(), self.kind, self.pos_indicator)


class WordSpecsInspector(WordInspector):
    """
    Instances: specsof('*', 'little', 'large')
    $ sj '太陽は月に比べて大きいです。'
    """
    def __init__(self, pos_indicator, *cats, **kwargs):
        super().__init__(cats[0], pos_indicator, **kwargs)
        self.cats=cats

    def check_subs(self, kind, word, lang, pos):
        from sagas.nlu.synonyms import synonyms
        r=synonyms.match(word, lang)
        if r is None:
            return predicate(kind, word, lang, pos)
        self.subs=r

        return predicate(self.kind, r, 'en', pos)

    def extract_specs(self, key, ctx:Context):
        if '/' in key:
            word=key  # the key == word
        else:
            word = f"{ctx.words[key]}/{ctx.lemmas[key]}"
        return word

    def run(self, key, ctx:Context):
        lang=ctx.lang
        word=self.extract_specs(key, ctx)
        pos=self.pos_indicator

        resultset=[]
        for kind in self.cats:
            result= self.check_subs(kind, word, lang, pos)
            logger.debug(f"check word {word} against {kind}, result is {result}")
            if result:
                ctx.add_result(self.name(), 'default', 'predicate',
                               {**self.result_base, 'pos': pos, 'word': word},
                               delivery_type='sentence')
            resultset.append(result)
        return any(resultset)

    def name(self):
        return "specs_of"

    def __str__(self):
        return "{}({},{})".format(self.name(), self.cats, self.pos_indicator)

class InspectorRunner(InspectorFixture):
    def __init__(self):
        super().__init__()
        import sagas.nlu.patterns as pat
        pat.print_not_matched=True

    def procs_common(self, data):
        domains, meta=self.request_domains(data)
        agency = ['c_pron', 'c_noun']
        rs = [Patterns(domains, meta, 2).verb(nsubj_pass=agency, obl=DateInspector('time')),
              Patterns(domains, meta, 2).verb(nsubj_pass=agency, obl=EntityInspector('GPE')),
              Patterns(domains, meta, 2).verb(nsubj=agency, xcomp=PredicateWordInspector('color', 'n')),
              ]
        print_result(rs)

    def test_1(self):
        """
        $ python -m sagas.nlu.inspector_wordnet test_1
        :return:
        """
        text = 'O homem fica amarelo.'
        data = {'lang': 'pt', "sents": text}
        self.procs_common(data)

if __name__ == '__main__':
    import fire
    fire.Fire(InspectorRunner)

