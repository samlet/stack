from sagas.nlu.inspectors import NegativeWordInspector as negative
from sagas.nlu.inspectors import DateInspector as dateins
from sagas.nlu.inspectors import EntityInspector as entins
from sagas.nlu.inspector_wordnet import PredicateWordInspector as kindof
from sagas.nlu.inspector_wordnet import VerbInspector as behaveof
from sagas.nlu.inspector_rasa import RasaInspector as intentof

from sagas.nlu.patterns import Patterns, print_result
import sagas.tracker_fn as tc

agency=['c_pron', 'c_noun', 'c_propn']

class LangSpecBase(object):
    def __init__(self, meta, domains):
        self.meta=meta
        self.domains=domains
        self.matched={}

    def verb_rules(self):
        pass
    def aux_rules(self):
        pass
    def subject_rules(self):
        pass
    def predicate_rules(self):
        pass
    def root_rules(self):
        pass

    def execute(self):
        '''
        The execute method default implementation
        :return:
        '''
        if len(self.matched)>0:
            matched_info={k:len(v.results) for k,v in self.matched.items()}
            tc.emp('blue', f"♯ matched id rules: {matched_info}")

    def collect(self, pats):
        print_result(pats)
        for r in pats:
            if r[1] and r[3].name != '':
                self.matched[r[3].name] = r[3]  # r[3] is Context

class Rules_id(LangSpecBase):
    def root_rules(self):
        domains, meta=(self.domains, self.meta)
        self.collect(pats=[Patterns(domains, meta, 1).verb(nsubj=agency, obj=agency),
              # $ sid 'Berapa umur kamu?' (en="How old are you?")
              Patterns(domains, meta, 5, name='years_old').verb(behaveof('age', 'n'), amod='c_det'),
              # $ sid 'Bola putih.' (球是白的)
              # notice: 'Bola Dimas putih.'无法匹配这条规则, 因为'Bola Dimas'是flat关系,
              # 针对id中的flat关系, 需要单独处理, 将flat关系的token合并为chunk, 然后再处理这个chunk与外界之间的关系.
              Patterns(domains, meta, 5).verb(behaveof('physical_entity', 'n'), amod=kindof('color', 'n')),
              ])

# ________________________________________________________________________
lang_specs={'id':[Rules_id]}

def exec_rules_by_type(ci:LangSpecBase, type_name):
    mappings={'verb_domains':ci.verb_rules,
              'aux_domains':ci.aux_rules,
              'subj_domains':ci.subject_rules,
              'predicate':ci.predicate_rules,
              'root_domains':ci.root_rules,
              }
    mappings[type_name]()
    # ci.root_rules()

def check_langspec(lang, meta, domains, type_name):
    # lang = data['lang']
    if lang in lang_specs:
        # from termcolor import colored
        tc.emp('cyan', f"✁ lang.spec for {lang}.{type_name} {'-' * 25}")
        for c in lang_specs[lang]:
            ci=c(meta, domains)
            exec_rules_by_type(ci, type_name)
            ci.execute()
    else:
        tc.emp('red', f'no special patterns for lang {lang}')


def rs_repr(rs, data):
    for serial, r in enumerate(rs):
        common = {'lemma': r['lemma'], 'word': r['word'],
                  'stems': r['stems']}
        meta = {'rel': r['rel'], **common, **data}
        lang=data['lang']

        # if lang in lang_specs:
        #     lang_specs[lang](meta, r['domains'])
        # else:
        #     tc.emp('red', f'no special patterns for lang {lang}')
        check_langspec(lang, meta, r['domains'], type_name = r['type'])

class LangspecRules(object):
    def langspec(self, sents, lang='en', engine='corenlp'):
        """
        $ python -m sagas.nlu.rules_lang_spec langspec 'Berapa umur kamu?' id
        :param sents:
        :param lang:
        :param engine:
        :return:
        """
        from sagas.nlu.uni_remote import dep_parse
        from sagas.nlu.corenlp_parser import get_chunks

        pipelines = ['predicts']
        doc_jsonify, resp = dep_parse(sents, lang, engine, pipelines)
        rs = get_chunks(doc_jsonify)
        rs_repr(rs, data={'lang': lang, "sents": sents, 'engine': engine, 'pipelines': pipelines})

    def langspec_id(self, sents, engine='corenlp'):
        """
        $ python -m sagas.nlu.rules_lang_spec langspec_id 'Berapa umur kamu?'
        :param sents:
        :param engine:
        :return:
        """
        from sagas.nlu.uni_remote import dep_parse
        from sagas.nlu.corenlp_parser import get_chunks

        pipelines = ['predicts']
        lang='id'
        doc_jsonify, resp = dep_parse(sents, lang, engine, pipelines)
        rs = get_chunks(doc_jsonify)
        # rs_repr(rs, data={'lang': lang, "sents": sents, 'engine': engine, 'pipelines': pipelines})
        data = {'lang': lang, "sents": sents, 'engine': engine, 'pipelines': pipelines}
        for serial, r in enumerate(rs):
            common = {'lemma': r['lemma'], 'word': r['word'],
                      'stems': r['stems']}
            meta = {'rel': r['rel'], **common, **data}
            c=Rules_id(meta, r['domains'])
            c.root_rules()
            c.execute()

if __name__ == '__main__':
    import fire
    fire.Fire(LangspecRules)

