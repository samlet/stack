from typing import Text, Dict, Any

from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)


class Rules_sr(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_sr(Serbian latin; Srpska Latinica, 塞尔维亚语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ ssr 'On se vozi biciklom.'
            pat(5, name='behave_drive').verb(
                extract_for('word', 'nsubj'),
                specs_trans('v', 'drive'),
                obl=specs_trans('n', 'vehicle'),
                nsubj=agency),
        ])
    

    def aux_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ ssr 'Да ли је то Ваша ташна?'
            pat(-5, name='desc_belong').cop(extract_for('word', 'nsubj'),
                                          extract_for('plain', 'det'),
                                          specs_trans('n', 'artifact'),
                                          cop='c_aux',
                                          nsubj=agency),
        ])

