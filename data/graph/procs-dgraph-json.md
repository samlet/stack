# procs-dgraph-json.md
+ procs-dgraph-json

```python
client=reset('''
    name: string @index(exact, term) .
    rated: uid @reverse @count .
    title: string @lang .
''')

# 查询边缘上的所有方面@facets
response = client.txn().query('''{
  data(func: eq(name, "Alice")) {
     name
     mobile @facets
     car @facets
  }
}''')
print_rs(response)

run_q('''{
  data(func: eq(name, "Alice")) {
    name
    friend @facets {
      name
      car @facets
      title@ru
    }
  }
}
''')
```

## cli
```sh
using rasa_1x
$ bash ./data/graph/gen_samples.sh
$ bash ./data/graph/gen_samples_it_pt.sh

# or
$ python -m sagas.graph.graph_manager create_lang_feeds
$ python -m sagas.graph.graph_manager create_lang_feeds ja /pi/ai/seq2seq/jpn-eng-2019/jpn.txt ./data/graph/jpn_eng_feed.json
$ python -m sagas.graph.graph_manager create_lang_feeds zh /pi/ai/seq2seq/cmn-eng-2019/cmn.txt ./data/graph/cmn_eng_feed.json True
$ python -m sagas.graph.graph_manager create_lang_feeds de /pi/ai/seq2seq/deu-eng/deu.txt ./data/graph/deu_eng_feed.json
$ python -m sagas.graph.graph_manager create_lang_feeds es /pi/ai/seq2seq/spa-eng/spa.txt ./data/graph/spa_eng_feed.json
```
