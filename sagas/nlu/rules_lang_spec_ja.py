from .rules_header import *

class Rules_ja(LangSpecBase):
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
            ])

    # def execute(self):
    #     super().execute()


