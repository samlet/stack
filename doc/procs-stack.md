# procs-stack.md
## latest
```sh
$ cdd /pi/agent_dispatcher  # sagas-ai/bots/agent_dispatcher
$ . env.sh
$ s1
$ s2
```

## old ..
* procs-cabocha-provider.ipynb
    - 使用grpc封装cabocha作为provider, 提供给前端的nlu组件.
* procs-nlu-cn-pipelines.ipynb
    - 测试中文nlu组件.

## servants
```sh
# $ start bus  # rabbit, 可以直接用brew-service代替

# $ foreman start -f Procfile_nlp  # on linux server
    # $ start bert-multi
    # $ start stanford-corenlp-server

$ foreman start -f Procfile_langs  # (s2) 代替以下服务启动
    $ start servant_nlu    # spacy-entities (spacy-2.1+)
    $ start servant_spacy  # spacy-2.1, spacy-ru
    $ start langprocs
    $ start timenlp

$ honcho start  # (s1) 代替以下服务启动
    $ start duckling
    $ start servant_de     # corenlp/ltp
    # $ start servant_zh
    $ start servant_words
    $ start servant_multilang
    $ start odoo

    # servant from dir: ./mats/nlu_multilang
    # $ start nlu

# 如果使用faiss, 需要启动bert
$ start bert-en

# nlu (rasa-1.x), located: /pi/ws/sagas-ai
$ honcho start
    $ start agent_servant
    $ start genesis_actions
```

## ofbiz
```sh
# $ start bus  # rabbit, 可以直接用brew-service代替
$ start ofbiz
```

## odoo routines
```sh
# odoo local server
$ start odoo
# 默认用户&密码是: admin&admin
$ open http://localhost:8069
```

+ docker-compose

```sh
./run-odoo.sh
start odoo_c
open http://localhost:8888/notebooks/procs-odoorpc.ipynb
```

## ja routines
```sh
$ start ja_backend
$ start ja_nlu_t
$ open http://localhost:8888/notebooks/procs-nlu-ja-pipelines.ipynb
```

## translator cacher(mongo)
⊕ [mongoexport — MongoDB Manual](https://docs.mongodb.com/manual/reference/program/mongoexport/)
⊕ [mongoimport — MongoDB Manual](https://docs.mongodb.com/manual/reference/program/mongoimport/#simple-import)

```sh
# backup
mongoexport --collection=trans --db=langs --out=./out/trans.json
# import
mongoimport --db=langs --collection=trans --file=./out/trans.json
```

## routines
```sh
## stack: rules - actions
$ python -m sagas.nlu.ruleset_procs verbs 'I want to play video.' en
$ verbs 'I want to play music.' en True
```




