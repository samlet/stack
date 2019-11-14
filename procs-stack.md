# procs-stack.md
* procs-cabocha-provider.ipynb
    - 使用grpc封装cabocha作为provider, 提供给前端的nlu组件.
* procs-nlu-cn-pipelines.ipynb
    - 测试中文nlu组件.

## servants
```sh
$ start bus  # rabbit

$ foreman start -f Procfile_nlp  # on linux server
    $ start bert-multi
    # start stanford-corenlp-server

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

    # servant from dir: ./mats/nlu_multilang
    $ start nlu
```

## ofbiz
```sh
$ start bus  # rabbit
$ start ofbiz
```

## odoo routines
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



