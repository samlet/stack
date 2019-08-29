from sagas.nlu.mats import Cats, Mats

default = Cats('default')

Mats(cat=default) \
    .sent(es="En mi patio tengo animales salvajes.",
          en="In my yard I have wild animals.",
          zh="在我的院子里，我有野生动物。",
          ja="私の庭には野生動物がいます。",
          v0="Watashi no niwa ni wa yasei dōbutsu ga imasu.",
          ) \



