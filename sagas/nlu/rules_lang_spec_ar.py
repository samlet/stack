from typing import Text, Dict, Any

from sagas.nlu.rules_header import *

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_ar(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_ar prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ sa '‫لا أحب البصل.‬'  (I don’t like onions.)
            # $ print_detail=true sa '‫لا أحب البصل.‬'
            pat(5, name='behave_fav').verb(extract_for('plain+translit', 'obj'),
                                           extract_for('plain+translit', 'nsubj'),
                                           behaveof('love', 'v'), obj='c_noun', nsubj=negative()),
        ])
    

