"""
$ pytest -s -v test_term_ref.py
"""
import pytest

from sagas.modules import match_agents
from sagas.nlu.anal import build_anal_tree
from pprint import pprint

@pytest.mark.parametrize(
    "sents, lang, engine",
    [
        ('this is a digital good', 'en', 'analspa'),
    ])
def test_term(sents, lang, engine):
    f = build_anal_tree(sents, lang, engine)
    f.draw()
    assert f.is_term('ref')
    pprint(f.links[0].as_json())
    assert f.links[0].name=='ProductType'

