from typing import Text, Dict, Any

from sagas.nlu.inferencer import InferPart, extensions
from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)

pron=['c_pron', 'c_det']
def induce_pron(c:InferPart, t:Text):
    if c.lemma=='-PRON-':
        return [(4, f"extract_for('plain', '{c.name}')"),
                (2, f"{c.name}=pron")]


extensions.register_parts('lt',{
    'nsubj': lambda c,t: induce_pron(c,t),
    'nmod': lambda c,t: induce_pron(c,t),
})

class Rules_lt(LangSpecBase):
    # def opts(self):
    #     return {'engine':'spacy'}

    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_lt(Lithuanian, 立陶宛语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ slt 'Kada nusileisime?'  (When do we land?)
            pat(-5, name='behave_descend').verb(extract_for('word', 'advmod'),
                                               specs_trans('v', 'travel'),
                                               advmod=interr('when')
                                               ),
        ])
    
    def subject_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ slt 'Ar tai jūsų lagaminas?'
            pat(-5, name='desc_suitcase').cop(extract_for('plain', 'nsubj'),
                                              extract_for('plain', 'nmod'),
                                              specs_trans('n', 'instrumentality'),
                                              nsubj=pron,
                                              nmod=pron),
        ])
