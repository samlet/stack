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


def dynamic_rule(data, rule_str, name='_none_', engine=None):
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
    # ft=InspectorFixture()
    # domains, meta=ft.request_domains(data, engine=engine)
    if engine is None:
        engine = cf.engine(data['lang'])
    pipelines = ['predicts']
    doc_jsonify, resp = dep_parse(data['sents'], data['lang'], engine, pipelines)
    if doc_jsonify is not None:
        if len(resp['predicts']) > 0:
            domains_set = resp['predicts']
        else:
            domains_set = get_chunks(doc_jsonify)

        for r in domains_set:
            domains = r['domains']
            meta = build_meta(r, data)
            print(r['type'], meta['word'], meta['lemma'], list(meta.keys()))
            pprint(domains)
            agency = ['c_pron', 'c_noun']
            rs = eval(f"[Patterns(domains, meta, 5, name='{name}').{rule_str}]")
            print_result(rs)

