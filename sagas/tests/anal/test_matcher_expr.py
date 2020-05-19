"""
$ pytest -s -v test_matcher_expr.py
"""
import logging

from sagas.nlu.anal_expr import match
from sagas.nlu.anal_data_types import behave_, desc_, phrase_, rel_, path_, _, _1, _2
from sagas.nlu.anal import build_anal_tree, Doc, AnalNode
from sagas.nlu.anal_corpus import model_info
import sagas.nlu.anal

sagas.nlu.anal.logger.setLevel(logging.DEBUG)

def test_match_expr():
    f = build_anal_tree('Note the output is a string', 'en', 'stanza')
    f.draw()

    r = match(f,
              behave_(_, _1 << 'perception|感知', _2 << _, _), lambda arg, v1, v2: [v1.text, v2.text],
              _, None
              )
    assert ['Note', 'string'] == r

    r = match(f,
              behave_(_, _1<<'unknown', _2<<_, _), lambda *args: 'unknown',
              # behave_(_, 'perception|感知', _1 << desc_('result|结果', _), _),
              #       lambda arg, v1: [arg.behave.text, v1.target.text],
              behave_(_, _1 << 'perception|感知', desc_('result|结果', _), _),
                    lambda arg, v1: [arg.behave.text, v1.text],
              behave_(_, _1 << 'unknown2', _2 << _, _), lambda *args: 'unknown2',
              _, None
              )
    assert ['Note', 'Note'] == r
    assert 0==len(_1.reqs)

def test_match_embed_expr():
    f = build_anal_tree('We expect them to change their minds', 'en', 'stanza')
    f.draw()
    r = match(f,
              behave_(_, _1<<'expect|期望', _, _,
                      rel_('xcomp') == behave_(_, _2<<'change|变', 'mind')),
                lambda arg, v1, v2: [v1.text, v2.text],
              _, None
              )
    assert ['expect', 'change'] == r

def test_match_absent_part():
    f = build_anal_tree('Nós estudamos.', 'pt', 'stanza')
    f.draw()
    r = match(f,
              behave_(_, _1 << 'study', _2 << _, _), lambda arg, v1, v2: [v1.text, v2.text],
              behave_(_, _1 << 'study', _, _), lambda arg, v1: [v1.text],
              behave_(_, _1 << 'learn', _2 << _, _), lambda arg, v1, v2: [v1.text, v2.text],
              _, None
              )
    assert ['estudamos'] == r

