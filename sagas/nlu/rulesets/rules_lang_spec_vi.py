from typing import Text, Dict, Any

from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_vi(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_vi(Vietnamese, 越南语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ svi 'Tôi muốn đăng ký một chuyến bay sang Athen.'  (I’d like to book a flight to Athens.)
            pat(5, name='behave_wish').verb(extract_for('word', 'nsubj'),
                                            behaveof('wish', 'v'),
                                            xcomp=specs_trans('*', 'registration'),
                                            nsubj=agency),
            # $ svi 'Tôi ăn me.'
            pat(5, name='behave_eat').verb(extract_for('word', 'nsubj'),
                                           behaveof('eat', 'v'),
                                           obj=specs_trans('n', 'food'),
                                           nsubj=agency),
            # $ svi 'Đứa trẻ chia sẻ bánh mì.'  (The child shares bread.)
            pat(5, name='behave_share').verb(extract_for('word', 'nsubj'),
                                             specs_trans('v', 'share'),
                                             nsubj=agency,
                                             xcomp=kindof('bread', '*')),
        ])
    

