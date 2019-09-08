from sagas.nlu.mats import Cats, Mats

default = Cats('default')

Mats(cat=default) \
    .sent(en="this is my mother",
          fr="c'est ma mère",
          zh="这是我的母亲",
          pt="essa é minha mãe",
          t0="",
          ) \



    