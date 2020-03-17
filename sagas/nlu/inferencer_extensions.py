from typing import Text, Any, Dict, List, Union

from sagas.nlu.inferencer import InferPart, extensions, norm_arg
from sagas.nlu.rules_header import *
from sagas.nlu.utils import get_possible_mean
import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)

all_of = lambda *arg: all([r[1] for r in arg])
def induce_subj(c:InferPart, t:Text):
    from sagas.nlu.nlu_cli import retrieve_word_info
    pat=c.domain.pattern(t)
    r = all_of(pat(nsubj='c_noun'), pat(nsubj=kindof('entity', 'n')))
    if r:
        word=c.word
        rs = retrieve_word_info('get_synsets', word, c.domain.lang, 'n')
        mean = get_possible_mean(rs)
        return 2, f"nsubj=kindof('{mean}')"
    else:
        return [(4, "extract_for('word', 'nsubj')"),
                (2, "nsubj=agency")]

def induce_measure(c:InferPart, t:Text):
    pat = c.domain.pattern(t)
    # print('**', c.name)
    if all_of(pat(**{c.name:kindof('unit_of_measurement', 'n')})):
        return [(4, f"extract_for('number', '{c.name}')"),
                (2, "nsubj=kindof('unit_of_measurement', 'n')")]

def induce_propn(c:InferPart, t:Text):
    pat = c.domain.pattern(t)
    if all_of(pat(**{c.name:'c_propn'})):
        return [(4, f"extract_for('word', '{c.name}')"),
                (2, f"{norm_arg(c.name)}='c_propn'")]

def registry_infer_exts():
    extensions.register_parts('*',{
        'advmod': lambda c,t: (4, "extract_for('word', 'advmod')"),
        'det': lambda c,t: (4, "extract_for('plain', 'det')"),
        'cop': lambda c,t: (2, "cop='c_aux'"),
        'head_amod': lambda c,t: (2, "head_amod=interr('what')"),

        # $ spt 'A cobra fala com o menino.'
        'nsubj': lambda c,t: induce_subj(c, t),
        # obj如果有kindof匹配结果, 下面的注册项不会被执行
        # 'obj': lambda c, t: induce_measure(c, t),

        'nummod': lambda c,t: (4, f"extract_for('plain+number', '{c.name}')"),
        'obl:arg': lambda c, t: induce_propn(c, t),
    })

