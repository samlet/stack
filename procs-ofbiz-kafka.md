# procs-ofbiz-kafka.md
## start
```python
from sagas.ofbiz.entities import OfEntity as e, oc, finder, MetaEntity
hub=oc.component('entity_event_hub')
# hub.setTrackOn(True)
# 打开所有实体更新事件: measure.entities
hub.setMeasureUpdaterOn(True)

hub.registerSubscriber('ProductType', 'store', 'run', 'kafka')
e().storeProductType(productTypeId="Test_type_2")
```

```sh
$ . ~/kafka-env.sh 
$ list-topic 
AccessLog
Test.create.return
event.ProductType
measure.entities
...

$ listen-all event.ProductType
{"_event":"run","productTypeId":"Test_type_2","_operation":"store"}

# 持续接收事件
$ listen-topic event.ProductType
{"_event":"run","productTypeId":"Test_type_3","_operation":"store"}
{"_event":"run","productTypeId":"Test_type_3","_operation":"store"}
{"_event":"run","productTypeId":"Test_type_2","_operation":"store"}

# 实体更新事件
$ listen-topic measure.entities
```

