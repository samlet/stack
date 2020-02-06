from typing import Text, Dict, Any

from sagas.nlu.rules_header import *

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_pt(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_pt prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ se 'I want to watch a movie'
            pat(5, name='behave_willing_ev').verb(behaveof('want', 'v'),
                                                  pred_any_path('xcomp/obj', 'social_event', 'n')),
            # $ spt 'Ele trabalha na padaria.'
            pat(5, name='behave_work').verb(behaveof('work', 'v'), obl=kindof('workplace', 'n')),
            # $ spt 'Nós comemos massa no restaurante.'
            pat(5, name='behave_eat').verb(behaveof('eat', 'v'),
                                           obl=kindof('building', 'n'),
                                           obj=kindof('food', 'n')),
            # $ spt 'Ela pensa nas meninas.'
            pat(5, name='behave_think_of').verb(behaveof('think', 'v'),
                                                obl=kindof('person', 'n'),),
            # $ spt 'Ele não toca na sopa.'
            pat(5, name='behave_touch_not').verb(behaveof('touch', 'v'),
                                                 advmod=negative(),
                                                 obl=kindof('matter', 'n')),

        ])
    

