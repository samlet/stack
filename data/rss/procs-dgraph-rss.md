# procs-dgraph-rss.md
+ stack/data/rss/urls.txt

## refs
⊕ [社交媒体 | RSSHub](https://docs.rsshub.app/social-media.html#bilibili)
    ⊕ [https://rsshub.app/bilibili/bangumi/media/9192](https://rsshub.app/bilibili/bangumi/media/9192)
⊕ [购物 | RSSHub](https://docs.rsshub.app/shopping.html#%E6%90%9C%E7%B4%A2%E7%BB%93%E6%9E%9C)
    ⊕ [https://rsshub.app/westore/new](https://rsshub.app/westore/new)

## start
```sh
$ (1) python -m sagas.graph.rss_hub proc_resources
# read: stack/data/rss/urls.txt
$ (2) python -m sagas.graph.rss_hub check_feeds True
$ (3) python -m sagas.graph.rss_hub load_resources
$ (4) python -m sagas.graph.rss_hub some_query
```

