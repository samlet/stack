from sagas.nlu.inspector_common import Inspector, Context
from sagas.nlu.inspectors import InspectorFixture, DateInspector, EntityInspector
from sagas.nlu.patterns import Patterns, print_result
import requests

feat_pos_mappings={'c_adj':'a', 'c_adv':'r', 'c_noun':'n', 'c_verb':'v'}
# feat_pos_mappings={'c_adj':['n','a','s'], 'c_adv':'r', 'c_noun':'n', 'c_verb':'v'}

class PredicateWordInspector(Inspector):
    def __init__(self, kind, pos_indicator='~', only_first=True):
        """
        Init a predicate inspector
        :param kind:
        :param pos_indicator: 如果是'~'就表示按照当前要测试chunk性质来决定要查找的继承链, 名词可以追溯继承链,
                形容词可以做直接匹配(用英语词干). 如果是'*'表示查找所有的词性, 这样有可能导致混乱; 如果是指定的词性,
                比如'n', 那么就会查询名词的继承链.
        :param only_first:
        """
        self.kind = kind
        self.only_first=only_first
        self.pos_indicator=pos_indicator

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

    def run(self, key, ctx:Context):
        result=False
        lang=ctx.meta['lang']
        word=ctx.lemmas[key]
        if self.pos_indicator=='~':
            pos=self.get_pos_by_feat(ctx.feats[key])
        else:
            pos=self.pos_indicator

        data={'word': word, 'lang': lang, 'pos': pos,
            'kind': self.kind, 'only_first': self.only_first}
        response = requests.post('http://localhost:8093/predicate',
                                 json=data)
        if response.status_code == 200:
            r=response.json()
            result=r['result']
        return result

    def __str__(self):
        return "{}({},{})".format(self.name(), self.kind, self.pos_indicator)

class InspectorRunner(InspectorFixture):
    def __init__(self):
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

