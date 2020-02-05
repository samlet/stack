from typing import Text, Dict, Any

from sagas.nlu.rules_header import *

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)

class Rules_en(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_en prepare phrase')

    def verb_rules(self):
        pat, actions_obj=(self.pat, self.actions_obj)

        self.collect(pats=[
            # $ se 'I want to play music.'
            pat(5, name='behave_media').verb(pred_any_path('xcomp/obj','sound/perception', 'n')),
            # $ se 'I want to watch a movie'
            pat(5, name='behave_willing_ev').verb(behaveof('want', 'v'), pred_any_path('xcomp/obj','social_event', 'n')),
            # $ se 'you took fifty damage'
            pat(5, name='avatar_injured').verb(behaveof('take', 'v'), pred_any_path('obj', 'damage', 'n'),
                                               obj=dateins('number')),
            ])

    def aux_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ se 'what will be the weather in three days?'
            pat(5, name='query_weather').root(predict_aux(
                ud.__text('will') >> [ud.nsubj('what'), ud.dc_cat('weather')])),
            # $ se 'you are dead'
            pat(5, name='avatar_dead').cop(behaveof('dead', 'a'), nsubj=agency, cop='c_aux'),
        ])

    def root_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)
        self.collect(pats=[
            # Recognizes dates and times described in many ways:
            #   today at 5pm
            #   2014-10-01
            #   the last Tuesday of October 2012
            #   twenty five minutes ago
            #   the day before labor day 2020
            #   June 10-11 (interval)
            #   third monday after christmas 1980
            #
            # $ se 'the last Tuesday of October 2012'
            pat(2, name='datetime').entire(dateins('time', entire=True))
        ])

    def execute(self):
        if len(self.matched)>0:
            matched_info={k:len(v.results) for k,v in self.matched.items()}
            tc.emp('green', f"♯ matched id rules: {matched_info}")

