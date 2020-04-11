from typing import Text, Dict, Any

from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_af(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_af(Afrikaans, 南非荷兰语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ saf 'Ry asseblief stadiger.'
            pat(5, name='behave_ride').verb(extract_for('word', 'advmod'),
                                            behaveof('ride', 'v'),
                                            advmod=specs_trans('*', 'slow', 'fast').opt(raw_fmt=raw_fmt_pos)
                                            ),
        ])
    
    def aux_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ saf 'Ek is haastig.'
            pat(5, name='desc_hastily').cop(extract_for('word', 'nsubj'),
                                            specs_trans('*', 'hurriedly').opt(raw_fmt=raw_fmt_pos),
                                            nsubj=agency, cop='c_aux'),
        ])
