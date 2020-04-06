from typing import Text, Dict, Any

from sagas.nlu.rules_header import *

import sagas.tracker_fn as tc
import logging

from sagas.nlu.tool_base import LangToolBase

logger = logging.getLogger(__name__)


class Rules_es(LangToolBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_es(Spanish) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ ses '¿Qué hace Marta?'
            pat(5, name='behave_make?').verb(
                behaveof('make', 'v'), nsubj=agency,
                obj=interr('what'), ),
            # $ ses 'Ella trabaja en una oficina.'
            pat(5, name='behave_work').verb(
                behaveof('work', 'v'),
                nsubj=agency,
                obl=kindof('place_of_business', 'n')),

            ## infers
            pat(5, name='behave_read').verb(
                extract_for('plain', 'advmod'),
                behaveof('read', 'v'), nsubj=agency,
                obl=kindof('school', '*'), obj=kindof('book', '*'))

        ])
    

