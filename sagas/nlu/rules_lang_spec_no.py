from typing import Text, Dict, Any

from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_no(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_no(Norwegian Bokmål, 挪威语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ sno 'Når lander vi?'
            pat(5, name='behave_land').verb(extract_for('word', 'advmod'),
                                            extract_for('word', 'nsubj'),
                                            behaveof('land', 'v'),
                                            advmod=interr('when'),
                                            nsubj=agency),

        ])
    

    def aux_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ sno 'Er dette kofferten din?'
            pat(5, name='ask_bag').cop(extract_for('word', 'nsubj'),
                                        behaveof('artifact', 'n'),
                                        cop=kindof('be', 'v'),
                                        nsubj=agency),
        ])