from sagas.nlu.inspectors import NegativeWordInspector as negative
from sagas.nlu.inspectors import DateInspector as dateins
from sagas.nlu.inspectors import EntityInspector as entins
from sagas.nlu.inspectors import MatchInspector as matchins
from sagas.nlu.inspector_wordnet import PredicateWordInspector as kindof
from sagas.nlu.inspector_wordnet import VerbInspector as behaveof
from sagas.nlu.inspector_rasa import RasaInspector as intentof
from sagas.nlu.lang_spec_intf import LangSpecBase, agency

from sagas.nlu.patterns import Patterns, print_result
import sagas.tracker_fn as tc

class Rules_id(LangSpecBase):
    def verb_rules(self):
        domains, meta = (self.domains, self.meta)
        self.collect(pats=[
            # $ sid 'Pekerjaan ini dimulai oleh mereka.' (This job is started by them.)
            Patterns(domains, meta, 2, name='behave_di_obl').verb(nsubj_pass=agency, obl=agency),
            # $ sid 'Makanan ini disebut nasi goreng.' (en="This food is called nasi goreng.")
            Patterns(domains, meta, 2, name='behave_di_obj').verb(nsubj_pass=agency, obj=agency),
            Patterns(domains, meta, 2, name='food').verb(obj = kindof('food/physical_entity', 'n')),
            # $ sid 'Raja dan ratu dianggap jahat.' (en="The king and queen are considered evil.")
            Patterns(domains, meta, 2, name='behave_di_amod').verb(nsubj_pass=agency, amod='c_adj'),
            # $ sid 'Surat-surat mereka dibuat di sini.'
            Patterns(domains, meta, 2, name='behave_di_case').verb(nsubj_pass=agency, case=agency),
            # $ sid 'Saya diduga membantu polisi.' (I am suspected of helping the police.)
            Patterns(domains, meta, 2, name='behave_di_xcomp').verb(nsubj_pass=agency, xcomp='c_verb'),
            # Kadang-kadang kami mandi di sungai. 有时我们在河里洗澡。
            Patterns(domains, meta, 5, name='behave_cleanse').verb(behaveof('cleanse/better', 'v')),
            # Lemari besar itu tidak terangkat. 那个大柜子抬不动。
            Patterns(domains, meta, 5, name='move_unable').verb(behaveof('move', 'v'), advmod=negative()),
            # Dia datang ke Shanghai untuk menjumpai adiknya. 他为了见弟弟来到了上海。
            Patterns(domains, meta, 5, name='behave_purpose').verb(
                behaveof('arrive', 'v'), nsubj=agency, xcomp='c_verb', obl=agency, ),

            # $ sid 'Siapa yang menulis laporan ini?'
            Patterns(domains, meta, 5, name='ask_event').verb(
                behaveof('write', 'v'), head_acl=matchins('siapa'), nsubj=agency, obj=agency, ),
            # $ sid 'Tujuan saya adalah mengubah kamu.' (My goal is to change you.)
            Patterns(domains, meta, 5, name='behave_cleanse').verb(behaveof('change', 'v'), nsubj=kindof('motivation', 'n')),
            ])

    def root_rules(self):
        domains, meta=(self.domains, self.meta)
        self.collect(pats=[
            Patterns(domains, meta, 1).verb(nsubj=agency, obj=agency),
            # $ sid 'Berapa umur kamu?' (en="How old are you?")
            Patterns(domains, meta, 5, name='years_old').verb(behaveof('age', 'n'), amod='c_det'),
            # $ sid 'Bola putih.' (球是白的)
            # notice: 'Bola Dimas putih.'无法匹配这条规则, 因为'Bola Dimas'是flat关系,
            # 针对id中的flat关系, 需要单独处理, 将flat关系的token合并为chunk, 然后再处理这个chunk与外界之间的关系.
            Patterns(domains, meta, 5).verb(behaveof('physical_entity', 'n'), amod=kindof('color', 'n')),
            # $ sid 'Apa tujuan mereka?' (ja="彼らの目的は何ですか？")
            Patterns(domains, meta, 5).verb(matchins('apa'), acl=agency),
            ])


