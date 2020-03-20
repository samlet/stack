"""
$ pytest -s -v test_inspector_axis.py
"""
import logging
import sagas.nlu.inspectors
from sagas.nlu.parse_client_helper import build_context


def test_axis():
    from sagas.nlu.rules_lang_spec_hi import axis
    sagas.nlu.inspectors.logger.setLevel(logging.DEBUG)
    sagas.nlu.rules_lang_spec_hi.logger.setLevel(logging.DEBUG)

    data = {'lang': 'hi', "sents": 'मैं सेब खाता हूं'}
    ctx, pat = next(build_context(data, 'verb', name='_test_'))

    all_of = lambda *arg: all([r[1] for r in arg])
    r = all_of(pat(axis('obj').inherit('khadya phala|edible fruits'), ))
    assert r

