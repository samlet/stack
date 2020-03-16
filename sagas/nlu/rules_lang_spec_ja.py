from typing import Text, Any, Dict, List, Union
from sagas.nlu.inferencer import extensions, DomainToken, InferPart
from sagas.nlu.inferencer_common import get_all_plains
from sagas.nlu.inspector_common import Inspector, Context
from sagas.nlu.registries import registry_named_exprs
from .rules_header import *
import sagas.tracker_fn as tc

def get_from_to(c:InferPart,t):
    results=[]
    if 'カラ' in c.domain.rels:
        results.append((4, "extract_for('plain', 'カラ')"))
    if 'マデ' in c.domain.rels:
        results.append((4, "extract_for('plain', 'マデ')"))
    return results

extensions.register_parts('ja',{
    '時間': lambda c,t: (4, "extract_for('plain+date_search+date_parse', '時間')"),
    'ガ': lambda c,t: (4, "extract_for('plain', 'ガ')"),
    'デ': lambda c,t: (4, "extract_for('plain', 'デ')"),
    'ニ': lambda c,t: (4, "extract_for('plain', 'ニ')"),
    '修飾': lambda c,t: (4, "extract_for('plain+number', '修飾')"),
    'カラ': lambda c,t: get_from_to(c,t),
    'マデ': lambda c,t: get_from_to(c,t),
})


def get_verb_interr(c:DomainToken, part:Text):
    return 4, "interr_root('??')"

extensions.register_domains('ja',{
    'verb': lambda c,t: get_verb_interr(c,t),
})
registry_named_exprs(
    # test notes: procs-jsonpath.ipynb
    from_to=lambda rs: (['from','to'],
                        get_all_plains(rs, '$[?inspector = "extract_comps" & provider = "plain"].value')),
    transport=lambda rs: (['transport_cat', 'transport_name'],
                          get_all_plains(rs, '$[?inspector = "kind_of" & part = "デ"].value.category,word')),
)

class Rules_ja(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_ja(Japanese, 日本语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj=(self.pat, self.actions_obj)

        self.collect(pats=[
            # $ duckling '二つ' ja
            # $ sja '庭に植物を二つ植えた。'
            # $ sja '庭に木を植えた。'
            pat(5, name='behave_plant').verb(extract_for('number', 'nummod'),
                                             extract_for('plain', 'iobj'),
                                             behaveof('plant', 'v'),
                                             obj=kindof('living_thing', 'n')),
            # $ sja '祖父は九十歳まで生きた。'
            pat(5, name='desc_live').verb(extract_for('number', 'obl'),
                                          extract_for('plain', 'nsubj'),
                                          behaveof('live', 'v'), nsubj=agency),
            # $ sja '祖父は五年前に九十歳で死んだ。'  ('My grandfather died five years ago at the age of ninety.')
            pat(5, name='desc_died').verb(extract_for('time', 'iobj'),
                                          extract_for('number', 'obl'),
                                          extract_for('plain', 'nsubj'),
                                          behaveof('die', 'v'), nsubj=agency),
        ])

    def predicate_rules(self):
        pat, actions_obj=(self.pat, self.actions_obj)

        self.collect(pats=[
            # $ sj "子は羊を聞きません。"
            pat(5, name='perceive_living').verb(behaveof('perceive', 'v'),
                                                                    ガ=kindof('living_thing', 'n')),
            # $ sj 'このお土産はきれいで安いです。'
            # [predicate](安いです。/anidesu.) It's cheap.
            # 	[ガ](御土産/yu tu chan) Souvenir
            # 	[修飾](綺麗だ/qi lida) Beautiful
            # +----+-------+---------+----------+----------+------------+--------------+
            # |    | rel   |   index | text     | lemma    | children   | features     |
            # |----+-------+---------+----------+----------+------------+--------------|
            # |  0 | ガ    |       1 | お土産は | 土産     | 御, 土産.. | c_x, x_p..   |
            # |  1 | 修飾  |       2 | きれいで | きれいで | 綺麗だ..   | c_adj, x_j.. |
            # +----+-------+---------+----------+----------+------------+--------------+
            pat(5, name='describe_cheap').verb(behaveof('cheap', 'a'),
                                                ガ=kindof('present', 'n')),
            # $ sj '彼のパソコンは便利じゃない。'
            # $ sj 'コンビニは便利で安い。'
            pat(3, name='describe_artifact').subj('adj',
                                               ガ=kindof('artifact', 'n')),
            # $ sj 'コンビニは便利で安い。'
            pat(3, name='describe_noun').subj('adj', ガ='c_noun'),

            # $ sj '肉料理をたくさん注文しました。'
            # $ python -m sagas.ja.knp_cli parse "どのおかずを注文したの？"
            # $ sj "どのおかずを注文したの？"
            pat(5, name='behave_order').verb(extract_for('plain', 'ヲ'),
                                             extract_for('plain', '修飾'),
                                             behaveof('order', 'v'),),
            # $ sj 'それはどんな味ですか？'
            pat(5, name='ask_taste').verb(extract_for('plain', 'ガ'),
                                          behaveof('taste', '*'), ),
            # $ sj 'このお茶はとても苦い。'
            pat(5, name='describe_taste').verb(extract_for('plain', '_'),
                                               extract_for('plain', 'ガ'),
                                               extract_for('plain', '修飾'),
                                               behaveof('bitter', 'a'),),

            # $ sj 'どんなおかずが好きですか？'
            pat(-5, name='desc_fav').verb(extract_for('plain', 'ガ'),
                                          interr('fav', is_part=False),),
            # $ sj 'ケーキの甘みが好きじゃなかった。'
            pat(-5, name='desc_fav_not').verb(
                extract_for('plain', 'ガ'),
                interr('fav', is_part=False),
                checker(has_lemma='ない'),),
            pat(-5, name='desc_fav_neg').verb(
                extract_for('plain', 'ガ'),
                interr('fav', is_part=False),
                checker(negative='_'), ),

            # $ sj '風が北から南に変わった。'
            # +----+-------+---------+--------+---------+------------+---------------+
            # |    | rel   |   index | text   | lemma   | children   | features      |
            # |----+-------+---------+--------+---------+------------+---------------|
            # |  0 | ガ    |       0 | 風が   | 風      | 風..       | c_noun, x_n.. |
            # |  1 | ニ    |       1 | 北から | 北      | 北..       | c_noun, x_n.. |
            # |  2 | ニ    |       2 | 南に   | 南      | 南..       | c_noun, x_n.. |
            # +----+-------+---------+--------+---------+------------+---------------+
            pat(5, name='ask_taste').verb(extract_for('plain', 'ニ'),
                                          behaveof('turn', 'v'),
                                          ガ=kindof('natural_phenomenon/process', 'n')),
            # $ sj 父は私にとてもきびしかった。
            # $ sj 本田先生は学生たちにきびしそうだ。
            chained(pat(5, name='desc_attitude'),
                    subj('adj', ガ=agency),
                    verb(extract_for('plain', 'ガ'),
                         extract_for('plain', 'ニ'),
                         extract_for('plain', '修飾'),
                         specsof('*', 'tight'),
                         )
                    ),
            pat(-5, name='desc_attitude_type').verb(specsof('*', 'tight')),
            # $ sj '予約を火曜日から木曜日に変えてもらった。'
            pat(5, name='change_statement').verb(extract_for('plain+date_search+date_parse', '時間'),
                                                 specsof('v', 'change'),
                                                 ヲ=kindof('statement', 'n')
                                                 ),
            # $ sj '日本はアメリカに比べて小さいです。'
            # $ sj '太陽は月に比べて大きいです。'
            pat(5, name='describe_compare').verb(
                extract_for('plain', 'ガ'),
                checker(has_rel='ニクラベル'),
                specsof('*', 'little', 'large'),),

            # infers ------
            # $ sj '予約を火曜日から木曜日に変えてもらった。'
            pat(5, name='predict_convert').verb(extract_for('plain+date_search+date_parse', '時間'),
                                                specsof('*', 'convert'), ヲ=kindof('booking', '*')),
            # $ sj 'ケーキが一つ残っている。'
            pat(5, name='predict_stay').verb(extract_for('plain+number', '修飾'), specsof('*', 'stay'),
                                             ガ=kindof('food', 'n')),
            # $ sj '牛乳を流しに注いだ。'
            # $ sj '古いビールを流しに注ぐ。'  (I will pour the old beer into the sink.)
            pat(5, name='predict_pour').verb(tags('pour_liquid'), specsof('*', 'pour'),
                                             ヲ=kindof('liquid', 'n'),
                                             ニ=kindof('kitchen_sink', '*')),
            # $ sj '流しを8つ直した。'
            pat(5, name='predict_heal').verb(series('events',
                                                    action='specs_of:category',
                                                    object='kind_of:category',
                                                    _count='ins_date:$[0].value.value'),
                                             specsof('v', 'correct'),
                                             修飾=dateins('number'),
                                             ヲ=kindof('artifact', 'n')),
            # $ sj 'オーブンを百八十度に温めてください。'
            pat(5, name='predict_heat').verb(specsof('*', 'heat'),
                                             extract_for('plain+temperature', 'ニ'),
                                             ヲ=kindof('oven', '*'),
                                             ニ=kindof('degree', '*')),
            # $ sj '新幹線で東京から大阪まで行きました。'
            # pat(5, name='predict_proceed').verb(slots('transport', fn='from_to,transport'),
            pat(5, name='predict_proceed').verb(slots('transport', fn='from_to,transport', driver='cache+tracker'),
                                                extract_for('plain', 'カラ'),
                                                extract_for('plain', 'マデ'),
                                                specsof('*', 'proceed'),
                                                checker(has_all_rels=['カラ', 'マデ']),
                                                デ=kindof('public_transport', 'n')),
            # $ sj '建物の裏に駐車しました。'
            pat(5, name='predict_parking').verb(specsof('*', 'parking'),
                                                understructure('ニ'),
                                                ニ=kindof('back', '*')),
            # $ sj '紙の裏に書いてください。'
            pat(5, name='predict_write').verb(specsof('*', 'write'),
                                              understructure('ニ'),
                                              ニ=kindof('back', '*')),

        ])

    # def execute(self):
    #     super().execute()


