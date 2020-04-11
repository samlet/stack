from typing import Text, Dict, Any

from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_ur(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_ur(Urdu, 乌尔都语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ sur '‫میں ایتھنز کی فلائٹ بک کرنا چاہتا ہوں‬'
            pat(5, name='behave_perform').verb(extract_for('word', 'nsubj'),
                                               behaveof('perform', 'v'),
                                               obj=specs_trans('v', 'travel'),
                                               aux=specs_trans('v', 'want'),
                                               nsubj=agency),
        ])
    

