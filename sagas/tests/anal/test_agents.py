"""
$ pytest -s -v test_agents.py
"""
import pytest

from sagas.modules import match_agents
from sagas.nlu.anal import build_anal_tree
from pprint import pprint

@pytest.mark.parametrize(
    "sents, lang, engine",
    [
        ('list some restaurants', 'en', 'analspa'),
    ])
def test_restaurants(sents, lang, engine):
    f = build_anal_tree(sents, lang, engine)
    f.draw()
    target = f.model().target
    agents=match_agents(target)
    assert len(agents)==1

    rs=agents[0](f)
    pprint(rs)
    assert len(rs)>1

