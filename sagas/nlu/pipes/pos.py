from typing import Text, Any, Dict, List, Union

from blinker import NamedSignal, signal
import rx
from rx import operators as ops
from dataclasses import dataclass

from sagas.nlu.pipes import pred_cond, filter_path, to_token
from sagas.util.collection_util import wrap
import logging
logger = logging.getLogger(__name__)

pos_sig=signal('pos')
@pos_sig.connect
def pos_proc(sender, **kwargs):
    results=[]

    source = rx.of(*kwargs['rs'])
    cond:pred_cond=kwargs['data']
    logger.debug(f"pred pos: {cond}")

    source.pipe(
        filter_path(cond.part),
        ops.filter(lambda t: t.upos.lower() in cond.cond),
        to_token(cond.cond),
    ).subscribe(
        on_next=lambda value: results.append({**value}),
        on_error=lambda e: logger.error(e),
    )

    return results

