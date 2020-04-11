from typing import Text, Dict, Any

from sagas.nlu.rules_header import *

import sagas.tracker_fn as tc
import logging

from sagas.nlu.tool_base import LangToolBase

logger = logging.getLogger(__name__)

class Rules_en(LangToolBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_en(English) prepare phrase')

    def verb_rules(self):
        pat, actions_obj=(self.pat, self.actions_obj)

        self.collect(pats=[
            # $ se 'I want to play music.'
            pat(5, name='behave_media').verb(pred_any_path('xcomp/obj','sound/perception', 'n')),
            # $ se 'I want to watch a movie'
            pat(5, name='behave_willing_ev').verb(behaveof('want', 'v'),
                                                  pred_any_path('xcomp/obj','social_event', 'n')),
            # $ se 'I like to eat cucumber.'
            #                  ┌−−−−−−−−┐
            #                  ╎   I    ╎
            #                  └−−−−−−−−┘
            #                    ▲
            #                    │ nsubj
            #                    │
            # ┌−−−−−−┐  root   ┌−−−−−−−−┐  xcomp   ┌−−−−−−−┐  obj   ┌−−−−−−−−−−┐
            # ╎ ROOT ╎ ──────▶ ╎  like  ╎ ╴╴╴╴╴╴╴▶ ╎  eat  ╎ ─────▶ ╎ cucumber ╎
            # └−−−−−−┘         └−−−−−−−−┘          └−−−−−−−┘        └−−−−−−−−−−┘
            #                    │                   │
            #                    │ punct             │ mark
            #                    ▼                   ▼
            #                  ┌−−−−−−−−┐          ┌−−−−−−−┐
            #                  ╎   .    ╎          ╎  to   ╎
            #                  └−−−−−−−−┘          └−−−−−−−┘
            # I like to eat tomatoes.
            # $ se 'I like to eat sweet corn.'
            #                  ┌−−−−−−−−┐
            #                  ╎   I    ╎
            #                  └−−−−−−−−┘
            #                    ▲
            #                    │ nsubj
            #                    │
            # ┌−−−−−−┐  root   ┌−−−−−−−−┐  xcomp   ┌−−−−−−−┐  obj   ┌−−−−−−┐  amod   ┌−−−−−−−┐
            # ╎ ROOT ╎ ──────▶ ╎  like  ╎ ╴╴╴╴╴╴╴▶ ╎  eat  ╎ ─────▶ ╎ corn ╎ ──────▶ ╎ sweet ╎
            # └−−−−−−┘         └−−−−−−−−┘          └−−−−−−−┘        └−−−−−−┘         └−−−−−−−┘
            #                    │                   │
            #                    │ punct             │ mark
            #                    ▼                   ▼
            #                  ┌−−−−−−−−┐          ┌−−−−−−−┐
            #                  ╎   .    ╎          ╎  to   ╎
            #                  └−−−−−−−−┘          └−−−−−−−┘
            pat(5, name='desc_eat').verb(extract_for('chunk+chunk_text', 'verb:xcomp/obj'),
                                         behaveof('like', 'v'),
                                         pred_any_path('xcomp/obj', 'food', 'n'),
                                         xcomp=kindof('eat', 'v'),),
            # $ se 'you took fifty damage'
            pat(5, name='avatar_injured').verb(behaveof('take', 'v'),
                                               pred_any_path('obj', 'damage', 'n'),
                                               obj=dateins('number')),

            # $ se 'Giving alms is a good deed.'
            #                  ┌−−−−−−┐
            #                  ╎  is  ╎
            #                  └−−−−−−┘
            #                    ▲
            #                    │ cop
            #                    │
            # ┌−−−−−−┐  root   ┌−−−−−−┐  csubj   ┌────────┐  obj   ┌──────┐
            # ╎ ROOT ╎ ──────▶ ╎      ╎ ───────▶ │ Giving │ ─────▶ │ alms │
            # └−−−−−−┘         ╎ deed ╎          └────────┘        └──────┘
            # ┌−−−−−−┐  amod   ╎      ╎  punct   ┌−−−−−−−−┐
            # ╎ good ╎ ◀────── ╎      ╎ ───────▶ ╎   .    ╎
            # └−−−−−−┘         └−−−−−−┘          └−−−−−−−−┘
            #                    │
            #                    │ det
            #                    ▼
            #                  ┌−−−−−−┐
            #                  ╎  a   ╎
            #                  └−−−−−−┘
            pat(5, name='desc_subj').verb(behaveof('give', 'v'), obj=agency,
                                          head_csubj='c_noun'),
            # 先用指定的方式解析成分, 根据解析的数据来编写predicts
            # $ nluc en 'Giving alms is a good deed.' aux
            # $ se 'Giving alms is a good deed.'
            pat(5, name='desc_subj_good').verb(predict_aux(
                ud.__cat('be') >> [ud.csubj('give'), ud.amod_cat('good')])),
            # $ se 'My grandfather died five years ago at the age of ninety.'
            pat(5, name='desc_died').verb(extract_for('time', 'advmod'),
                                          extract_for('number', 'obl'),
                                          extract_for('plain', 'nsubj'),
                                          behaveof('die', 'v'), nsubj=agency),
            # $ print_detail=on se 'what restaurants can you recommend?'
            # $ se 'what restaurants can you recommend?'
            pat(5, name='ask_recommend').verb(extract_for('rasa', '_'),
                                              behaveof('recommend', 'v'),
                                              obj='c_noun',
                                              aux='c_aux',
                                              nsubj=agency),
            # $ se 'It totally concerns you.'
            pat(5, name='desc_refer').verb(extract_for('plain', 'nsubj'),
                                           extract_for('plain', 'obj'),
                                           behaveof('refer', 'v'),
                                           nsubj=agency, obj=agency),
            # $ sen 'I baked it in the oven at 180 degrees for an hour.'
            pat(2, name='behave_cook').verb(behaveof('cook', 'v'),
                                            extract_for('plain', 'obj'),
                                            nsubj=agency,
                                            obl=extract('plain+number+time+temperature'),
                                            obj=agency),
            # $ se 'What do you think about the war?'
            pat(5, name='military_fact').verb(
                pipes(collect=['verb', 'noun']),
                pipes(sense=sense_cond.is_cat('/obl', 'fact|事情')
                      .with_roles(domain='military|军')),),
            # pat(1, name='collect_v_n').verb(pipes(collect=['verb', 'noun'])),

            # $ se 'i play football'
            pat(5, name='sports').verb(
                inform('track'),
                sense('obj').cat_of(obj='SportTool|运动器材')
                    .has_role(domain='football|足球')
                    .has_role(domain='sport|体育')
                    .has_role(CoEvent='exercise|锻炼'),
                obj=kindof('football', 'n')
            ),
        ])

    def aux_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ se 'what will be the weather in three days?'
            pat(5, name='query_weather').root(predict_aux(
                ud.__text('will') >> [ud.nsubj('what'), ud.dc_cat('weather')])),
            # $ se 'you are dead'
            pat(5, name='avatar_dead').cop(behaveof('dead', 'a'), nsubj=agency, cop='c_aux'),
            # the following is wrong pattern
            # pat(-5, name='desc_dead').cop(behaveof('be', '*'), nsubj=agency, head=kindof('dead', '*')),

            # se 'my email is samlet@ymail.com'
            pat(5, name='desc_email').cop(extract_for('email', '_'),
                                       nsubj=kindof('electronic_mail', 'n'),
                                       cop='c_aux'),
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
