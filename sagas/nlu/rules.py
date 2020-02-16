from typing import Text, Dict, Any

from sagas.nlu.patterns import print_result
from sagas.nlu.rules_header import *

import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)

#⊕ [nmod](https://universaldependencies.org/u/dep/nmod.html)
def verb_patterns(meta, domains):
    behaviours_obl = lambda rs: [Patterns(domains, meta, 5).verb(behaveof(r, 'v'), obl='c_noun') for r in rs]
    actions_obl = lambda rs: [Patterns(domains, meta, 5).verb(behaveof(r[0], 'v'), obl=kindof(r[1], 'n')) for r in rs]
    actions_obj = lambda rs: [Patterns(domains, meta, 5).verb(behaveof(r[0], 'v'), obj=kindof(r[1], 'n')) for r in rs]
    actions_vob = lambda rs: [Patterns(domains, meta, 5).verb(behaveof(r[0], 'v'), __engine='ltp', vob=kindof(r[1], 'n')) for r in rs]
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
          Patterns(domains, meta).verb(__engine='corenlp', obj=agency),

          # 关系parataxis用于一对可能是独立句子的东西，但它们被一起作为一个句子对待。
          # $ sd 'Diese Liga ist die beste Liga, glaube ich.' ([en] This league is the best league, I think.)
          Patterns(domains, meta).verb(_rel='parataxis', nsubj=agency),
          # 子句的依赖关系匹配:
          # $ ses 'Yo hago ejercicio porque cuido mi cuerpo.'
          Patterns(domains, meta, 5).verb(_rel='advcl', obj=agency),

          # Passive-Voice: Sie werden nicht berücksichtigt.
          Patterns(domains, meta, 1).verb(nsubj_pass=agency, aux_pass='c_aux'),
          Patterns(domains, meta, 2).verb(nsubj_pass=agency, aux_pass='c_aux', advmod=negative()),

          # 匹配否定词: Han har ikke tøjet på.
          Patterns(domains, meta, 2).verb(nsubj=agency, obj=agency, advmod=negative()),

          # 匹配日期维: I was born in the spring of 1982.
          Patterns(domains, meta, 2).verb(nsubj_pass=agency, obl=dateins('time')),
          # $ sd 'Die Aufnahmen begannen im November.'
          Patterns(domains, meta, 5).verb(nsubj=agency, obl=dateins('time')),

          # 匹配实体: I was born in Beijing.
          Patterns(domains, meta, 2).verb(nsubj_pass=agency, obl=entins('GPE')),
          # $ sr 'Я работаю в китае.'
          Patterns(domains, meta, 5).verb(nsubj=agency, obl=entins('location')),

          # 匹配继承链: O homem fica amarelo.
          Patterns(domains, meta, 2).verb(nsubj=agency, xcomp=kindof('color', 'n')),
          Patterns(domains, meta, 2).verb(nsubj=kindof('activity', 'n')),

          # $ se 'They read these newspapers.'
          # $ sid 'Mereka membaca koran-koran ini.'
          Patterns(domains, meta, 5).verb(nsubj=agency, obj=kindof('print_media/artifact', 'n')),

          # health theme _________
          # $ ses '¿Te duelen las piernas?' (zh="你的腿受伤了吗？")
          Patterns(domains, meta, 5).verb(behaveof('suffer', 'v'), nsubj=kindof('body_part', 'n')),
          # $ sz "吸烟对你的健康有害。"
          Patterns(domains, meta, 5).verb(behaveof('consume', 'v'), cmp='c_adp'),
          # $ se 'Do it correctly.'
          Patterns(domains, meta, 5, name='command_do').verb(behaveof('make', 'v'), advmod='c_adv'),

          # $ se 'That spider flies.'
          # $ sid 'Burung dan kupu-kupu terbang.'
          # $ sid 'Laba-laba tersebut terbang.'  (这个句子使用的是单词原型'Laba-laba', 而不是词干lemma)
          Patterns(domains, meta, 5, name='describe_animal_behave')
              .verb(behaveof('travel', 'v'), nsubj=kindof('animal', 'n')),
          # $ sid 'Burung itu suka makan serangga.' (zh="鸟喜欢吃虫子。")
          Patterns(domains, meta, 5, name='describe_animal_hobby')
              .verb(behaveof('like', 'v'), nsubj=kindof('animal', 'n')),

          # 匹配行为: Ayer Roberto cenó en un restaurante excelente.
          *behaviours_obl(['eat/consume']),
          # 匹配行为与对象:
          # $ se 'What do you think about the war?'
          *actions_obl([('evaluate', 'group_action/event'),
                        ('examine', 'interest/state'),
                        # (id) Ular besar keluar dari dalam lubang. 大蛇从洞里出来。
                        ('leave', 'space/location'),
                        ]),
          # $ sd 'Wie untersuchen Sie diese Angelegenheit?'
          *actions_obj([('evaluate', 'group_action/event'),
                        ('examine', 'interest/state'),
                        # $ sid 'saya punya anjing'  (en="i have a dog")
                        ('own', 'animal/organism'),
                        # $ sid 'Kalian punya jeruk.'  (en="You have oranges.")
                        ('own', 'fruit/food'),
                        # $ sid 'Mereka membaca koran-koran ini.'  (They read these newspapers.)
                        # $ se 'They read these newspapers.'
                        ('interpret/understand', 'print_media'),
                        # (id) Saya main bola keranjang tiap-tiap pagi. 我每天早上打篮球。
                        ('play', 'game_equipment'),
                        # (id) Polis telah menangkap dua orang pencuri. 警察已经抓住了两个小偷。
                        ('catch', 'criminal/person'),
                        # $ se 'Who initiates this attack?'
                        # $ sid 'Siapa yang memulai serangan ini?'
                        ('cause', 'event'),
                        ]),

          # 匹配意图(全句或chunk)
          # $ sd 'Ich stimme dir in diesem Punkt nicht zu.'
          Patterns(domains, meta, 5).verb(nsubj=agency, obl=intentof('context_indicator', 0.6, False)),

          # 匹配中文的成分
          # $ sz '搞外遇。'
          Patterns(domains, meta, 5).verb(__engine='ltp', vob=kindof('sexual_intercourse/organic_process', 'n')),
          *actions_vob([('copulate', 'sexual_intercourse/organic_process'),]),

          # $ sz '你有几台笔记本电脑？'  (如果使用ltp但禁用predicates, 如果启用predicates, 则vob成份就改为a1)
          Patterns(domains, meta, 5).verb(behaveof('have', 'v'), __engine='ltp',
                                          vob=intentof('how_many', 0.75)),
          *actions_vob([('have', 'device/artifact'),]),

          # 成分提取
          # $ sit 'Non abbiamo riscaldamento.'  ("我们没有暖气。")
          Patterns(domains, meta, 5, name='describe_have_not')
              .verb(extract_for('plain', 'obj'),
                    behaveof('have', 'v'),
                    advmod=kindof('not', '*'), obj='c_noun'),
          ]
    print_result(pats)

def aux_patterns(meta, domains):
    # agency = ['c_pron', 'c_noun', 'c_propn']
    things = lambda rs: [Patterns(domains, meta, 5).aux('noun', nsubj=kindof(r, 'n')) for r in rs]
    categories= lambda rs: [Patterns(domains, meta, 5).cop(behaveof(r, 'n'), nsubj=agency) for r in rs]
    pats=[Patterns(domains, meta).aux('pron', 'noun', nsubj=agency, cop='c_aux'),
          # Eine Teilnahme ist kostenlos. (Attendance is free of charge.)
          Patterns(domains, meta).aux('adj', nsubj=agency, cop='c_aux'),
          # Wir haben ihn zum Bürgermeister gewählt. ([en] We chose him as mayor.)
          Patterns(domains, meta).aux('pron', 'noun', nsubj_pass=agency, cop='c_aux'),
          # Dies war der erste Sieg seiner Karriere. ([en] This was the first victory of his career.)
          Patterns(domains, meta).aux('noun', nsubj=agency, cop='c_aux', amod='c_adj', nmod='c_noun'),
          # Ben kimim?
          Patterns(domains, meta).aux('pron', 'noun', aux_q='c_aux'),

          # 匹配继承链:
          # $ ses 'Este juego es facilísimo.' ([en] This game is very easy.)
          Patterns(domains, meta, 2).aux('adj', nsubj=kindof('activity', 'n')),
          Patterns(domains, meta, 2).aux('adj', nsubj=kindof('person', 'n')),
          Patterns(domains, meta, 2).aux('adj', nsubj=kindof('fruit', 'n')),

          # 匹配自然现象
          # $ se "what will be the weather in three days ?"
          Patterns(domains, meta, 5).cop(behaveof('weather/phenomenon', 'n'), nsubj=agency, cop='c_aux'),
          Patterns(domains, meta, 5).cop(behaveof('weather/phenomenon', 'n'),
                                         nsubj=agency, cop='c_aux',
                                         nmod=dateins({'snips/date', 'snips/datetime'},
                                                      provider='snips')),

          # $ se "How many files are there?"
          Patterns(domains, meta, 5).aux('adv', nsubj=kindof('file/communication', 'n'),
                                         cop=kindof('be', 'v')),  ## 因为behaveof取得是key, 而kindof取得是词干

          # La manzana es una fruta saludable. ([zh] 苹果是一种健康的水果。)
          *things(['fruit', 'food']),
          # Leopard is a beast.
          *things(['animal/living_thing', 'animal_product/material']),
          # $ se 'He is an optimist.'
          *categories(['person/organism']),

          # 匹配意图(全句或chunk)
          # $ sd 'Shenzhen ist das Silicon Valley für Hardware-Firmen'
          Patterns(domains, meta, 5).entire(intentof('tech', 0.6, True)),
          # $ sd 'Die Nutzung der Seite ist kostenlos.'
          Patterns(domains, meta, 5).aux('adj', nsubj=intentof('using', 0.6, False), cop='c_aux'),
          ]
    print_result(pats)

def subj_patterns(meta, domains):
    # agency = ['c_pron', 'c_noun', 'c_propn']
    descs= lambda rs: [Patterns(domains, meta, 5).subj('pron', 'noun', nsubj=kindof(r, 'n')) for r in rs]
    props = lambda rs: [Patterns(domains, meta, 5).subj('pron', 'noun',
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

def predict_patterns(meta, domains):
    print('... predict patterns')
    pats=[Patterns(domains, meta, 5).verb(behaveof('have', 'v'), __engine='ltp', vob=intentof('how_many', 0.75)),
          # $ sz '有多少文件'
          Patterns(domains, meta, 5).verb(behaveof('have', 'v'), __engine='ltp', a1=kindof('file/communication', 'n')),
          # $ sz '包含几个文件'
          Patterns(domains, meta, 5).verb(behaveof('include', 'v'), __engine='ltp', a1=kindof('file/communication', 'n')),
          # $ sz '你有几台笔记本电脑？'
          Patterns(domains, meta, 5).verb(behaveof('have', 'v'), __engine='ltp',
                                          a1=intentof('how_many', 0.75)),

          # $ sj "ファイルはいくつありますか？"
          Patterns(domains, meta, 5).verb(behaveof('exist', 'v'), __engine='knp',
                                          修飾='c_num', ガ=kindof('file/communication', 'n')),
          # $ sj "いくつかのファイルが含まれています"
          Patterns(domains, meta, 5).verb(behaveof('include', 'v'), __engine='knp',
                                          ガ=kindof('file/communication', 'n')),
          # $ sj "子は羊を聞きません。"
          Patterns(domains, meta, 5, name='perceive_living').verb(behaveof('perceive', 'v'),
                                          ガ=kindof('living_thing', 'n')),
          # Patterns(domains, meta, 3, name='describe_artifact').aux('adj',
          #                                       ガ=kindof('artifact', 'n')),
          ]
    print_result(pats)
