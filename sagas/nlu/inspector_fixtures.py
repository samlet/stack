import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)
class InspectorFixture(object):
    def __init__(self):
        from sagas.tool.loggers import init_logger
        init_logger()

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

    def request_domains(self, data, print_format='table', engine='corenlp'):
        import requests
        import json
        from sagas.conf.conf import cf

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
        common = {'lemma': r['lemma'], 'word': r['word'],
                  'stems': r['stems']}
        meta = {'rel': r['rel'], **common, **data}
        return domains, meta

