from typing import Text, Dict, Any

from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_pl(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_pl(Polish, 波兰语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ spl 'Poproszę kartę dań.'
            pat(5, name='behave_ask').verb(behaveof('ask', 'v'),
                                           obj=kindof('menu', 'n')),
            # $ spl 'Poproszę piwo.'
            # $ spl 'Poproszę kawę.'
            pat(5, name='behave_food').verb(behaveof('ask', 'v'),
                                            obj=kindof('food', 'n')),
        ])
    

