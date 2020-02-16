from typing import Text, Dict, Any

from sagas.nlu.rules_header import *

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_fa(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_fa prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ sfa '‫من دوست دارم خیار بخورم.‬'  (I like to eat cucumber.)
            # $ sfa '‫من دوست دارم گوجه فرنگی بخورم.‬'  (I like to eat tomatoes.)
            pat(-5, name='desc_fav').verb(interr('have', is_part=False),
                                          pred_any_path('ccomp/obj', 'food', 'n'),
                                          nsubj=agency,),
            # $ sfa '‫عدس دوست دارید؟‬'
            pat(-5, name='ask_fav').verb(extract_for('plain+translit', 'nsubj'),
                                         interr('have', is_part=False),
                                         compound_lvc=interr('fav'),)

        ])
    

