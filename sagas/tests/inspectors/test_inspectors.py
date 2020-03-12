"""
$ pytest -s -v test_inspectors.py
"""
import pytest

from sagas.nlu.inspector_common import Context
from sagas.nlu.parse_client_helper import build_context
from sagas.nlu.rules_header import *
from pprint import pprint

@pytest.mark.parametrize(
    "data, dominator, insp",
    [
        ({'lang': 'en', "sents": 'I want to watch a movie'},
         'verb', behaveof('want', 'v')),
        ({'lang': 'pt', "sents": 'Nós comemos massa no restaurante.'},
         'verb', behaveof('eat', 'v')),
    ],
)
def test_behaveof(data, dominator, insp):
    for ctx,serv in build_context(data, dominator, name='_test_'):
        r = serv(insp)
        assert r[1]


@pytest.mark.parametrize(
    "data, dominator, insp",
    [
        ({'lang': 'pt', "sents": 'Nós comemos massa no restaurante.'},
         'verb', dict(obl=kindof('building', 'n'))),
    ],
)
def test_kindof(data, dominator, insp):
    for ctx,serv in build_context(data, dominator, name='_test_'):
        r = serv(**insp)
        assert r[1]

@pytest.mark.parametrize(
    "data, dominator, insp",
    [
        ({'lang': 'pt', "sents": 'Eu preciso disso até amanhã.'},
         'verb', dict(advmod=dateins('time'))),
        ({'lang': 'pt', "sents": 'Nós não vemos nossos pais desde ontem.'},
         'verb', dict(advmod=dateins('time'))),
    ],
)
def test_dateins(data, dominator, insp):
    for ctx,serv in build_context(data, dominator, name='_test_'):
        r = serv(**insp)
        assert r[1]

@pytest.mark.parametrize(
    "data, dominator, insp",
    [
        ({'lang': 'pt', "sents": 'Ele está entre meu irmão e minha irmã.'},
         'aux', dict(case='c_adp')),
    ],
)
def test_aux_pos(data, dominator, insp):
    for ctx,serv in build_context(data, dominator, name='_test_'):
        r = serv(**insp)
        assert r[1]


