"""
$ pytest -s -v test_inspector_expr.py
"""
import logging
from sagas.nlu.parse_client_helper import build_context
from sagas.nlu.rules_header import *
from sagas.nlu import inspectors, inspector_pipes
from pprint import pprint
import pytest

all_of = lambda *arg: all([r[1] for r in arg])

@pytest.mark.parametrize(
    "sents, lang",
    [
        ('A magas tanár nem angol, hanem magyar.', 'hu'),
    ],
)
def test_pipes_interr_and_cat(sents, lang):
    from sagas.nlu.pipes import cat
    inspectors.logger.setLevel(logging.DEBUG)
    inspector_pipes.logger.setLevel(logging.DEBUG)
    cat.logger.setLevel(logging.DEBUG)

    data = {'lang': lang, "sents": sents}
    ctx, pat = next(build_context(data, 'cop', name='_test_'))

    # rs=pat(pipes(interr=pred_cond('/conj/cc', 'but')),
    #        pipes(pos=pred_cond('/conj', ['adj'])),
    #        pipes(cat=pred_cond('/conj', 'person')),
    #        )
    rs = pat(ins().interr('/conj/cc')=='but',
             ins().pos('/conj')==['adj'],
             ins().cat('/conj')=='person',
             )
    pprint((rs[1], rs[0], rs[3].results))
    assert all_of(rs)

