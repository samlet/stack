from typing import Text, Any, Dict, List, Union

from sagas.nlu.inferencer import InferPart, extensions
from sagas.nlu.rules_header import *
from sagas.nlu.utils import get_possible_mean
import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)

def induce_subj(c:InferPart, t:Text):
    from sagas.nlu.nlu_cli import retrieve_word_info
    pat=c.domain.pattern(t)
    all_of = lambda *arg: all([r[1] for r in arg])
    r = all_of(pat(nsubj='c_noun'), pat(nsubj=kindof('entity', 'n')))
    if r:
        word=c.word
        rs = retrieve_word_info('get_synsets', word, c.domain.lang, 'n')
        mean = get_possible_mean(rs)
        return 2, f"nsubj=kindof('{mean}')"
    else:
        return [(4, "extract_for('plain', 'nsubj')"),
                (2, "nsubj=agency")]

def registry_infer_exts():
    extensions.register_parts('*',{
        # $ spt 'A cobra fala com o menino.'
        'nsubj': lambda c,t: induce_subj(c, t),
    })

