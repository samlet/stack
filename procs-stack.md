# procs-stack.md
* procs-cabocha-provider.ipynb
    - 使用grpc封装cabocha作为provider, 提供给前端的nlu组件.
* procs-nlu-cn-pipelines.ipynb
    - 测试中文nlu组件.

## servants
```sh
$ start bert-multi
$ start bus  # rabbit

$ foreman start -f Procfile_langs  # 代替以下服务启动
    $ start servant_nlu    # spacy-entities (spacy-2.1+)
    $ start servant_spacy  # spacy-2.1, spacy-ru
    $ start langprocs
    $ start timenlp

$ honcho start  # 代替以下服务启动
    $ start duckling
    $ start servant_de     # corenlp/ltp
    # $ start servant_zh
    $ start servant_words
    $ start servant_multilang

    # servant from dir: ./mats/nlu_multilang
    $ start nlu
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

