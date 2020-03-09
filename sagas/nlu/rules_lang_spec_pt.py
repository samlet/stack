from typing import Text, Dict, Any

from sagas.nlu.inspector_common import Context
from sagas.nlu.inspectors_dataset import get_interrogative
from sagas.nlu.rules_header import *

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)

def check_interr(key:Text, ctx:Context, check_fn) -> bool:
    for stem in ctx.stem_pieces(key):
        interr=get_interrogative(stem, 'pt')
        if interr and check_fn(interr):
            return True
    return False

class Rules_pt(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_pt prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ se 'I want to watch a movie'
            pat(5, name='behave_willing_ev').verb(behaveof('want', 'v'),
                                                  pred_any_path('xcomp/obj', 'social_event', 'n')),
            # $ spt 'Ele trabalha na padaria.'
            pat(5, name='behave_work').verb(behaveof('work', 'v'), obl=kindof('workplace', 'n')),
            # $ spt 'Nós comemos massa no restaurante.'
            pat(5, name='behave_eat').verb(behaveof('eat', 'v'),
                                           obl=kindof('building', 'n'),
                                           obj=kindof('food', 'n')),
            # $ spt 'Ela pensa nas meninas.'
            pat(5, name='behave_think_of').verb(behaveof('think', 'v'),
                                                obl=kindof('person', 'n'),),
            # $ spt 'Ele não toca na sopa.'
            pat(5, name='behave_touch_not').verb(behaveof('touch', 'v'),
                                                 advmod=negative(),
                                                 obl=kindof('matter', 'n')),
            # $ spt 'A casa tem dezenove quartos.'  ("The house has nineteen rooms.")
            pat(3, name='obj_num').verb(checker(has_num='verb:obj'), ),
            # $ spt 'Nós vamos entender o que ela disse.'
            pat(5, name='behave_understand').verb(extract_for('plain', 'nsubj'),
                                                  behaveof('understand', 'v'),
                                                  nsubj=agency, ccomp=kindof('say', '*')),
            # $ spt 'Por que você não perguntou?'  (Why have you not asked?)
            pat(5, name='behave_ask').verb(tags('inform'),
                                           extract_for('plain', 'nsubj'),
                                           behaveof('ask', 'v'),
                                           advmod=negative(),
                                           obl=cust(check_interr, lambda w: w=='why'),
                                           nsubj=agency),
            # $ spt 'Ele pediu uma cerveja.'  (He has asked for a beer.)
            pat(5, name='behave_request').verb(extract_for('plain', 'nsubj'),
                                               behaveof('request', 'v'),
                                               nsubj=agency,
                                               obj=specsof('n', 'beverage', 'food')),

        ])

    def aux_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ spt 'Com licença, onde é o banheiro?'
            pat(5, name='desc_where').cop(interr_root('where'), extract_for('plain', 'nsubj'), cop='c_aux',
                                          nsubj=agency),

        ])
    

