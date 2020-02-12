from typing import Text, Dict, Any

from sagas.nlu.rules_header import *

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_it(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_it prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ se 'I want to watch a movie'
            pat(5, name='behave_willing_ev').verb(behaveof('want', 'v'),
                                                  pred_any_path('xcomp/obj', 'social_event', 'n')),
            # $ sit 'I postini lavorano di mattina.'
            pat(5, name='desc_work_time').verb(behaveof('work', 'v'),
                                               nsubj=agency,
                                               obl=extract_dt()
                                               ),
        ])
    

    def aux_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ sit 'I miei genitori sono degli avvocati.'
            pat(-5, name='desc_professional_1').cop(behaveof('professional', 'n'),
                                                   nsubj=agency, cop='c_aux'),
            # $ sit 'I miei cugini sono idraulici.'  (配管工)
            pat(-5, name='desc_professional_2').cop(behaveof('craftsman/skilled_worker', 'n'),
                                                  nsubj=agency, cop='c_aux'),
            # $ sit 'Dove sono i meccanici?'
            pat(5, name='ask_loc').cop(extract_c('nsubj'), extract_c('advmod'),
                                       nsubj=agency,
                                       advmod=interr('where')),
        ])
