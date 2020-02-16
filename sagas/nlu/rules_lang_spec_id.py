from typing import Text, Dict, Any

from sagas.nlu.rules_header import *

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)

class Rules_id(LangSpecBase):
    def verb_rules(self):
        pat, actions_obj=(self.pat, self.actions_obj)

        self.collect(pats=[
            # $ sid 'Pekerjaan ini dimulai oleh mereka.' (This job is started by them.)
            pat(2, name='behave_di_obl').verb(nsubj_pass=agency, obl=agency),
            # $ sid 'Makanan ini disebut nasi goreng.' (en="This food is called nasi goreng.")
            pat(2, name='behave_di_obj').verb(nsubj_pass=agency, obj=agency),
            pat(2, name='food').verb(obj = kindof('food/physical_entity', 'n')),
            # $ sid 'Raja dan ratu dianggap jahat.' (en="The king and queen are considered evil.")
            pat(2, name='behave_di_amod').verb(nsubj_pass=agency, amod='c_adj'),
            # $ sid 'Surat-surat mereka dibuat di sini.'
            pat(2, name='behave_di_case').verb(nsubj_pass=agency, case=agency),
            # $ sid 'Saya diduga membantu polisi.' (I am suspected of helping the police.)
            pat(2, name='behave_di_xcomp').verb(nsubj_pass=agency, xcomp='c_verb'),
            # Kadang-kadang kami mandi di sungai. 有时我们在河里洗澡。
            pat(5, name='behave_cleanse').verb(behaveof('cleanse/better', 'v')),
            # Lemari besar itu tidak terangkat. 那个大柜子抬不动。
            pat(5, name='move_unable').verb(behaveof('move', 'v'), advmod=negative()),
            # Dia datang ke Shanghai untuk menjumpai adiknya. 他为了见弟弟来到了上海。
            pat(5, name='behave_purpose').verb(
                behaveof('arrive', 'v'), nsubj=agency, xcomp='c_verb', obl=agency, ),

            # $ sid 'Siapa yang menulis laporan ini?'
            pat(5, name='ask_event').verb(
                behaveof('write', 'v'), head_acl=matchins('siapa'), nsubj=agency, obj=agency, ),
            # $ sid 'Tujuan saya adalah mengubah kamu.' (My goal is to change you.)
            pat(5, name='behave_cleanse').verb(behaveof('change', 'v'), nsubj=kindof('motivation', 'n')),
            # $ sid 'Lakukan dengan benar.' (Do it correctly.)
            pat(5, name='command_amod').verb(behaveof('make', 'v'), amod='c_adj'),
            # $ sid 'Di mana kamu simpan makanan saya?'
            pat(5, name='keep_object_where').verb(behaveof('have', 'v'), obl=matchins(['di mana', 'dimana'], 'chunk'), obj=agency),
            # $ sid 'Aku tak bisa tidur.' (zh="我无法入睡。")
            # purpose: 测试重名的成分, 此例中的advmod
            # ┌−−−−−−┐  root     ┌−−−−−−−−−┐  punct   ┌−−−−−┐
            # ╎ ROOT ╎ ────────▶ ╎         ╎ ───────▶ ╎  .  ╎
            # └−−−−−−┘           ╎  tidur  ╎          └−−−−−┘
            # ┌−−−−−−┐  advmod   ╎         ╎  nsubj   ┌−−−−−┐
            # ╎ tak  ╎ ◀──────── ╎         ╎ ───────▶ ╎ Aku ╎
            # └−−−−−−┘           └−−−−−−−−−┘          └−−−−−┘
            #                      │
            #                      │ advmod
            #                      ▼
            #                    ┌−−−−−−−−−┐
            #                    ╎  bisa   ╎
            #                    └−−−−−−−−−┘
            pat(5, name='behave_unable').verb(behaveof('rest', 'v'), advmod=negative()),
            # $ sid 'Kami tak boleh berbicara.' (we are not allowed to speak.)
            pat(5, name='communicate_unable').verb(behaveof('communicate', 'v'), advmod=negative()),

            *actions_obj([
                # $ sid 'Saya melihat kucing terbang.'  (I see a cat flying.)
                ('perceive', 'living_thing/object'),
                ]),
            ])

    def aux_rules(self):
        pat, actions_obj=(self.pat, self.actions_obj)

        self.collect(pats=[
            # $ sid 'Sedekah adalah amal baik.'
            pat(5, name='desc_social_welfare').cop(behaveof('social_welfare', 'n'),
                                                   nsubj=agency,
                                                   amod='c_adj',
                                                   cop='c_aux'),

            # ❶ $ sid 'Minggu depan adalah hari Paskah.'  (Next week is Easter.)
            # [aux_domains](adalah) is ⊙︿⊙ day(hari)
            # 	[nsubj](Minggu depan) Next week
            # 	[cop](adalah) is
            # 	[flat](Paskah) Easter
            # +----+-------+---------+--------+---------+-----------------+------------------+
            # |    | rel   |   index | text   | lemma   | children        | features         |
            # |----+-------+---------+--------+---------+-----------------+------------------|
            # |  0 | nsubj |       1 | Minggu | minggu  | Minggu, depan.. | c_propn, x_nsd.. |
            # |  1 | cop   |       3 | adalah | adalah  | adalah..        | c_aux, x_o--..   |
            # |  2 | flat  |       5 | Paskah | paskah  | Paskah..        | c_propn, x_nsd.. |
            # |  3 | punct |       6 | .      | .       | ...             | c_punct, x_z--.. |
            # +----+-------+---------+--------+---------+-----------------+------------------+
            #
            # ❷ $ python -m sagas.nlu.extractor_cli datetime 'Minggu depan' id
            # ❸ $ def Paskah id
            pat(5, name='desc_feast_day').cop(behaveof('day', 'n'),
                                              flat=kindof('feast_day/day', 'n'),
                                              nsubj='c_propn'),
            pat(3, name='extract_day').cop(behaveof('day', 'n'),
                                              flat=kindof('feast_day/day', 'n'),
                                              nsubj=extract('plain+date_search+date_parse')),
            ])

    def subject_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)
        self.collect(pats=[
            # $ sid 'Apa yang lebih murah?'
            pat(1).subj('adj', nsubj=agency, head_amod=interr('what')),
            # $ sid 'Siapa yang di kiri Anda?' (zh="谁在你的左边？")
            pat('loc_inquiry', 5).subj('pron', 'noun', nsubj=agency, case=kindof('in', 'r'), head_nmod=matchins('siapa')),
            ])

    def root_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)
        self.collect(pats=[
            pat(1).verb(nsubj=agency, obj=agency),
            # $ sid 'Berapa umur kamu?' (en="How old are you?")
            pat(5, name='years_old').verb(behaveof('age', 'n'), amod='c_det'),
            # $ sid 'Bola putih.' (球是白的)
            # notice: 'Bola Dimas putih.'无法匹配这条规则, 因为'Bola Dimas'是flat关系,
            # 针对id中的flat关系, 需要单独处理, 将flat关系的token合并为chunk, 然后再处理这个chunk与外界之间的关系.
            pat(5).verb(behaveof('physical_entity', 'n'), amod=kindof('color', 'n')),
            # $ sid 'Jaraknya dekat.' (en="The distance is close.")
            pat(5).verb(behaveof('measure', 'n'), amod='c_adj'),

            # $ sid 'Apa tujuan mereka?' (ja="彼らの目的は何ですか？")
            pat(5).verb(matchins('apa'), acl=agency),
            # $ sid 'Bau apa itu?' (en="What's that smell?", zh="那是什么味道？")
            pat(5).verb(behaveof('perception', 'n'), acl=matchins('apa')),
            # $ sid 'Bagaimana tenggorokanmu?' (zh="喉咙怎么样？")
            pat(5).verb(behaveof('body_part', 'n'), amod=matchins({'bagaimana'}, 'in')),
            # $ sid "Mengapa lehermu sakit?" (Why does your neck hurt?)
            pat(5).verb(behaveof('body_part', 'n'), advmod=matchins({'mengapa'}, 'in'), amod=kindof('ill', 'a')),
            # $ sid 'Dada mereka tidak sakit.'
            # $ sid 'Lidah saya kering.','Perut saya sakit.'
            pat(5).verb(behaveof('body_part', 'n'), amod='c_adj'),
            # $ sid 'Karpet ini sangat kotor.'
            pat(5, name='describe_object').verb(behaveof('object', 'n'), amod='c_adj'),

            # $ sid 'Bola Dimas putih.'  ("白色迪马斯球。")
            # ┌──────┐  root   ┌────────┐  flat   ┌───────┐  amod   ┌───────┐
            # │ ROOT │ ──────▶ │  Bola  │ ──────▶ │ Dimas │ ──────▶ │ putih │
            # └──────┘         └────────┘         └───────┘         └───────┘
            #                    │
            #                    │ punct
            #                    ▼
            #                  ┌────────┐
            #                  │   .    │
            #                  └────────┘
            pat(5, 'describe_color').root(behaveof('object', 'n'),
                                          anal(amod=predicate_fn('color', 'n'))),
            # $ sid 'Karpet di kantor saya abu-abu.' (en="The carpet in my office is gray.")
            #                                     ┌−−−−−−−−┐
            #                                     ╎  saya  ╎
            #                                     └−−−−−−−−┘
            #                                       ▲
            #                                       │ det
            #                                       │
            # ┌−−−−−−┐  root   ┌────────┐  nmod   ┌────────┐  amod   ┌−−−−−−−−−┐
            # ╎ ROOT ╎ ──────▶ │ Karpet │ ──────▶ │ kantor │ ──────▶ ╎ abu-abu ╎
            # └−−−−−−┘         └────────┘         └────────┘         └−−−−−−−−−┘
            #                    │                  │
            #                    │ punct            │ case
            #                    ▼                  ▼
            #                  ┌−−−−−−−−┐         ┌────────┐
            #                  ╎   .    ╎         │   di   │
            #                  └−−−−−−−−┘         └────────┘
            pat(5, 'describe_object_chunk').root(behaveof('object', 'n'),
                                          anal(amod=predicate_fn('entity', 'n'))),
            # $ sid 'Siapa orang terpenting di kantormu?'
            # ┌−−−−−−┐  root   ┌−−−−−−−−┐  acl   ┌−−−−−−−−−−−−┐  nmod   ┌−−−−−−−−−−┐  case   ┌−−−−┐
            # ╎ ROOT ╎ ──────▶ ╎ Siapa  ╎ ─────▶ ╎   orang    ╎ ──────▶ ╎ kantormu ╎ ──────▶ ╎ di ╎
            # └−−−−−−┘         └−−−−−−−−┘        └−−−−−−−−−−−−┘         └−−−−−−−−−−┘         └−−−−┘
            #                    │                 │
            #                    │ punct           │ amod
            #                    ▼                 ▼
            #                  ┌−−−−−−−−┐        ┌−−−−−−−−−−−−┐
            #                  ╎   ?    ╎        ╎ terpenting ╎
            #                  └−−−−−−−−┘        └−−−−−−−−−−−−┘
            pat(5, name='pred_people').root(interr_root('who'),
                                            any_path('acl/amod', 'first', 'a'),
                                            any_path('acl/nmod', 'organization', 'n'),
                                            acl=kindof('people', 'n')),
            # $ sid 'Tidak banyak pohon di gurun.'
            pat(5, name='noun_desc').root(comps(noun_desc=True)),
        ])

    def execute(self):
        from sagas.nlu.ruleset_procs import print_root_domains
        super().execute()
        # $ sid 'Ada ujian matematika di sekolah ini.'
        print_root_domains(self.meta['sents'], self.meta['lang'],
                           ['compound', 'amod', 'nsubj', 'obj', 'nmod'])
