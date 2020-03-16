from typing import Text, Dict, Any

from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_tr(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_tr(Turkish, 土耳其语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ str 'Bir bira isterim.'
            pat(-5, name='behave_i_want').verb(specs_trans('v', 'request'),
                                              obj=kindof('food', 'n')),
        ])
    

