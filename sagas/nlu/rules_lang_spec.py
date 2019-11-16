from sagas.nlu.inspectors import NegativeWordInspector as negative
from sagas.nlu.inspectors import DateInspector as dateins
from sagas.nlu.inspectors import EntityInspector as entins
from sagas.nlu.inspector_wordnet import PredicateWordInspector as kindof
from sagas.nlu.inspector_wordnet import VerbInspector as behaveof
from sagas.nlu.inspector_rasa import RasaInspector as intentof

from sagas.nlu.patterns import Patterns, print_result
import sagas.tracker_fn as tc

agency=['c_pron', 'c_noun', 'c_propn']

def id_patterns(meta, domains):
    pats=[Patterns(domains, meta, 1).verb(nsubj=agency, obj=agency),
          # $ sid 'Berapa umur kamu?' (en="How old are you?")
          Patterns(domains, meta, 5).verb(behaveof('age', 'n'), amod='c_det'),
          # $ sid 'Bola putih.' (球是白的)
          # notice: 'Bola Dimas putih.'无法匹配这条规则, 因为'Bola Dimas'是flat关系,
          # 针对id中的flat关系, 需要单独处理, 将flat关系的token合并为chunk, 然后再处理这个chunk与外界之间的关系.
          Patterns(domains, meta, 5).verb(behaveof('physical_entity', 'n'), amod=kindof('color', 'n')),
          ]
    print_result(pats)

# ________________________________________________________________________
lang_specs={'id':id_patterns}

def check_langspec(lang, meta, domains, type_name):
    # lang = data['lang']
    if lang in lang_specs:
        # from termcolor import colored
        tc.emp('cyan', f"✁ lang.spec for {lang}. {'-' * 25}")
        lang_specs[lang](meta, domains)
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

if __name__ == '__main__':
    import fire
    fire.Fire(LangspecRules)

