from cachetools import cached

from sagas.conf.conf import cf
from sagas.tracker_jupyter import enable_jupyter_tracker
from sagas.nlu.rules_header import *  # must be included
# from sagas.nlu.inspectors import InspectorFixture
from sagas.nlu.patterns import print_result
from sagas.nlu.uni_remote import dep_parse
from sagas.nlu.corenlp_parser import get_chunks
from sagas.nlu.rules_meta import build_meta

from pprint import pprint

enable_jupyter_tracker()
cf.enable_opt('print_not_matched')

@cached(cache={})
def hot_code(rule_code):
    cc = compile(rule_code, '<string>', 'eval')
    return cc

def interp(rule_code, domains, meta):
    return eval(hot_code(rule_code))

def dynamic_rule(data, rule_str, name='_none_', engine=None, graph=False):
    """
    >>> from sagas.tool.dynamic_rules import dynamic_rule
    >>> data = {'lang': 'ja', "sents": '彼のパソコンは便利じゃない。'}
    >>> dynamic_rule(data, "subj('adj',ガ=kindof('artifact', 'n'))", engine='knp')

    :param data:
    :param rule_str:
    :param name:
    :param engine:
    :return:
    """
    import sagas.tracker_fn as tc
    from sagas.kit.analysis_kit import AnalysisKit
    # ft=InspectorFixture()
    # domains, meta=ft.request_domains(data, engine=engine)
    if engine is None:
        engine = cf.engine(data['lang'])
    pipelines = ['predicts']

    tc.emp('magenta', f"({data['lang']}) {data['sents']}")
    doc_jsonify, resp = dep_parse(data['sents'], data['lang'], engine, pipelines)
    if doc_jsonify is not None:
        if len(resp['predicts']) > 0:
            domains_set = resp['predicts']
        else:
            domains_set = get_chunks(doc_jsonify)

        if graph:
            AnalysisKit().console_vis(data['sents'], data['lang'])

        for r in domains_set:
            domains = r['domains']
            meta = build_meta(r, data)
            print(r['type'], meta['word'], meta['lemma'], list(meta.keys()))

            pprint(domains)
            agency = ['c_pron', 'c_noun']
            rs = interp(f"[Patterns(domains, meta, 5, name='{name}').{rule_str}]",
                        domains, meta)
            print_result(rs)

