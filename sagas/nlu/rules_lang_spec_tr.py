from typing import Text, Dict, Any

from sagas.nlu.patterns import DefaultArgs
from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
import logging

from sagas.nlu.tool_base import LangToolBase

logger = logging.getLogger(__name__)


class Rules_tr(LangToolBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_tr(Turkish, 土耳其语) prepare phrase')

    def opts(self) -> Dict[Text, Any]:
        return {'verb': DefaultArgs.create(extract_for('feats', 'verb:_')),
                }

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ str 'Bir bira isterim.'  (I’d like a beer.)
            pat(-5, name='behave_food').verb(
                specs_trans('v', 'request'),
                obj=kindof('food', 'n')),
            # $ str 'Rezervasyonumu onaylamak istiyorum.'  (I would like to confirm my reservation.)
            pat(5, name='behave {verb.obj:cat} for {verb.obj.obj:cat}, '
                        'modal {verb._:cat}, personal {verb._:personal}').verb(
                specs_trans('v', 'request'),
                ins().cat('/obj/obj') == 'reservation',
                obj=kindof('approve', '*')),
            # $ str 'Köyden geliyorum.'
            # $ str 'Hangi köylerden geliyorsun?'  ("您来自哪个村庄？")
            pat(5, name='come from {verb.obl:cat}, '
                        'personal {verb._:personal}').verb(
                # extract_for('feats', 'verb:_'),
                specs_trans('v', 'come'),
                obl=kindof('social_group', 'n')),
            # $ str 'Ofiste yumurta yiyorlar.'
            pat(5, name='behave {verb._:cat} with {verb.obj:cat}, '
                        'loc {verb.nsubj:cat}, '
                        'personal {verb._:personal}').verb(
                # extract_for('feats', 'verb:_'),
                specs_trans('v', 'eat', 'feed', 'consume'),
                nsubj=kindof('place_of_business', 'n'),
                obj=kindof('food', 'n')),

            # $ str 'Ağustosta güzel elbiseler giyeriz.'
            pat(5, name='behave_we_wear').verb(
                specs_trans('v', 'wear'),
                obl=kindof('time_period', 'n'),
                obj=kindof('dress', 'n')),
        ])
    

    def aux_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ str 'Sigaranız var mı?'  (Do you have cigarettes?)
            pat(5, name='desc_exist').cop(extract_for('word', 'nsubj'),
                                          behaveof('exist', '*'),
                                          nsubj='c_noun'),
        ])
