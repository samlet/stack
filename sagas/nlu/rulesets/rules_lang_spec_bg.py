from typing import Text, Dict, Any

from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_bg(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_bg(Bulgarian, 保加利亚语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ sbg 'Той пътува с мотор.'
            # $ sbg 'Той пътува с кораб.'
            # $ sbg 'Той пътува с лодка.'
            # Data source: 'En route'
            pat(5, name='behave_travel').verb(extract_for('plain', 'nsubj'),
                                              behaveof('travel', 'v'),
                                              nsubj=agency,
                                              obl=kindof('vehicle', '*')),
        ])
    

