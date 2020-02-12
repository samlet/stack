from typing import Text, Dict, Any

from sagas.nlu.rules_header import *

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_it(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_it prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ se 'I want to watch a movie'
            pat(5, name='behave_willing_ev').verb(behaveof('want', 'v'),
                                                  pred_any_path('xcomp/obj', 'social_event', 'n')),
        ])
    

    def aux_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            pat(-5, name='desc_professional').cop(behaveof('professional', 'n'),
                                                   nsubj=agency, cop='c_aux'),
        ])
