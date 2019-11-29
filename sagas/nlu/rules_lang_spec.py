import logging
from sagas.nlu.inspectors import NegativeWordInspector as negative
from sagas.nlu.inspectors import DateInspector as dateins
from sagas.nlu.inspectors import EntityInspector as entins
from sagas.nlu.inspector_wordnet import PredicateWordInspector as kindof
from sagas.nlu.inspector_wordnet import VerbInspector as behaveof
from sagas.nlu.inspector_rasa import RasaInspector as intentof
from sagas.nlu.lang_spec_intf import LangSpecBase, agency

from sagas.nlu.patterns import Patterns, print_result
import sagas.tracker_fn as tc
from sagas.nlu.rules_lang_spec_de import Rules_de
from sagas.nlu.rules_meta import build_meta

logger = logging.getLogger(__name__)

class Rules_id(LangSpecBase):
    def verb_rules(self):
        domains, meta = (self.domains, self.meta)
        self.collect(pats=[
            # $ sid 'Pekerjaan ini dimulai oleh mereka.' (This job is started by them.)
            Patterns(domains, meta, 2, name='behave_di_obl').verb(nsubj_pass=agency, obl=agency),
            # $ sid 'Makanan ini disebut nasi goreng.' (en="This food is called nasi goreng.")
            Patterns(domains, meta, 2, name='behave_di_obj').verb(nsubj_pass=agency, obj=agency),
            Patterns(domains, meta, 2, name='food').verb(obj = kindof('food/physical_entity', 'n')),
            # $ sid 'Raja dan ratu dianggap jahat.' (en="The king and queen are considered evil.")
            Patterns(domains, meta, 2, name='behave_di_amod').verb(nsubj_pass=agency, amod='c_adj'),
            # $ sid 'Surat-surat mereka dibuat di sini.'
            Patterns(domains, meta, 2, name='behave_di_case').verb(nsubj_pass=agency, case=agency),
            # $ sid 'Saya diduga membantu polisi.' (I am suspected of helping the police.)
            Patterns(domains, meta, 2, name='behave_di_xcomp').verb(nsubj_pass=agency, xcomp='c_verb'),
            # Kadang-kadang kami mandi di sungai. 有时我们在河里洗澡。
            Patterns(domains, meta, 5, name='behave_cleanse').verb(behaveof('cleanse/better', 'v')),
            # Lemari besar itu tidak terangkat. 那个大柜子抬不动。
            Patterns(domains, meta, 5, name='move_unable').verb(behaveof('move', 'v'), advmod=negative()),
            # Dia datang ke Shanghai untuk menjumpai adiknya. 他为了见弟弟来到了上海。
            Patterns(domains, meta, 5, name='behave_purpose').verb(
                behaveof('arrive', 'v'), nsubj=agency, xcomp='c_verb', obl=agency, ),
            ])

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
lang_specs={'id': [Rules_id],
            'de': [Rules_de],
            }

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
        # meta = {'rel': r['rel'], **common, **data}
        meta=build_meta(r, common, data)
        lang=data['lang']

        # if lang in lang_specs:
        #     lang_specs[lang](meta, r['domains'])
        # else:
        #     tc.emp('red', f'no special patterns for lang {lang}')
        check_langspec(lang, meta, r['domains'], type_name = r['type'])

class LangspecRules(object):
    def __init__(self):
        from sagas.tool.loggers import init_logger
        init_logger()

    def langspec(self, sents, lang='en', engine='corenlp'):
        """
        $ python -m sagas.nlu.rules_lang_spec langspec 'Berapa umur kamu?' id
        $ python -m sagas.nlu.rules_lang_spec langspec 'Die Nutzung der Seite ist kostenlos.' de

        :param sents:
        :param lang:
        :param engine:
        :return:
        """
        from sagas.nlu.uni_remote import dep_parse
        from sagas.nlu.corenlp_parser import get_chunks

        pipelines = ['predicts']
        doc_jsonify, resp = dep_parse(sents, lang, engine, pipelines)
        # print('.......')
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

