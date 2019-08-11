# procs-artifacts.md
1. login-name目录下是均以'type:id'形式存在的artifact, 包括blueprint在内, 这样就方便了交叉引用, 也方便更改存储介质;
2. 初始化的模板数据放在stack/assets目录下, 为了测试方便, 每次启动时都删除掉artifact目录, 重新复制asset数据. (使用一个开关)

3. 管理artifacts的代码用python来写, 使用grpc封装, 然后经由blueprint-actor与前端的bloc交互, bloc不直接访问artifacts的grpc接口(要支持hybrid架构, 以及安全性上的考虑);

## start
```sh
## nlp services  (chinese_hanlp dir)
$ run
## nlu  (chinese_hanlp dir)
$ ./nlu-server.sh 

## grpc  (stack dir)
$ start as
# or: python -m sagas.ofbiz.rpc_artifacts
```


