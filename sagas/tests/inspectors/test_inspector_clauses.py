"""
$ pytest -s -v test_inspector_clauses.py
"""
from sagas.nlu.inferencer import parse
from sagas.nlu.inspector_common import Context
from sagas.nlu.rules_header import *
from sagas.nlu.rules_meta import build_meta
from pprint import pprint

def test_cla_expr():
    from sagas.nlu.inspector_common import cla_meta
    from sagas.nlu.inspector_clauses import cla_expr
    e = cla_expr('verb:obl', cop={'be'})
    assert e.run('', cla_meta('Ela negou ser minha mãe.', 'pt'))

def test_clauses():
    from sagas.tool.misc import translit_chunk, display_synsets, target_lang
    data = {'lang': 'pt', "sents": 'Ela negou ser minha mãe.'}
    rs = parse(data)
    # for serial, r in enumerate(rs):
    r=rs[0]

    type_name = r['type']
    theme = type_name.split('_')[0]
    domains=r['domains']
    # print(type_name)
    meta = build_meta(r, data)
    pprint(meta)
    ctx = Context(meta, domains, name='_test_')
    insp=clauses(all, cla_expr('verb:obl', cop={'be'}))
    assert insp.run('', ctx)


