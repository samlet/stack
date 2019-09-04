from sagas.nlu.mats import Cats, Mats

default = Cats('default')

Mats(cat=default) \
    .sent(en="we learn french",
          fr="nous apprenons le français",
          zh="我们学法语",
          fa="ما فرانسوی را یاد می گیریم",
          t0="ma fransoi ra iad mi girim",
          ) \
    .sent(en="this is my nephew",
          fr="C'est mon neveu",
          zh="这是我的侄子",
          fa="این خواهرزاده من است",
          t0="ain joahrzadh mn ast",
          ) \
    .sent(en="this is my uncle",
          fr="c'est mon oncle",
          zh="这是我的叔叔",
          fa="این عموی من است",
          t0="ain amoi mn ast",
          ) \
    .sent(en="the aunt",
          fr="la tante",
          zh="阿姨",
          fa="خاله",
          t0="khalh",
          ) \





    