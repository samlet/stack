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
            ])

    def execute(self):
        super().execute()


