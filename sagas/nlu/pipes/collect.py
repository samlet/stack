from typing import Text, Any, Dict, List, Union

from blinker import NamedSignal, signal
import rx
from rx import operators as ops
from dataclasses import dataclass

from sagas.nlu.pipes import pred_cond, filter_path, to_token, filter_pos
from sagas.util.collection_util import wrap
import logging
logger = logging.getLogger(__name__)

collect_sig = signal('collect')
@collect_sig.connect
def collect_pos(sender, **kwargs):
    results=[]
    source = rx.of(*kwargs['rs'])
    pos_list:List[Text]=kwargs['data']

    source.pipe(
        filter_pos(pos_list),
        to_token(),
    ).subscribe(
        on_next=lambda value: results.append(value),
        on_error=lambda e: logger.error(e),
        on_completed=lambda: logger.debug("done."),
    )
    return results

