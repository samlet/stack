from sagas.nlu.inspectors import NegativeWordInspector as negative
from sagas.nlu.inspectors import DateInspector as dateins
from sagas.nlu.inspectors import EntityInspector as entins
from sagas.nlu.inspector_wordnet import PredicateWordInspector as kindof
from sagas.nlu.inspector_wordnet import VerbInspector as behaveof
from sagas.nlu.inspector_rasa import RasaInspector as intentof

from sagas.nlu.patterns import Patterns, print_result
agency=['c_pron', 'c_noun', 'c_propn']

def id_patterns(meta, domains):
    pats=[Patterns(domains, meta, 1).verb(nsubj=agency, obj=agency),
          # $ sid 'Berapa umur kamu?' (en="How old are you?")
          Patterns(domains, meta, 5).verb(behaveof('age', 'n'), amod='c_det'),
          ]
    print_result(pats)

# ________________________________________________________________________
lang_specs={'id':id_patterns}

def check_langspec(lang, meta, domains):
    # lang = data['lang']
    if lang in lang_specs:
        from termcolor import colored
        print(colored(f"✁ lang.spec for {lang}. {'-' * 25}", 'cyan'))
        lang_specs[lang](meta, domains)
    else:
        print(f'no special patterns for lang {lang}')


def rs_repr(rs, data):
    for serial, r in enumerate(rs):
        common = {'lemma': r['lemma'], 'stems': r['stems']}
        meta = {'rel': r['rel'], **common, **data}
        lang=data['lang']
        if lang in lang_specs:
            lang_specs[lang](meta, r['domains'])
        else:
            print(f'no special patterns for lang {lang}')

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

