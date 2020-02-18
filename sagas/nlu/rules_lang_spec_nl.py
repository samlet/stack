from typing import Text, Dict, Any

from sagas.nlu.rules_header import *

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_nl(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_nl prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ snl 'Heeft u bonen?'
            pat(5, name='desc_have').verb(behaveof('have', 'v'),
                                          obj=kindof('plant', 'n'),
                                          nsubj=agency),
            # $ snl 'Ik eet graag komkommer.'
            pat(-5, name='desc_fav_eat').verb(behaveof('eat', 'v'),
                                             obj=kindof('food', 'n'),
                                             advmod=kindof('gladly', '*'),
                                             nsubj=agency),
        ])
    

