from typing import Text, Dict, Any

from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_ca(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_ca(Catalan, 加泰罗尼亚语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ sca "Els nens no senten l'ànec."
            pat(-5, name='behave_feel').verb(extract_for('word', 'advmod'),
                                            behaveof('feel', 'v'),
                                            nsubj=kindof('person', 'n'),
                                            obj=kindof('living_thing', 'n')),
        ])
    

