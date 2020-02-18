from typing import Text, Dict, Any

from sagas.nlu.rules_header import *

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_hr(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_hr prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ shr 'On pije kavu.'
            pat(-5, name='behave_drink').verb(behaveof('drink', 'v'),
                                             nsubj=agency,
                                             obj=kindof('beverage', 'n')),
            # $ shr 'Imate li cvjetače?'  (Do you have cauliflower?)
            # ... 'value': {'category': 'plant',
            #             'pos': 'n',
            #             'subs': 'cauliflower',
            #             'word': 'cvjetače/cvjetač'}}]
            # $ shr 'Imate li graha?'
            pat(-5, name='desc_have').verb(behaveof('have', 'v'),
                                           obj=kindof('plant', 'n')),
        ])
    

