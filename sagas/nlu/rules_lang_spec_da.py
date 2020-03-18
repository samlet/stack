from typing import Text, Dict, Any

from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_da(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_da(Danish, 丹麦语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ sda 'De spiser uden mig.'
            pat(5, name='behave_eat').verb(extract_for('word', 'nsubj'),
                                           extract_for('chunk', 'verb:obl'),
                                           behaveof('eat', 'v'), nsubj=agency),
            # $ sda 'Han skriver til kvinden.'
            pat(5, name='behave_write').verb(extract_for('word', 'nsubj'),
                                             behaveof('write', 'v'),
                                             nsubj=agency,
                                             obl=kindof('person', 'n')),

        ])
    
    def aux_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ sda 'Det er en bog om heste.'
            pat(5, name='desc_book').cop(extract_for('word', 'nsubj'),
                                         extract_for('plain', 'det'),
                                         extract_for('chunk', 'aux:nmod'),
                                         behaveof('book', 'n'),
                                         nsubj=agency, cop='c_aux',
                                         nmod=kindof('living_thing', 'n')),
        ])

