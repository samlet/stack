from typing import Text, Dict, Any

from sagas.nlu.inferencer import extensions
from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)

extensions.register_parts('ru',{
    'nsubj': lambda c,t: [(4, "extract_for('plain', 'nsubj')"),
                          (2, "nsubj=agency")],
})
class Rules_ru(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_ru prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ sru 'У Вас есть сигареты?'
            # $ sru 'У Вас есть пепельница?'
            pat(5, name='behave_exist').verb(extract_for('plain', 'nsubj'),
                                           behaveof('exist', 'v'), nsubj=agency),
            # $ sru 'У меня нет ложки.'
            pat(5, name='behave_not').verb(behaveof('negative', '*'),
                                           extract_for('plain', 'nsubj'),
                                           nsubj=agency, obl=kindof('ego', '*')),
            # $ sru 'Я хотел бы кофе.'
            pat(5, name='behave_desire').verb(extract_for('plain', 'nsubj'),
                                              behaveof('desire', 'v'),
                                              nsubj=agency,
                                              obj=kindof('food', 'n')),
        ])

    def subject_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ sru 'Этот столик свободен?'
            pat(5, name='desc_free').cop(
                behaveof('free', '*'),
                extract_for('plain', 'nsubj'),
                nsubj=agency),
        ])
    

