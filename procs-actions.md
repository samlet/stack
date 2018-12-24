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


