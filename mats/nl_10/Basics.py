from sagas.nlu.mats import Cats, Mats

default = Cats('default')

Mats(cat=default) \
    .sent(nl="Hoeveel brood eet jij?",
          en="How much bread do you eat?",
          ja="あなたはどれくらいのパンを食べますか？",
          de="Wie viel Brot isst du?",
          ) \


