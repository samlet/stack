from sagas.nlu.mats import Cats, Mats

default = Cats('default')

Mats(cat=default) \
    .sent(ar="لقد حاولت وسعك.",
          en="I've tried your power.",
          zh="我已经尝试过你的力量了。",
          ja="あなたの力を試しました。",
          v0="Anata no chikara o tameshimashita.",
          v1="laqad hawalat wasaeik.",
          ) \
    .sent(ar="أشتاق إليه.",
          en="I miss him.",
          zh="我想念他。",
          ja="彼が恋しい",
          v0="Kare ga koishī",
          v1="'ashtaq 'iilayh.",
          ) \




