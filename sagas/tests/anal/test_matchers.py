"""
$ pytest -s -v test_matchers.py
"""
import logging

from sagas.nlu.anal_expr import match
from sagas.nlu.anal_data_types import behave_, desc_, phrase_, rel_, path_, _, _1, _2
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

def test_and_or():
    f = build_anal_tree('list some restaurants', 'en', 'stanza')
    f.draw()
    target = f.model().target
    print(target.text, target.types)
    assert target.match('InstitutePlace|场所')
    assert target.match('location: reside|住下; location: eat|吃')
    assert not target.match('+location: reside|住下; location: eat|吃')

def test_desc_matcher():
    f = build_anal_tree('Note the output is a string', 'en', 'stanza')
    f.draw()
    assert f == behave_(_, 'perception|感知', _, _)
    assert f == behave_(_, 'perception|感知', desc_('result|结果', _), _)
    assert not f == behave_(_, 'perception|感知', desc_('food', _), _)

def test_match_expr():
    f = build_anal_tree('Note the output is a string', 'en', 'stanza')
    f.draw()
    r=match(f,
            behave_(_, 'perception|感知', _, _), lambda arg: 'perception',
            behave_(_, 'perception|感知', desc_('result|结果', _), _), lambda arg: arg.text,
            _, None
            )
    assert 'perception'==r

    r = match(f,
              behave_(_, 'unknown', _, _), lambda arg: 'unknown',
              # behave_(_, 'perception|感知', desc_('result|结果', _), _),
              #       lambda arg: [arg.behave.text],
              behave_(_, 'perception|感知', _1<<desc_('result|结果', _), _),
                    lambda arg, v1: [arg.behave.text, v1.target.text],
              _, None
              )
    assert ['Note', 'output'] == r
    # assert ['Note'] == r

    r = match(f/'ccomp'/'nsubj',
              'pos:noun', lambda arg: arg.text,
              _, None
              )
    assert 'output' == r

    r = match(f / 'ccomp' / 'nsubj',
              'pos:pron', lambda arg: arg.text,
              _, None
              )
    assert r is None

    r = match(f,
              behave_(_, 'perception|感知', _1<<_, _), lambda arg, v1: v1.text,
              _, None
              )
    assert 'string' == r

    r = match(f,
              behave_(_, _1<<'perception|感知', _2 << _, _), lambda arg, v1, v2: [v1.text, v2.text],
              _, None
              )
    assert ['Note', 'string'] == r

