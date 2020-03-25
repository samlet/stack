from typing import Text, Dict, Any

from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_uk(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_uk(Ukrainian, 乌克兰语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ suk 'Коли ми приземляємося?'
            pat(5, name='behave_landing').verb(extract_for('word', 'advmod'),
                                               extract_for('word', 'nsubj'),
                                               specs_trans('v', 'land'),
                                               nsubj=agency),
        ])

    def subject_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ suk 'Це Ваша валіза?'
            pat(5, name='desc_suitcase').cop(extract_for('word', 'nsubj'),
                                             extract_for('plain', 'det'),
                                             specs_trans('n', 'instrumentality'),
                                             nsubj=agency),

        ])

