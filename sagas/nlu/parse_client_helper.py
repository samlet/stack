from typing import Text, Any, Dict, List, Union
from sagas.nlu.inspector_common import Context
from sagas.nlu.patterns import Patterns
from sagas.nlu.rules_meta import build_meta
from sagas.nlu.inspectors_dataset import get_interrogative

def build_context(data:Dict[Text,Text], dominator:Text, name='_noname_', **kwargs):
    from sagas.nlu.inferencer import parse

    rs = parse(data)
    for serial, r in enumerate(rs):
        # type_name = r['type']
        # theme = type_name.split('_')[0]
        domains = r['domains']
        # print(type_name)
        meta = build_meta(r, data)
        ctx = Context(meta, domains, name=name)
        pat = Patterns(domains, meta, 5, name=name).opts(**kwargs)
        serv = pat.prepare(dominator)
        yield ctx, serv

def check_interr(key:Text, ctx:Context, check_fn, lang='pt') -> bool:
    for stem in ctx.stem_pieces(key):
        interr=get_interrogative(stem, lang)
        if interr and check_fn(interr):
            return True
    return False

