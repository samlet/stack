from typing import Text, Dict, Any

from sagas.nlu.rules_header import *

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_fr(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_fr prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ sf 'Elle a gratuitement des légumes.'  (She has some vegetables for free.)
            pat(5, name='desc_have').verb(extract_for('plain', 'obj'),
                                          extract_for('plain', 'advmod'),
                                          behaveof('have', 'v'),
                                          nsubj=agency, obj='c_noun'),
            # $ sf 'Ça te concerne totalement.'
            pat(5, name='desc_refer').verb(extract_for('plain', 'nsubj'),
                                          extract_for('plain', 'iobj'),
                                          behaveof('refer', 'v'),
                                          nsubj=agency, iobj=agency),
            # $ sf "J'aime bien votre humour."
            pat(5, name='behave_love').verb(extract_for('plain', 'nsubj'),
                                           extract_for('plain', 'obj'),
                                           behaveof('love', 'v'),
                                           nsubj=agency, obj=agency),
            # $ sf 'Elle présente tous les caractères de cette maladie.'
            pat(5, name='behave_represent').verb(extract_for('plain', 'nsubj'),
                                            extract_for('plain', 'obj'),
                                            specsof('v', 'represent', 'show'),
                                            nsubj=agency, obj=agency),
        ])
    

    def aux_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ sf 'Il est quasiment prêt.'
            pat(5, name='desc_state').cop(extract_for('plain', '_'),
                                          extract_for('plain', 'advmod'),
                                          behaveof('state/attribute', 'n'),
                                          nsubj=agency,
                                          cop='c_aux'),
        ])
