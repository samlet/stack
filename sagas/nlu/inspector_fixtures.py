from typing import Text, Dict, Any

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)
class InspectorFixture(object):
    def __init__(self):
        pass

    def print_table(self, rs):
        import sagas
        # from IPython.display import display
        # df_set=[]
        for r in rs:
            for k,v in r.items():
                if k!='domains':
                    logging.debug('%s=%s'%(k,v))
            df = sagas.to_df(r['domains'], ['rel', 'index', 'text', 'lemma', 'children', 'features'])
            # df_set.append(df)
            # if console:
            #     sagas.print_df(df)
            # else:
            #     display(df)
            tc.dfs(df)

    def request_domains(self, data:Dict[Text, Any], print_format='table', engine=None):
        import requests
        import json
        from sagas.conf.conf import cf
        from sagas.nlu.rules_meta import build_meta

        if engine is None:
            engine=cf.engine(data['lang'])
        data['engine']=engine
        tc.info(f".. request is {data}")

        response = requests.post(f'{cf.servant(engine)}/verb_domains', json=data)
        rs = response.json()
        if len(rs)==0:
            tc.info('.. verb_domains servant returns empty set.')
            tc.info('.. request data is', data)
            return None,None

        r = rs[0]
        # if print_format=='table':
        #     self.print_table(rs)
        # elif print_format=='jupyter':
        #     self.print_table(rs, False)
        if print_format!='json':
            self.print_table(rs)
        else:
            tc.info(json.dumps(r, indent=2, ensure_ascii=False))

        domains = r['domains']
        # common = {'lemma': r['lemma'], 'word': r['word'],
        #           'stems': r['stems']}
        # meta = {'rel': r['rel'], **common, **data}

        meta = build_meta(r, data)
        return domains, meta

    def analyse_domains(self, sents, lang, engine=None, domain=None):
        from sagas.nlu.ruleset_procs import cached_chunks, get_main_domains
        from sagas.conf.conf import cf

        engine = cf.engine(lang) if engine is None else engine
        if domain is None:
            domain, domains = get_main_domains(sents, lang, engine)
        else:
            chunks = cached_chunks(sents, lang, engine)
            domains = chunks[domain]
        return domains
