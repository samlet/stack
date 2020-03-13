from typing import Text, Dict, Any

from sagas.nlu.inferencer import extensions, InferPart
from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)

def head_interr(c:InferPart, part:Text):
    from sagas.nlu.inspectors_dataset import get_interrogative
    rep=get_interrogative(c.lemma, 'ru')
    if rep:
        return 2, f"{part}=interr('{rep}')"
    else:
        return 4, f"extract_for('plain', '{part}')"

extensions.register_parts('ru',{
    'nsubj': lambda c,t: [(4, "extract_for('plain', 'nsubj')"),
                          (2, "nsubj=agency")],
    'head_csubj': lambda c,t: head_interr(c, 'head_csubj'),
})
class Rules_ru(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_ru(Russian, 俄语) prepare phrase')

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
            # $ sru 'Можно прикурить?'
            pat(5, name='behave_light').verb(behaveof('light', 'v'),
                                             head_csubj=interr('can')),
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
    

