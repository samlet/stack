from typing import Text, Dict, Any

from sagas.nlu.inferencer import extensions, InferPart
from sagas.nlu.inferencer_common import predict_pos
from sagas.nlu.rules_header import *

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)

def induce_dim(c:InferPart, t:Text, dim:Text):
    pat=c.domain.pattern(t)
    r = pat(**{c.name:dateins(dim)})
    logger.debug(f"t:{t}, dim:{dim}, result:{r[1]}, {r[0]}")
    if r[1]:
        return 2, f"{c.name}=dateins('{dim}')"

extensions.register_parts('pt',{
    # $ spt 'Eu preciso disso até amanhã.'
    'advmod': lambda c,t: induce_dim(c, t, 'time'),
    # $ spt 'Ele está entre meu irmão e minha irmã.'
    'case': lambda c,t: predict_pos(c, t, 'c_adp'),
})

class Rules_pt(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_pt(Portuguese, 葡萄牙语) prepare phrase')

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

            # $ spt 'Ela negou ser minha mãe.'  (She denied being my mother)
            pat(5, name='behave_deny').verb(extract_for('plain', 'nsubj'),
                                            behaveof('deny', 'v'),
                                            clauses(all, cla_expr('verb:obl', cop={'be'})),
                                            nsubj=agency,
                                            obl=kindof('relative', 'n')),
            # $ spt 'Desde quando você gosta de abacaxi?'
            pat(5, name='behave_like').verb(extract_for('plain', 'advmod'),
                                            extract_for('plain', 'nsubj'),
                                            behaveof('like', 'v'),
                                            nsubj=agency,
                                            advmod=cust(check_interr, lambda w: w == 'since_when'),
                                            obl=kindof('matter', 'n')),
            # infers
            # $ spt 'Eu preciso disso até amanhã.'
            pat(5, name='behave_want').verb(extract_for('plain', 'nsubj'),
                                            behaveof('want', 'v'), nsubj=agency,
                                            advmod=dateins('time')),
            # $ spt 'Nós falamos durante o jantar.'
            pat(5, name='behave_talk').verb(extract_for('plain', 'nsubj'),
                                            behaveof('talk', 'v'), nsubj=agency,
                                            obl=kindof('dine', '*')),

            # $ spt 'A cobra fala com o menino.' -> below 2 pats
            pat(5, name='behave_talk').verb(extract_for('plain', 'nsubj'),
                                            behaveof('talk', 'v'), nsubj=agency,
                                            obl=kindof('living_thing', 'n')),
            pat(5, name='living_thing_talk').verb(behaveof('talk', 'v'),
                                            nsubj=kindof('living_thing'),
                                            obl=kindof('living_thing', 'n')),
            # $ spt 'A folha tem vinte centímetros.'
            pat(5, name='behave_measure').verb(behaveof('have', 'v'),
                                                  extract_for('plain+number', 'obj'),
                                                  nsubj=kindof('matter', 'n'),
                                                  obj=kindof('unit_of_measurement', '*')),
            # $ spt 'O café abre em fevereiro.'
            pat(5, name='behave_open').verb(behaveof('open', 'v'),
                                            nsubj=kindof('restaurant'),
                                            obl=kindof('time_period', 'n')),

        ])

    def aux_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ spt 'Com licença, onde é o banheiro?'
            pat(5, name='desc_where').cop(interr_root('where'),
                                          extract_for('plain', 'nsubj'),
                                          cop='c_aux',
                                          nsubj=agency),

        ])
    

