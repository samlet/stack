from typing import Text, Dict, Any

from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_sv(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_sv(Swedish, 瑞典语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ ssv 'En ren äter ett äpple.'
            pat(-5, name='behave_eat').verb(extract_for('word', 'nsubj'),
                                           behaveof('eat', 'v'),
                                           obj=kindof('food', 'n')),
        ])
    

