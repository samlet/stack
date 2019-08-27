# procs-stack.md
* procs-cabocha-provider.ipynb
    - 使用grpc封装cabocha作为provider, 提供给前端的nlu组件.
* procs-nlu-cn-pipelines.ipynb
    - 测试中文nlu组件.

## servants
```sh
$ start duckling
$ start bert-multi
$ start bus  # rabbit

$ start servant_nlu
$ start servant_de     # corenlp/ltp
$ start servant_spacy  # spacy-2.1, spacy-ru
# $ start servant_zh
$ start servant_words
$ start servant_multilang

# servant from dir: ./mats/nlu_multilang
$ start nlu

$ start langprocs
$ start timenlp
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

