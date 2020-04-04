# procs-rasa-issues.md
1. 非内部的component, 名称只能是全路径, 否则无法在配置文件中对其进行配置:
    + workspace/rasa/stack/sagas/provider/time_extractor.py
        name = "sagas.provider.time_extractor.TimeExtractor"

## packages
⊕ [prompt-toolkit requirement conflict · Issue #370 · jupyter/jupyter](https://github.com/jupyter/jupyter/issues/370)

+ prompt_toolkit==1.0.14

```sh
# rasa-core-0.13.x依赖1.0.14版本
$ pip install prompt-toolkit==1.0.14
$ pip install ipykernel==4.8.0

# ⊕ [ipython · PyPI](https://pypi.org/project/ipython/#history)
# 只有6.2.1版本依赖1.0.14, 之后的版本依赖的是1.0.15
$ pip install ipython==6.2.1
```

+ snips-nlu==0.17.3
    * 依赖这个版本的.md格式解析.

## trainer
⊕ [unable to train with mixed datatype · Issue #1363 · RasaHQ/rasa_nlu](https://github.com/RasaHQ/rasa_nlu/issues/1363)

Ok... i found a solution
instead of

curl --request POST --header 'content-type: application/x-yml' @config_train_server_json.yml --url 'localhost:5000/train?project=test_model'

use this (--data-binary added to curl request)

```sh
curl --request POST --header 'content-type: application/x-yml' --data-binary @config_train_server_json.yml --url 'localhost:5000/train?project=test_model'
```

