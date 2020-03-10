"""
$ pytest -s -v test_inspector_clauses.py
"""
import pytest

from sagas.nlu.inspector_common import Context
from sagas.nlu.parse_client_helper import build_context
from sagas.nlu.rules_header import *
from pprint import pprint

def test_cla_expr():
    from sagas.nlu.inspector_common import cla_meta
    from sagas.nlu.inspector_clauses import cla_expr
    e = cla_expr('verb:obl', cop={'be'})
    assert e.run('', cla_meta('Ela negou ser minha mãe.', 'pt'))

@pytest.mark.parametrize(
    "data, insp",
    [
        ({'lang': 'pt', "sents": 'Ela negou ser minha mãe.'},
         clauses(all, cla_expr('verb:obl', cop={'be'}))),
    ],
)
def test_clauses(data, insp):
    for ctx,_ in build_context(data, 'verb', name='_test_'):
        assert insp.run('', ctx)


