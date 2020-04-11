"""
$ pytest -s -v test_matchers.py
"""
import logging

from sagas.nlu.anal_data_types import behave_, desc_, phrase_, rel_, path_, _
from sagas.nlu.anal import build_anal_tree, Doc, AnalNode
from sagas.nlu.anal_corpus import model_info
import sagas.nlu.anal

sagas.nlu.anal.logger.setLevel(logging.DEBUG)

def test_behave_matcher():
    f = build_anal_tree('We expect them to change their minds', 'en', 'stanza')
    f.draw()
    model = f.rels('xcomp')[0].model()
    model_info(model)

    assert (f/'nsubj').match(_)
    assert (f/'obj').match('pos:pron')
    assert (f / 'xcomp').match(behave_(_, 'change|变', 'mind'))
    # assert (f/'xcomp').match(behave_(_, 'change|变', 'mind') |
    #                          behave_(_, 'change|变', 'mental|精神'))
    assert f.match(behave_(_, 'expect|期望', _, _))
    assert not f.match(behave_(_, 'love', _, _))
    assert f.match(behave_(_, 'expect|期望', _, _,
                           rel_('xcomp')==behave_(_, 'change|变', 'mind')))

    assert f==behave_(_, 'expect|期望', _, _)

def test_desc_matcher():
    f = build_anal_tree('Note the output is a string', 'en', 'stanza')
    f.draw()
    assert f == behave_(_, 'perception|感知', _, _)
    assert f == behave_(_, 'perception|感知', desc_('result|结果', _), _)
    assert not f == behave_(_, 'perception|感知', desc_('food', _), _)

