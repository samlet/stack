"""
$ pytest -s -v test_term.py
"""
import pytest

from sagas.modules import match_agents
from sagas.nlu.anal import build_anal_tree
from pprint import pprint

@pytest.mark.parametrize(
    "sents, lang, engine",
    [
        ('你在北京的公司的主要传真号码是什么', 'zh', 'analspa'),
        ('你在北京的公司的主要传真号码是什么', 'zh', 'analz'),
    ])
def test_term(sents, lang, engine):
    f = build_anal_tree(sents, lang, engine)
    f.draw()
    # target = f.model().target
    assert (f/'nsubj').is_term('typ')

