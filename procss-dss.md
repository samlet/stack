# procss-dss.md
## start
```dart
class LinearSales {
  final int year;
  final int sales;
```

```sh
. env.sh
$ gen_dss
# 'python -m sagas.ofbiz.gen_tool gen-dss-model'
# 复制到entitymodel_dss.xml文件中, 重启ofbiz(start br)

# 检查模型:
$ tool entity_model DssLinearSales
```

