# procs.md
⊕ [Language Support](https://rasa.com/docs/nlu/0.13.8/languages/)
⊕ [服务器配置](https://rasa.com/docs/nlu/0.13.8/config/#section-configuration)
⊕ [Choosing a Rasa NLU Pipeline](https://rasa.com/docs/nlu/0.13.8/choosing_pipeline/#choosing-pipeline)

## start
```sh
# create configure files: config.yml, nlu_data/nlu_data.md

# train
./train.sh
# start nlu server
./nlu-server.sh
# execute a intent query
./query.sh 
# or via curl
curl -XPOST localhost:5000/parse -d '{"q":"Lenge siden sist", "project":"norwegian"}'
```

