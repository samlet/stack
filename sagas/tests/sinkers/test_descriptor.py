"""
$ pytest -s -v test_descriptor.py
"""
import logging
import pytest

from sagas.nlu.descriptor import Descriptor


def test_descriptor():
    import sagas.nlu.descriptor
    sagas.nlu.descriptor.logger.setLevel(logging.DEBUG)

    # $ str 'Rezervasyonumu onaylamak istiyorum.'
    results = [{'delivery': 'sentence',
                'inspector': 'specs_of',
                'part': 'verb:_',
                'pattern': 'behave {verb.obj:cat} for {verb.obj.obj:cat}, modal '
                           '{verb._:cat}, personal {verb._:personal}',
                'provider': 'default',
                'value': {'category': 'request',
                          'pos': 'v',
                          'subs': [{'candidates': 'request',
                                    'substitute': 'request',
                                    'word': 'iste'}],
                          'words': ['istiyorum/iste']}},
               {'delivery': 'slot',
                'inspector': 'pipes',
                'part': 'verb:obj/obj',
                'pattern': 'behave {verb.obj:cat} for {verb.obj.obj:cat}, modal '
                           '{verb._:cat}, personal {verb._:personal}',
                'provider': 'cat/cat_proc',
                'value': [{'cat': 'reservation',
                           'path': '/obj/obj',
                           'pos': 'noun',
                           'trans': 'reservation',
                           'value': 'reservation',
                           'word': 'rezervasyon'}]},
               {'delivery': 'sentence',
                'inspector': 'kind_of',
                'part': 'verb:obj',
                'pattern': 'behave {verb.obj:cat} for {verb.obj.obj:cat}, modal '
                           '{verb._:cat}, personal {verb._:personal}',
                'provider': 'default',
                'value': {'category': 'approve', 'pos': '*', 'word': 'onaylamak/onayla'}},
               {'delivery': 'slot',
                'inspector': 'extract_comps',
                'part': 'verb:_',
                'pattern': 'behave {verb.obj:cat} for {verb.obj.obj:cat}, modal '
                           '{verb._:cat}, personal {verb._:personal}',
                'provider': 'feats',
                'value': [{'Aspect': 'Prog',
                           'Mood': 'Ind',
                           'Number': 'Sing',
                           'Person': '1',
                           'Polarity': 'Pos',
                           'Polite': 'Infm',
                           'Tense': 'Pres'}]}]
    dsp=Descriptor()
    patt='behave {verb.obj:cat} for {verb.obj.obj:cat},' \
         ' modal {verb._:cat}, personal {verb._:personal}'
    assert dsp.render(patt, results)=='behave approve for reservation, modal request, personal 1_Sing'


