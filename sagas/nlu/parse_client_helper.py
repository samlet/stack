from typing import Text, Any, Dict, List, Union


def build_context(data:Dict[Text,Text], dominator:Text, name='_noname_'):
    from sagas.nlu.inferencer import parse
    from sagas.nlu.inspector_common import Context
    from sagas.nlu.rules_meta import build_meta
    from sagas.nlu.patterns import Patterns

    rs = parse(data)
    for serial, r in enumerate(rs):
        # type_name = r['type']
        # theme = type_name.split('_')[0]
        domains = r['domains']
        # print(type_name)
        meta = build_meta(r, data)
        ctx = Context(meta, domains, name=name)
        pat = Patterns(domains, meta, 5, name=name)
        serv = pat.prepare(dominator)
        yield ctx, serv

