from typing import Text, Any, Dict, List, Union

from blinker import NamedSignal, signal
import rx
from rx import operators as ops
from dataclasses import dataclass

from sagas.nlu.pipes import pred_cond, filter_path, to_token, filter_pos, sense_cond
from sagas.util.collection_util import wrap, to_obj
import logging

from sagas.zh.hownet_helper import get_trees

logger = logging.getLogger(__name__)

def filter_sense(data:sense_cond):
    exprs=[]
    if data.roles:
        # print(data.roles)
        exprs.append(ops.filter(lambda t: any([st.has_role(**data.roles) for st in t.sense])))
    if data.cat:
        exprs.append(ops.filter(lambda t: any([st.cat_of(data.cat) for st in t.sense])))
    return rx.pipe(*exprs)

sense_sig = signal('sense')
@sense_sig.connect
def sense_proc(sender, **kwargs):
    results=[]
    source = rx.of(*kwargs['rs'])
    cond:sense_cond=kwargs['data']

    source.pipe(
        filter_path(cond.part),
        ops.map(lambda t: to_obj({'sense': get_trees(t.lemma), **t})),
        filter_sense(cond),
        ops.map(lambda t: {'path': t.path,
                           'word': t.lemma,
                           'cat': cond.cat,
                           'value': cond.cat,
                           'roles': cond.roles,
                           'pos': t.upos.lower()}),
    ).subscribe(
        on_next=lambda value: results.append(value),
        on_error=lambda e: logger.error(e),
        on_completed=lambda: logger.debug("done."),
    )
    return results

