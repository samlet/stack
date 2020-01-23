from typing import Text, Any, Dict, List
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
from sagas.nlu.inspector_registry import ci  # must be included

enable_jupyter_tracker()
cf.enable_opt('print_not_matched')

@cached(cache={})
def hot_code(rule_code):
    cc = compile(rule_code, '<string>', 'eval')
    return cc

def interp(rule_code, domains, meta):
    return eval(hot_code(rule_code))

class DynamicRules(object):
    def __init__(self):
        self.result_set=[]

    def predict(self, data:Dict[Text, Any], rule_str:Text, name='_none_', engine=None,
                     graph=False, operator=all) -> bool:
        """
        >>> from sagas.tool.dynamic_rules import DynamicRules
        >>> data = {'lang': 'ja', "sents": '彼のパソコンは便利じゃない。'}
        >>> DynamicRules().predict(data, "subj('adj',ガ=kindof('artifact', 'n'))", engine='knp')

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

            check_r=[]
            for r in domains_set:
                domains = r['domains']
                meta = build_meta(r, data)
                print(r['type'], meta['word'], meta['lemma'], list(meta.keys()))

                pprint(domains)
                agency = ['c_pron', 'c_noun']
                rs = interp(f"[Patterns(domains, meta, 5, name='{name}').{rule_str}]",
                            domains, meta)
                print_result(rs)
                results = [el for r in rs for el in r[3].results if r[1]]  # r[1] is true/false
                self.result_set.extend(results)

                check_r.append(operator([r[1] for r in rs]))

            return operator(check_r)

        return False