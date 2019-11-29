# procs-dgraph-ofbiz-labels.md
## start
■ ofbiz-multilang-labels的dgraph支持:
    + procs-dgraph-ofbiz-labels.ipynb
    $ python -m sagas.ofbiz.resources label_json 'CommonStatus'
    $ python -m sagas.ofbiz.resources create_resources_data
        + stack/data/labels/labels.json


```ini
key: string @index(exact) .
value: string @index(fulltext) @lang .
```

