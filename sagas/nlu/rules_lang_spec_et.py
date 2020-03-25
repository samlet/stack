from typing import Text, Dict, Any

from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_et(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_et(Estonian, 爱沙尼亚语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ set 'Millal me maandume?'
            pat(5, name='behave_landing').verb(extract_for('word', 'nsubj'),
                                               specs_trans('v', 'land'),
                                               mark=interr('when'),
                                               nsubj=agency),
        ])
    

    def aux_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ set 'Kas see on teie kohver?'
            pat(5, name='desc_suitcase').cop(extract_for('word', 'advmod'),
                                             specs_trans('n', 'instrumentality'),
                                             nmod=agency,
                                             cop='c_aux'),
        ])