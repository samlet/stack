from sagas.nlu.inspectors import NegativeWordInspector as negative
from sagas.nlu.inspectors import DateInspector as dateins
from sagas.nlu.inspectors import EntityInspector as entins
from sagas.nlu.inspector_wordnet import PredicateWordInspector as kindof
from sagas.nlu.inspector_wordnet import VerbInspector as behaveof

from sagas.nlu.patterns import Patterns, print_result

agency=['c_pron', 'c_noun', 'c_propn']
#⊕ [nmod](https://universaldependencies.org/u/dep/nmod.html)
def verb_patterns(meta, domains):
    behaviours_obl = lambda rs: [Patterns(domains, meta, 2).verb(behaveof(r, 'v'), obl='c_noun') for r in rs]
    pats=[Patterns(domains, meta, 1).verb(nsubj=agency, obj=agency),
          # 复合动词: Drengen har nederdelen på. (har..på是一个动词) ([en] The boy is wearing the skirt.)
          Patterns(domains, meta, 2).verb(compound_prt='c_adv', nsubj=agency, obj=agency),
          # 连接另一个动词: Pigerne spiser måltidet og drikker teen. ([en] The girls eat the meal and drink the tea.)
          Patterns(domains, meta).verb(nsubj=agency, obj=agency, conj='c_verb'),
          # nmod: nominal modifier
          # The nmod relation is used for nominal dependents of another noun or noun phrase and functionally corresponds to an attribute, or genitive complement.
          Patterns(domains, meta).verb(nsubj=agency, cop='c_aux', nmod=agency),
          # obl: oblique nominal
          # The obl relation is used for a nominal (noun, pronoun, noun phrase) functioning as a non-core (oblique) argument or adjunct. This means that it functionally corresponds to an adverbial attaching to a verb, adjective or other adverb.
          Patterns(domains, meta).verb(nsubj=agency, obl=agency),
          # advmod: adverbial modifier
          # An adverbial modifier of a word is a (non-clausal) adverb or adverbial phrase that serves to modify a predicate or a modifier word.
          Patterns(domains, meta).verb(nsubj=agency, advmod='c_adv'),
          # Wir können tanzen, wenn wir wollen. ([en] We can dance if we want. [zh] 如果我们想要，我们可以跳舞。)
          Patterns(domains, meta).verb(nsubj=agency, advcl='c_aux'),
          # Ben okuldayım. ([en] I'm in school.)
          Patterns(domains, meta).verb(nsubj=agency),
          # Φοράω το μάλλινο παλτό μου. ([en] I wear my wool coat.)
          Patterns(domains, meta).verb(obj=agency),
          # 关系parataxis用于一对可能是独立句子的东西，但它们被一起作为一个句子对待。
          # Diese Liga ist die beste Liga, glaube ich. ([en] This league is the best league, I think.)
          Patterns(domains, meta).verb(_rel='parataxis', nsubj=agency),

          # Passive-Voice: Sie werden nicht berücksichtigt.
          Patterns(domains, meta, 1).verb(nsubj_pass=agency, aux_pass='c_aux'),
          Patterns(domains, meta, 2).verb(nsubj_pass=agency, aux_pass='c_aux', advmod=negative()),

          # 匹配否定词: Han har ikke tøjet på.
          Patterns(domains, meta, 2).verb(nsubj=agency, obj=agency, advmod=negative()),
          # 匹配日期维: I was born in the spring of 1982.
          Patterns(domains, meta, 2).verb(nsubj_pass=agency, obl=dateins('time')),
          # 匹配实体: I was born in Beijing.
          Patterns(domains, meta, 2).verb(nsubj_pass=agency, obl=entins('GPE')),

          # 匹配继承链: O homem fica amarelo.
          Patterns(domains, meta, 2).verb(nsubj=agency, xcomp=kindof('color', 'n')),
          Patterns(domains, meta, 2).verb(nsubj=kindof('activity', 'n')),

          # 匹配行为: Ayer Roberto cenó en un restaurante excelente.
          *behaviours_obl(['eat/consume']),
          ]
    print_result(pats)

def aux_patterns(meta, domains):
    # agency = ['c_pron', 'c_noun', 'c_propn']
    things = lambda rs: [Patterns(domains, meta, 2).aux('noun', nsubj=kindof(r, 'n')) for r in rs]
    pats=[Patterns(domains, meta).aux('pron', 'noun', nsubj=agency, cop='c_aux'),
          # Eine Teilnahme ist kostenlos. (Attendance is free of charge.)
          Patterns(domains, meta).aux('adj', nsubj=agency, cop='c_aux'),
          # Wir haben ihn zum Bürgermeister gewählt. ([en] We chose him as mayor.)
          Patterns(domains, meta).aux('pron', 'noun', nsubj_pass=agency, cop='c_aux'),
          # Dies war der erste Sieg seiner Karriere. ([en] This was the first victory of his career.)
          Patterns(domains, meta).aux('noun', nsubj=agency, cop='c_aux', amod='c_adj', nmod='c_noun'),
          # Ben kimim?
          Patterns(domains, meta).aux('pron', 'noun', aux_q='c_aux'),

          # 匹配继承链: Este juego es facilísimo. ([en] This game is very easy.)
          Patterns(domains, meta, 2).aux('adj', nsubj=kindof('activity', 'n')),
          Patterns(domains, meta, 2).aux('adj', nsubj=kindof('person', 'n')),
          Patterns(domains, meta, 2).aux('adj', nsubj=kindof('fruit', 'n')),

          # La manzana es una fruta saludable. ([zh] 苹果是一种健康的水果。)
          *things(['fruit', 'food']),
          # Leopard is a beast.
          *things(['animal/living_thing', 'animal_product/material']),
          ]
    print_result(pats)

def subj_patterns(meta, domains):
    # agency = ['c_pron', 'c_noun', 'c_propn']
    descs= lambda rs: [Patterns(domains, meta, 2).subj('pron', 'noun', nsubj=kindof(r, 'n')) for r in rs]
    props = lambda rs: [Patterns(domains, meta, 2).subj('pron', 'noun',
                                                        nsubj=kindof(r, 'n'),
                                                        amod='c_adj'
                                                        ) for r in rs]
    pats=[Patterns(domains, meta).subj('pron', 'noun', nsubj=agency),
          # O nasıl? ([en] Who am I?)
          Patterns(domains, meta).subj('adv', nsubj=agency),
          # Tuvalette örümcek var. ([en] There's a spider in the bathroom.)
          Patterns(domains, meta).subj('adj', nsubj=agency, obl=agency),
          # Banyoda kadınlar var. ([en] There are women in the bathroom.)
          Patterns(domains, meta).subj('adj', nsubj=['x_nadj'], obl=agency),
          # Solda bir köpek var. ([en] There's a dog on the left. [ja] 左側に犬がいます。)
          Patterns(domains, meta).subj('adj', nsubj=agency, amod='c_adj'),
          # Ankara'da çok kedi var. ([en] There are many cats in Ankara. [ja] アンカラにはたくさんの猫がいます。)
          Patterns(domains, meta).subj('adj', nsubj=agency, obl='c_propn'),
          # Ne kadar sütümüz var? ([en] How much milk do we have?)
          Patterns(domains, meta).subj('adj', nsubj=agency),
          # Яблоко - это здоровый фрукт. ([zh] 苹果是一种健康的水果。)
          *descs(['food/matter']),
          # $ sr 'Яблоко - это здоровый фрукт.'
          *props(['food/matter']),
          ]
    print_result(pats)
