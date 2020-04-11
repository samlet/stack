from typing import Text, Dict, Any

from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_fi(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_fi(Finnish, 芬兰语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ sfi 'Voiko täältä lainata aurinkovarjoa?'  (Can one rent a sun umbrella / parasol here?)
            pat(5, name='behave_excerpt').verb(extract_for('plain', 'advmod'),
                                               extract_for('plain', 'obj'),
                                               behaveof('borrow', 'v'),
                                               obj=kindof('artifact', 'n')),
            # infers ------
            # $ sfi 'Haluaisin appelsiinimehun.'
            pat(5, name='behave_desire').verb(behaveof('desire', 'v'), nmod=kindof('orange_juice', 'n')),

        ])
    

