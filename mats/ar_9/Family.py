from sagas.nlu.mats import Cats, Mats

default = Cats('default')

sents=[
    ('أُسْتاذي سام جَوْعان.', 'My professor Sam is hungry.'),
    ('جاري جورْج مُحاسِب.', ''),
    ('زَوْجي وَأَبي', ''),
]

Mats(cat=default) \
    .sent(ar="بِنْتي مُحاسِبة مُمْتازة.",
          en="My daughter is an excellent accountant.",
          zh="我的女儿是一位优秀的会计师。",
          ja="私の娘は優秀な会計士です。",
          v0="Watashi no musume wa yūshūna kaikeishidesu.",
          v1="binty muhasibt mumtaz.",
          ) \
    .sent(ar="زَوْجي جَوْعان وَتَعْبان.",
          en="My husband is hungry and tired.",
          zh="我丈夫饿了又累了。",
          ja="夫は空腹で疲れています。",
          v0="Otto wa kūfuku de tsukarete imasu.",
          ) \











