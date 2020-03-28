from typing import Text, Any, Dict, List, Union

from blinker import NamedSignal, signal
import rx
from rx import operators as ops
from dataclasses import dataclass

from sagas.nlu.pipes import pred_cond, filter_path, to_token
from sagas.util.collection_util import wrap
import logging
logger = logging.getLogger(__name__)

def is_interr(word, interr, lang):
    from sagas.nlu.inspectors_dataset import get_interrogative
    return get_interrogative(word, lang)==interr

def pred_interr(cand, lang):
    return rx.pipe(
        ops.filter(lambda t: is_interr(t.lemma, cand, lang)),)

interr_sig=signal('interr')
@interr_sig.connect
def interr_proc(sender, **kwargs):
    results=[]

    source = rx.of(*kwargs['rs'])
    cond:pred_cond=kwargs['data']
    lang=kwargs['lang']
    # ['part']      '/conj/cc'
    # ['interr']    'but'
    # ['lang']      'hu'

    source.pipe(
        filter_path(cond.part),
        pred_interr(cond.cond, lang),
        to_token(cond.cond),
    ).subscribe(
        on_next=lambda value: results.append({'interr':cond.cond, **value}),
        on_error=lambda e: logger.error(e),
        on_completed=lambda: logger.debug('done.'),
    )

    return results
