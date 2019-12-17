from typing import Any, Callable, Dict, List, Text, Optional, Type
import logging
from sagas.nlu.inspectors import NegativeWordInspector as negative
from sagas.nlu.inspectors import DateInspector as dateins
from sagas.nlu.inspectors import EntityInspector as entins
from sagas.nlu.inspectors import MatchInspector as matchins
from sagas.nlu.inspector_wordnet import PredicateWordInspector as kindof
from sagas.nlu.inspector_wordnet import VerbInspector as behaveof
from sagas.nlu.inspector_rasa import RasaInspector as intentof
from sagas.nlu.lang_spec_intf import LangSpecBase, agency

from sagas.nlu.patterns import Patterns, print_result
import sagas.tracker_fn as tc
from sagas.nlu.rules_meta import build_meta

# ________________________________________________________________________
logger = logging.getLogger(__name__)

def exec_rules_by_type(ci:LangSpecBase, type_name):
    mappings={'verb_domains':ci.verb_rules,
              'aux_domains':ci.aux_rules,
              'subj_domains':ci.subject_rules,
              'predicate':ci.predicate_rules,
              'root_domains':ci.root_rules,
              }
    mappings[type_name]()
    # ci.root_rules()

def parse_sents(meta):
    from sagas.nlu.uni_remote import dep_parse, parse_and_cache
    # 'lang': lang, "sents": sents, 'engine': engine
    # doc_jsonify, _ = dep_parse(meta['sents'], meta['lang'], meta['engine'])
    doc_jsonify, resp = parse_and_cache(meta['sents'], meta['lang'], meta['engine'])
    return doc_jsonify, resp

def class_from_module_path(module_path: Text) -> Any:
    """Given the module name and path of a class, tries to retrieve the class.
    The loaded class can be used to instantiate new objects. """
    import importlib

    # load the module, will raise ImportError if module cannot be loaded
    module_name, _, class_name = module_path.rpartition(".")
    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    return getattr(m, class_name)

def load_mods(mod_files):
    import json

    lang_mods={}
    for mod_file in mod_files:
        print(f'.. load mod {mod_file}')
        with open(mod_file) as f:
            cfg=json.load(f)
            for k,v in cfg.items():
                if k in lang_mods:
                    lang_mods[k].extend(v)
                else:
                    lang_mods[k]=v

    lang_mod_classes={}
    for k,v in lang_mods.items():
        lang_mod_classes[k]=[class_from_module_path(c) for c in v]
    return lang_mod_classes

class LangSpecs(object):
    def __init__(self):
        import glob
        # self.lang_specs = {'id': [Rules_id], 'de': [Rules_de], }
        # scan conf/mod_*.json
        self.lang_specs=load_mods(glob.glob('/pi/stack/conf/mod_*.json'))

    def check_langspec(self, lang, meta, domains, type_name) -> Dict:
        # lang = data['lang']
        mod_rs={}
        if lang in self.lang_specs:
            doc, _=parse_sents(meta)
            # from termcolor import colored
            tc.emp('cyan', f"✁ lang.spec for {lang}.{type_name} {'-' * 25}")
            for c in self.lang_specs[lang]:
                ci=c(meta, domains, doc=doc)
                exec_rules_by_type(ci, type_name)
                ci.execute()

                mod_rs[c.__name__]=ci.matched
        else:
            tc.emp('red', f'no special patterns for lang {lang}')
        return mod_rs

langspecs=LangSpecs()

def rs_repr(rs, data):
    from pprint import pprint
    feats=[]
    for serial, r in enumerate(rs):
        # common = {'lemma': r['lemma'], 'word': r['word'],
        #           'stems': r['stems']}
        # meta = {'rel': r['rel'], **common, **data}
        meta=build_meta(r, data)
        lang=data['lang']

        # if lang in lang_specs:
        #     lang_specs[lang](meta, r['domains'])
        # else:
        #     tc.emp('red', f'no special patterns for lang {lang}')
        mod_rs=langspecs.check_langspec(lang, meta, r['domains'], type_name = r['type'])
        if len(mod_rs)>0:
            for mod,matched in mod_rs.items():
                matched_info = {k: len(v.results) for k, v in matched.items()}
                for ctx in matched.values():  # matched value type is Context
                    pprint(ctx.results)
                tc.emp('yellow', f"{mod} -> {matched_info}")
                feats.extend(matched.keys())

    tc.emp('green', f"features -> {feats}")

class LangspecRules(object):
    def __init__(self):
        pass

    def langspec(self, sents, lang='en', engine='corenlp'):
        """
        $ python -m sagas.nlu.rules_lang_spec langspec 'Berapa umur kamu?' id
        $ python -m sagas.nlu.rules_lang_spec langspec 'Siapa yang menulis laporan ini?' id
            ♯ matched id rules: {'ask_event': 0}
            features -> ['ask_event']
        $ python -m sagas.nlu.rules_lang_spec langspec 'Die Nutzung der Seite ist kostenlos.' de
        $ python -m sagas.nlu.rules_lang_spec langspec 'I want to play music.' en

        :param sents:
        :param lang:
        :param engine:
        :return:
        """
        from sagas.nlu.uni_remote import dep_parse
        from sagas.nlu.corenlp_parser import get_chunks

        pipelines = ['predicts']
        meta={'lang': lang, "sents": sents, 'engine': engine, 'pipelines': pipelines}
        # doc_jsonify, resp = dep_parse(sents, lang, engine, pipelines)
        doc_jsonify, resp =parse_sents(meta)
        rs = get_chunks(doc_jsonify)
        rs_repr(rs, data=meta)

    def langspec_id(self, sents, engine='corenlp'):
        """
        $ python -m sagas.nlu.rules_lang_spec langspec_id 'Berapa umur kamu?'
        :param sents:
        :param engine:
        :return:
        """
        from sagas.nlu.uni_remote import dep_parse
        from sagas.nlu.corenlp_parser import get_chunks
        from sagas.nlu.rules_lang_spec_de import Rules_de
        from sagas.nlu.rules_lang_spec_id import Rules_id

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
            c=Rules_id(meta, r['domains'], doc=doc_jsonify)
            c.root_rules()
            c.execute()

if __name__ == '__main__':
    import fire
    from sagas.tool.loggers import init_logger

    init_logger()
    fire.Fire(LangspecRules)

