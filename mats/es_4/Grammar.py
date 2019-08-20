from sagas.nlu.mats import Cats, Mats

default = Cats('default')

Mats(cat=default) \
    .sent(es="Ésta es mi hija.",
          en="This is my daughter.",
          zh="这是我的女儿。",
          ja="これは私の娘です。",
          v0="Kore wa watashi no musumedesu.",
          ) \
    .sent(es="Él tiene muchos libros de historia.",
          en="He has many history books.",
          zh="他有很多历史书。",
          ja="彼には多くの歴史の本があります。",
          v0="Kare ni wa ōku no rekishi no hon ga arimasu.",
          ) \
    .sent(es="Hoy hace mucho calor.",
          en="Today it's very hot.",
          zh="今天很热。",
          ja="今日はとても暑いです。",
          v0="Kyō wa totemo atsuidesu.",
          ) \
    .sent(es="¿Es éste tu libro?",
          en="Is this your book?",
          zh="这是你的书吗？",
          ja="これはあなたの本ですか？",
          v0="Kore wa anata no hondesu ka?",
          ) \
    .sent(es="Hay muchos libros en ese cuarto.",
          en="There are many books in that room.",
          zh="那个房间里有很多书。",
          ja="その部屋にはたくさんの本があります。",
          v0="Sono heya ni wa takusan no hon ga arimasu.",
          ) \









