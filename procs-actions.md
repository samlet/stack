# procs-actions.md
```sh
$ run action_server
$ jupyter notebook
$ open http://localhost:8890/notebooks/procs-actions.ipynb

# or
$ using bigdata
$ python action_testor.py
```

## form actions
```sh
$ run action_server
$ ./form_testor.py
# load trained model
$ ./agent_testor.py
```

+ issue: 如果用agent.load直接加载训练好的模型, 则在handle_text时不会访问actions服务.
    要正确的配置endpoint: action_endpoint=endpoints.action


## add a action
1. nlu intent
2. domain.xml: actions
3. stories.md
4. actions.py

5. train & start nlu
6. train & start core

## test a action
```sh
## nlp services  (chinese_hanlp dir)
$ run
## nlu  (chinese_hanlp dir)
$ ./nlu-server.sh 

## execute a action, don't require to run actions server  (stack dir)
$ python -m sagas.bots.action_runner execute action_about_date '找音乐会'
```

