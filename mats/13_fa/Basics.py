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
    .sent(en="the sun is yellow",
          fr="le soleil est jaune",
          zh="太阳是黄色的",
          fa="خورشید زرد است",
          t0="jorshid zrd ast",
          ) \
    .sent(en="snow is white",
          fr="La neige est blanche",
          zh="雪是白色的",
          fa="برف سفید است",
          t0="brf sfid ast",
          ) \
    .sent(en="the sun shines in summer",
          fr="le soleil brille en été",
          zh="阳光普照在夏天",
          fa="خورشید تابستان می درخشد",
          t0="jorshid tabstan mi drkhshd",
          ) \
    .sent(en="the winter is cold",
          fr="l'hiver est froid",
          zh="冬天很冷",
          fa="زمستان سرد است",
          t0="zmstan srd ast",
          ) \
    .sent(en="what is the weather like today",
          fr="quel temps fait-il aujourd'hui",
          zh="今天天气如何",
          fa="امروز هوا چطور است",
          t0="amroz hoa chtor ast",
          ) \
    .sent(en="what time is it",
          fr="quelle heure est-il",
          zh="现在是几奌",
          fa="ساعت چند است",
          t0="saat chnd ast",
          ) \





    