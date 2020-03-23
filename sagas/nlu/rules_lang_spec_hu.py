from typing import Text, Dict, Any

from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_hu(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_hu(Hungarian, 匈牙利语) prepare phrase')

    def subject_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ shu 'A magas tanár nem angol, hanem magyar.'
            pat(-5, name='desc_person_lang').cop(
                pipes(interr=pred_cond('/conj/cc', 'but')),
                pipes(pos=pred_cond('/conj', ['adj'])),
                pipes(cat=pred_cond('/conj', 'person')),
            ),
        ])
    

