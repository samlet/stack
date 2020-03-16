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
            # $ str 'Bir bira isterim.'  (I’d like a beer.)
            pat(-5, name='behave_i_want').verb(specs_trans('v', 'request'),
                                              obj=kindof('food', 'n')),
        ])
    

    def aux_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ str 'Sigaranız var mı?'  (Do you have cigarettes?)
            pat(5, name='desc_exist').cop(extract_for('word', 'nsubj'),
                                          behaveof('exist', '*'), nsubj='c_noun'),
        ])