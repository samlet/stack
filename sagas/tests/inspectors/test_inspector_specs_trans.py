"""
$ pytest -s -v test_inspector_specs_trans.py
"""
from sagas.nlu.rules_header import *
import logging

def test_spec_trans():
    from sagas.nlu.parse_client_helper import build_context
    from sagas.nlu.inspector_wordnet import logger

    logger.setLevel(logging.DEBUG) # only display debug message when fail
    # Please drive slowly.
    data = {'lang': 'af', "sents": 'Ry asseblief stadiger.'}
    ctx, pat = next(build_context(data, 'verb', name='_test_'))

    all_of = lambda *arg: all([r[1] for r in arg])
    r = all_of(pat(advmod=specs_trans('*', 'slow', 'fast').opt(raw_fmt=raw_fmt_pos)))
    assert r
    r = all_of(pat(advmod=specs_trans('*', 'slow', 'fast').opt(trans_idx=0)))
    assert r

def test_spec_trans_aux():
    from sagas.nlu.parse_client_helper import build_context
    from sagas.nlu.inspector_wordnet import logger

    logger.setLevel(logging.DEBUG) # only display debug message when fail
    # I’m in a hurry.
    data = {'lang': 'af', "sents": 'Ek is haastig.'}
    ctx, pat = next(build_context(data, 'cop', name='_test_'))

    all_of = lambda *arg: all([r[1] for r in arg])
    r = all_of(pat(specs_trans('*', 'hurriedly').opt(raw_fmt=raw_fmt_pos),))
    assert r
