from typing import Text, Dict, Any

from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_he(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_he(Hebrew, 希伯来语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ she '‫אני מבקש משהו בלי בשר.‬'
            pat(5, name='behave_ask').verb(extract_for('word', 'nsubj'),
                                           extract_for('word', 'obj'),
                                           behaveof('request', 'v'),
                                           nsubj=agency),
        ])
    

