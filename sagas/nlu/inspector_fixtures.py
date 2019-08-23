class InspectorFixture(object):
    def __init__(self):
        from sagas.tool.loggers import init_logger
        init_logger()

    def print_table(self, rs, console=True):
        import sagas
        from IPython.display import display
        # df_set=[]
        for r in rs:
            for k,v in r.items():
                if k!='domains':
                    print('%s=%s'%(k,v))
            df = sagas.to_df(r['domains'], ['rel', 'index', 'text', 'lemma', 'children', 'features'])
            # df_set.append(df)
            if console:
                sagas.print_df(df)
            else:
                display(df)

    def request_domains(self, data, print_format='table'):
        import requests
        import json
        from sagas.conf.conf import cf

        print(f".. request is {data}")
        response = requests.post(f'{cf.common_s}/verb_domains', json=data)
        rs = response.json()
        if len(rs)==0:
            print('.. verb_domains servant returns empty set.')
            print('.. request data is', data)
            return None,None

        r = rs[0]
        if print_format=='table':
            self.print_table(rs)
        elif print_format=='jupyter':
            self.print_table(rs, False)
        else:
            print(json.dumps(r, indent=2, ensure_ascii=False))

        domains = r['domains']
        common = {'lemma': r['lemma'], 'stems': r['stems']}
        meta = {'rel': r['rel'], **common, **data}
        return domains, meta
