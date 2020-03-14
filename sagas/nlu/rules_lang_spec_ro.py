from typing import Text, Dict, Any

from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_ro(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_ro(Romanian, 罗马尼亚语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # infers ...
            # $ sro 'Eu citesc o scrisoare.'
            # $ sro 'Eu citesc ziarul.'  (I read the newspaper.)
            pat(5, name='behave_read_comm').verb(extract_for('plain', 'nsubj'),
                                            behaveof('read', 'v'), nsubj=agency,
                                            obj=kindof('written_communication', 'n')),

            # $ sro 'Tu scrii și eu citesc.'
            pat(5, name='behave_write').verb(extract_for('plain', 'nsubj'), behaveof('write', 'v'), nsubj=agency),
            pat(5, name='behave_read').verb(extract_for('plain', 'nsubj'), behaveof('read', 'v'), nsubj=agency),
        ])
    

