from typing import Text, Dict, Any

from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_sl(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_sl(Slovene, 斯洛文尼亚语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ ssl 'On se pelje s kolesom.'
            pat(5, name='behave_drive').verb(
                extract_for('word', 'nsubj'),
                behaveof('drive', 'v'), nsubj=agency,
                obl=kindof('vehicle', 'n')),
        ])
    

