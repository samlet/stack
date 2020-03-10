"""
$ pytest -s -v test_inspector_cust.py
"""
import pytest

from sagas.nlu.inspector_common import Context
from sagas.nlu.parse_client_helper import build_context
from sagas.nlu.rules_header import *
from pprint import pprint

@pytest.mark.parametrize(
    "data, dominator, insp",
    [
        ({'lang': 'pt', "sents": 'Desde quando você gosta de abacaxi?'},
         'verb', dict(advmod=cust(check_interr, lambda w: w == 'since_when'))),
        ({'lang': 'pt', "sents": 'Por que você não perguntou?'},
         'verb', dict(obl=cust(check_interr, lambda w: w=='why'))),
    ],
)
def test_cust(data, dominator, insp):
    for ctx,serv in build_context(data, dominator, name='_test_'):
        r = serv(**insp)
        assert r[1]
