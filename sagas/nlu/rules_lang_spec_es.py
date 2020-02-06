from typing import Text, Dict, Any

from sagas.nlu.rules_header import *

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_es(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_es prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ se 'I want to watch a movie'
            pat(5, name='behave_willing_ev').verb(behaveof('want', 'v'),
                                                  pred_any_path('xcomp/obj', 'social_event', 'n')),
            # $ ses '¿Qué hace Marta?'
            pat(5, name='behave_make?').verb(behaveof('make', 'v'), nsubj=agency,
                                             obj=interr('what'),),
            # $ ses 'Ella trabaja en una oficina.'
            pat(5, name='behave_work').verb(behaveof('work', 'v'), nsubj=agency,
                                            obl=kindof('place_of_business', 'n')),
        ])
    

