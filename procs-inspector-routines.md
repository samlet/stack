# procs-inspector-routines.md
## 1. CheckerInspector
    """
    Instances: checker(has_lemma='ない'),
        checker(negative='_'),
        checker(has_rel='ニクラベル'),
        checker(has_num='verb:obj'),
        checker(has_all_rels=['カラ', 'マデ']),

    >>> pat(3, name='obj_num').verb(checker(has_num='verb:obj'), ),
    """

```python
checker(has_lemma='ない'),
checker(negative='_'),
checker(has_rel='ニクラベル'),
checker(has_num='verb:obj'),
checker(has_all_rels=['カラ', 'マデ']),

pat(3, name='obj_num').verb(checker(has_num='verb:obj'), ),
```

## 2. CompExtractInspector
    """
    提取指定成分:
    Instances:
        extract_for('chunk+chunk_text', 'verb:xcomp/obj'),
        nsubj=extract('plain+date_search+date_parse'),
        extract_for('plain+date_search+date_parse', '時間'),
        extract_for('plain+translit', 'obj'),
        extract_for('number', 'obl'),
        extract_for('time', 'advmod'),
        extract_for('plain+temperature', 'ニ'),
        extract_for('rasa', '_')
        extract_for('chunk', 'verb:xcomp/obj')
        extract_for('ner', '_'), extract_for('ner', 'xcomp')

    >>> pat(3, name='extract_day').cop(behaveof('day', 'n'),
          flat=kindof('feast_day/day', 'n'),
          nsubj=extract('plain+date_search+date_parse')),
    """

```python
extract_for('chunk+chunk_text', 'verb:xcomp/obj'),
nsubj=extract('plain+date_search+date_parse'),
extract_for('plain+date_search+date_parse', '時間'),
extract_for('plain+translit', 'obj'),
extract_for('number', 'obl'),
extract_for('time', 'advmod'),
extract_for('plain+temperature', 'ニ'),
extract_for('rasa', '_')
extract_for('chunk', 'verb:xcomp/obj')
extract_for('ner', '_'), extract_for('ner', 'xcomp')

pat(3, name='extract_day').cop(behaveof('day', 'n'),
          flat=kindof('feast_day/day', 'n'),
          nsubj=extract('plain+date_search+date_parse')),
```

## 3. CompsInspector
    """
    # $ sid 'Tidak banyak pohon di gurun.'
    >>> pat(5, name='noun_desc').root(comps(noun_desc=True)),
    """

```python
pat(5, name='noun_desc').root(comps(noun_desc=True)),
```

## 4. PredictsInspector
    """
    # 先用指定的方式解析成分, 根据解析的数据来编写predicts
    # $ nluc en 'Giving alms is a good deed.' aux
    # $ se 'Giving alms is a good deed.'
    >>> pat(5, name='desc_subj_good').verb(predict_aux(
            ud.__cat('be') >> [ud.csubj('give'), ud.amod_cat('good')])),
        
    # $ se 'what will be the weather in three days?'
    >>> pat(5, name='query_weather').root(predict_aux(
            ud.__text('will') >> [ud.nsubj('what'), ud.dc_cat('weather')])),            
    """

```python
pat(5, name='desc_subj_good').verb(predict_aux(
            ud.__cat('be') >> [ud.csubj('give'), ud.amod_cat('good')])),
pat(5, name='query_weather').root(predict_aux(
            ud.__text('will') >> [ud.nsubj('what'), ud.dc_cat('weather')])),                  
```

## 5. PathInspector
    """
    >>> pat(5, name='behave_media').verb(pred_any_path('xcomp/obj','sound/perception', 'n')),
    >>> pat(5, name='pred_people').root(interr_root('who'),
            any_path('acl/amod', 'first', 'a'),
            any_path('acl/nmod', 'organization', 'n'),
            acl=kindof('people', 'n')),
    """

```python
pat(5, name='behave_media').verb(pred_any_path('xcomp/obj','sound/perception', 'n')),
pat(5, name='pred_people').root(interr_root('who'),
            any_path('acl/amod', 'first', 'a'),
            any_path('acl/nmod', 'organization', 'n'),
            acl=kindof('people', 'n')),
```

## 6. RasaInspector
    """
    >>> from sagas.nlu.rules_header import *
    >>> # $ sd 'Shenzhen ist das Silicon Valley für Hardware-Firmen'
    >>> Patterns(domains, meta, 5).entire(intentof('tech', 0.6, True)),
    >>> # $ sd 'Die Nutzung der Seite ist kostenlos.'
    >>> Patterns(domains, meta, 5).aux('adj', nsubj=intentof('using', 0.6, False), cop='c_aux'),
    """

```python
intentof('tech', 0.6, True),
nsubj=intentof('using', 0.6, False),
```

## 7. TagsInspector
    """
    Instances: tags('age?')
    """

```python
tags('age?')
```

## 8. SeriesInspector
    """
    Instances:
        series('events',
                action='specs_of:category',
                object='kind_of:category',
                _count='ins_date:$[0].value.value'),
    Testcases: $ sj '流しを8つ直した。'
    """

```python
series('events',
        action='specs_of:category',
        object='kind_of:category',
        _count='ins_date:$[0].value.value'),
```

## 9. SlotsInspector    
    """
    Instances:
        slots('transport', fn='from_to,transport'),
        slots('transport', fn='from_to,transport', driver='cache+tracker'),
    Testcases: $ sj '新幹線で東京から大阪まで行きました。'
    Notes: 如果使用tracker作为driver, 需要先将相应的slots名称添加到rasa-domain中
    """

```python
slots('transport', fn='from_to,transport'),
slots('transport', fn='from_to,transport', driver='cache+tracker'),
```

## 10. PredicateWordInspector
    """
    Instances:
        nsubj=kindof('plan', '*', extract=extract_noun_chunk)

    # $ se 'That spider flies.'
    # $ sid 'Burung dan kupu-kupu terbang.'
    # $ sid 'Laba-laba tersebut terbang.'  (这个句子使用的是单词原型'Laba-laba', 而不是词干lemma)
    >>> Patterns(domains, meta, 5, name='describe_animal_behave')
            .verb(behaveof('travel', 'v'), nsubj=kindof('animal', 'n')),
    # $ sid 'Burung itu suka makan serangga.' (zh="鸟喜欢吃虫子。")
    >>> Patterns(domains, meta, 5, name='describe_animal_hobby')
            .verb(behaveof('like', 'v'), nsubj=kindof('animal', 'n')),
    """

```python
nsubj=kindof('animal', 'n'),
amod=kindof('ill', 'a'),
nsubj=kindof('plan', '*', extract=extract_noun_chunk),
```

## 11. VerbInspector
    """
    # $ ses '¿Te duelen las piernas?' (zh="你的腿受伤了吗？")
    >>> Patterns(domains, meta, 5).verb(behaveof('suffer', 'v'), nsubj=kindof('body_part', 'n')),
    # $ sz "吸烟对你的健康有害。"
    >>> Patterns(domains, meta, 5).verb(behaveof('consume', 'v'), cmp='c_adp'),
    # $ se 'Do it correctly.'
    >>> Patterns(domains, meta, 5, name='command_do').verb(behaveof('make', 'v'), advmod='c_adv'),
    """

```python
behaveof('travel', 'v'), 
behaveof('weather/phenomenon', 'n'),
behaveof('need', '*', extract=extract_verb),
```

## 12. WordSpecsInspector            
    """
    Instances: specsof('*', 'little', 'large')
    $ sj '太陽は月に比べて大きいです。'
    """

```python
specsof('*', 'little', 'large'),
obj=specsof('n', 'beverage', 'water', 'juice', 'cafe'),
specsof('v', 'represent', 'show'),
```

## 13. DateInspector
    """
    Instances: obj=dateins('number')
    Testcases:
        $ ses 'Nosotros comíamos con la familia para Navidad.'

    # $ se "what will be the weather in three days ?"
    >>> Patterns(domains, meta, 5).cop(behaveof('weather/phenomenon', 'n'),
         nsubj=agency, cop='c_aux',
         nmod=dateins({'snips/date', 'snips/datetime'},
         provider='snips')),
    """

```python
obj=dateins('number')
nmod=dateins({'snips/date', 'snips/datetime'},
         provider='snips')
```

## 14. NegativeWordInspector
    """
    # Passive-Voice: Sie werden nicht berücksichtigt.
          Patterns(domains, meta, 1).verb(nsubj_pass=agency, aux_pass='c_aux'),
          Patterns(domains, meta, 2).verb(nsubj_pass=agency, aux_pass='c_aux', advmod=negative()),
    """

```python
advmod=negative()
```

## 15. InterrogativePronounInspector
    """
    # $ sid 'Apa yang lebih murah?'
            pat(1).subj('adj', nsubj=agency, head_amod=interr('what')),
    # $ sid 'Siapa orang terpenting di kantormu?'
            pat(5, name='pred_people').root(interr_root('who'),
                    any_path('acl/amod', 'first', 'a'),
                    any_path('acl/nmod', 'organization', 'n'),
                    acl=kindof('people', 'n')),
    """

```python
interr_root('who'),
head_amod=interr('what'),
```

## 16. MatchInspector
    """
    # $ sid 'Apa tujuan mereka?' (ja="彼らの目的は何ですか？")
    >>> pat(5).verb(matchins('apa'), acl=agency),
    # $ sid 'Bau apa itu?' (en="What's that smell?", zh="那是什么味道？")
    >>> pat(5).verb(behaveof('perception', 'n'), acl=matchins('apa')),
    # $ sid 'Bagaimana tenggorokanmu?' (zh="喉咙怎么样？")
    >>> pat(5).verb(behaveof('body_part', 'n'), amod=matchins({'bagaimana'}, 'in')),
    # $ sid "Mengapa lehermu sakit?" (Why does your neck hurt?)
    >>> pat(5).verb(behaveof('body_part', 'n'), advmod=matchins({'mengapa'}, 'in'), amod=kindof('ill', 'a')),
    """

```python
acl=matchins('apa'),
amod=matchins({'bagaimana'}, 'in'),
advmod=matchins({'mengapa'}, 'in'),
```

## 17. CustInspector
    """
    Examples:
        # $ python -m sagas.ko.ko_helper nouns '피자와 스파게티가'
        # $ sko '우리는 피자와 스파게티가 필요해요.'  (We need pizza and spaghetti.)
        # $ sko '우리는 생선과 스테이크가 필요해요.'  (We need fish and steaks.)
        pat(-5, name='desc_need').verb(
            behaveof('need', '*', extract=extract_verb),
            checker(has_rel='nsubj'),
            nsubj=cust(extract_nouns),),

        # $ sko '이번 주말에 벌써 계획이 있어요?'
        #   (Do you already have plans for this weekend?)
        #   (ibeon jumal-e beolsseo gyehoeg-i iss-eoyo?)
        pat(-5, name='desc_plan').verb(
            interr_root('have'),
            checker(has_rel='obl'),
            obl=cust(extract_datetime),
            nsubj=kindof('plan', '*', extract=extract_noun_chunk), ),
    """

```python
nsubj=cust(extract_nouns),
obl=cust(extract_datetime),
```

## 18. EntityInspector
    """
    >>> from sagas.nlu.inspectors import EntityInspector as entins
    >>> # 匹配实体: I was born in Beijing.
    >>> Patterns(domains, meta, 2).verb(nsubj_pass=agency, obl=entins('GPE')),
    >>> # $ sr 'Я работаю в китае.'
    >>> Patterns(domains, meta, 5).verb(nsubj=agency, obl=entins('location')),
    """

```python
obl=entins('GPE'),
obl=entins('location'),
```

## 19. Functors
```python
# $ sid 'Bola Dimas putih.'  ("白色迪马斯球。")
pat(5, 'describe_color').root(behaveof('object', 'n'),
        anal(amod=predicate_fn('color', 'n'))),
# $ sid 'Karpet di kantor saya abu-abu.' (en="The carpet in my office is gray.")
pat(5, 'describe_object_chunk').root(behaveof('object', 'n'),
        anal(amod=predicate_fn('entity', 'n'))),

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
```





