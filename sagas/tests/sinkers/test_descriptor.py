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
                'part': '_',
                'pattern': 'behave_reservation',
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
                'pattern': 'behave_reservation',
                'provider': 'cat/cat_proc',
                'value': [{'cat': 'reservation',
                           'path': '/obj/obj',
                           'pos': 'noun',
                           'trans': 'reservation',
                           'value': 'reservation',
                           'word': 'rezervasyon'}]},
               {'delivery': 'sentence',
                'inspector': 'kind_of',
                'part': 'obj',
                'pattern': 'behave_reservation',
                'provider': 'default',
                'value': {'category': 'approve', 'pos': '*', 'word': 'onaylamak/onayla'}}]
    dsp=Descriptor()
    patt = 'behave {obj:_} for {obj:/obj}, modal {_:_}'
    assert dsp.render(patt, results)=='behave approve for reservation, modal request'


