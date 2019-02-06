## use builder
```bash
$ python -m sagas.ofbiz.builder gen-model > sagas/ofbiz/schema_testing_g.py
```

## testing
```bash
$ python -m sagas.ofbiz.schema_testing
```

## api
```bash
python movies_api.py
```

+ use insomnia: http://127.0.0.1:5000/graphql

```graphql
{
  movies (limit:3, offset:2) {
    title
    saMovieGenresAppl{
        movieGenresId
    }
  }
}
```

## steps
+ 如果变更了数据模型中的字段定义:
    1. 使用脚本删除和重建这个表, 需要先删除有外键引用到该表的表. 重建表只需要重启ofbiz即可.
    2. 使用xx_data_loader重新加载seed数据.
    3. 使用gen-schema-queries.sh重新生成schema.
