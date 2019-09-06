from sagas.nlu.mats import Cats, Mats

default = Cats('default')

Mats(cat=default) \
    .sent(en="i have a dog",
          fr="j'ai un chien",
          zh="我养了一条狗",
          he="יש לי כלב",
          t0="ish li chlb",
          ) \

    