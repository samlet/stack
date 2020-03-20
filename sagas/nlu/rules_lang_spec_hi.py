from typing import Text, Dict, Any

from sagas.hi.iwn_helper import inherit_axis
from sagas.nlu.inspector_common import Context
from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)

def fn_inherit(key:Text, ctx:Context, *args, **kwargs):
    lemma=ctx.lemmas[key]
    pos=ctx.get_feat_pos(key)
    logger.debug(f"predicate {lemma}, {pos} : {args[0]}")
    succ= inherit_axis(lemma, pos, args[0])
    if succ:
        ctx.add_result('axis', fn_inherit.__name__, key,
                       val={'lemma':lemma, 'pos':pos, 'axis':args[0]})
    return succ

class AxisInspector(GeneralInspector):
    """
    >>> axis=AxisInspector
    >>> ins=axis('obj').inherit('khadya phala|edible fruits')
    """
    @property
    def fn_map(self):
        return {'inherit': fn_inherit,}

axis=AxisInspector

class Rules_hi(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_hi(Hindi, 印地语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ shi 'मैं सेब खाता हूं'
            pat(-5, name='behave_fruits').verb(
                tags('watch'),
                axis('obj').inherit('khadya phala|edible fruits'),
                extract_for('word', 'nsubj'),
                nsubj=agency,
            ),
        ])
    

