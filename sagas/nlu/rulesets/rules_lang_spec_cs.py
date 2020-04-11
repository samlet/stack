from typing import Text, Dict, Any

from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)

class Rules_cs(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_cs(Czech, 捷克语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ scs 'Nečeká na poslední den.'
            pat(5, name='behave_wait').verb(behaveof('wait', 'v'),
                                            obl=kindof('day', 'n')),
            # $ scs 'František se stará o koně.'
            pat(5, name='behave_care').verb(extract_for('plain', 'nsubj'),
                                            behaveof('care', 'v'), nsubj=agency,
                                            obl_arg=kindof('animal', 'n')),
            # $ scs 'Zajímám se o tu ženu.'
            pat(5, name='behave_matter_to').verb(behaveof('matter_to', 'v'),
                                                 obl_arg=kindof('person', 'n')),
            # $ scs 'Staráme se o Žofii.'
            pat(5, name='behave_care').verb(extract_for('plain', 'obl:arg'),
                                            behaveof('care', 'v'),
                                            obl_arg='c_propn'),

        ])
    

