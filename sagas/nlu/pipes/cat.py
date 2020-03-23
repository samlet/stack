from typing import Text, Any, Dict, List, Union

from blinker import NamedSignal, signal
import rx
from rx import operators as ops
from dataclasses import dataclass

from sagas.nlu.pipes import pred_cond, filter_path, to_token
from sagas.util.collection_util import wrap, to_obj
import logging
logger = logging.getLogger(__name__)

pos_map={'adj': 'adjective',
         'adp': 'adposition',
         'adv': 'adverb',
         'cconj': 'conjunction',
         'sconj': 'conjunction',
        }
def get_pos(upos):
    pos=upos.lower()
    return pos_map[pos] if pos in pos_map else pos

pos_abbrev={'adj': 'a', 'noun':'n', 'verb':'v'}
def get_abbrev(upos):
    pos=upos.lower()
    return pos_abbrev[pos] if pos in pos_abbrev else '*'

def trans(word, lang, pos):
    from sagas.nlu.translator import translate, with_words, WordsObserver
    pos=get_pos(pos)
    logger.debug(f"trans {word}, {lang}, {pos}")
    r, t = translate(word, source=lang, target='en', options={'get_pronounce'}, tracker=with_words())
    candidates=t.observer(WordsObserver).get_axis(r, pos)
    return candidates

cat_sig=signal('cat')
@cat_sig.connect
def cat_proc(sender, **kwargs):
    from sagas.nlu.utils import predicate, get_word_sets

    results=[]

    source = rx.of(*kwargs['rs'])
    lang = kwargs['lang']
    cond:pred_cond=kwargs['data']
    logger.debug(f"pred pos: {cond}")

    kind=cond.cond
    logger.debug(f"lang: {lang}, cond: {cond}")
    source.pipe(
        filter_path(cond.part),
        ops.map(lambda t: to_obj({'word': t.text if t.upos.lower() in ['adj'] else t.lemma, **t})),
        ops.map(lambda t: to_obj({'trans': trans(t.word, lang, t.upos), **t})),
        ops.filter(lambda t: predicate(kind, t.trans, 'en', '*')),

        ops.map(lambda t: {'path':t.path,
                           'word': t.word,
                           'trans': t.trans,
                           'cat': kind,
                           'pos': t.upos.lower()}),
    ).subscribe(
        on_next=lambda value: results.append({**value}),
        on_error=lambda e: logger.error(e),
    )
    logger.debug(f"result: {results}")
    return results

