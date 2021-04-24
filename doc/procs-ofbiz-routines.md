# procs-ofbiz-model.md
## create ipython profile
⊕ [Introduction to IPython configuration — IPython 7.22.0 documentation](https://ipython.readthedocs.io/en/stable/config/intro.html)

```bash
ipython profile create bluecc   # create the profile bluecc
ipython locate profile bluecc
# 在这个目录下startup子目录下创建00-first.py:
# from sagas.modules.deles import *

ipython --profile=bluecc        # start IPython using the new profile
In [3]: invoices.getInvoiceTotal("demo10001")
Out[3]: Decimal('36.43')
```
```python
In [1]: e('relations').Person
```

## quick start
```python
from sagas.modules.deles import *
total=invoices.getInvoiceTotal('demo10000')
print(f"total {total}")
```

```python
# ❶
from sagas.ofbiz.services import OfService as s, oc, track
from sagas.ofbiz.entities import OfEntity as e
ok, r=track(lambda a: s().testScv(defaultValue=5.5, message="hello world"))
print(ok, r)    

# ❷
from sagas.ofbiz.services import OfService as s, oc, track
from sagas.ofbiz.entities import OfEntity as e
ok, r=await s('srv').testScv(defaultValue=6.6, message="hello world")
print(ok,r)

# ❸
import sagas.ofbiz.entities as ee
ent=ee.entity('Product')
val=ent.record('GZ-2002')
print(ent.to_json(val,True))
```

## imports
```python
from sagas.ofbiz.services import OfService as s
from sagas.ofbiz.entities import OfEntity as e, oc, finder, MetaEntity
import sagas.ofbiz.entities as ee

from py4j.java_gateway import get_field

## import packages
oc.import_package('com.sagas.generic.*')
# hub=oc.j.EntityEventHub.getEntityEventHub(oc.delegator)

# data types
oc.import_package('java.math.BigDecimal')
productRating=oc.j.BigDecimal(5)
fromDate=oc.j.Timestamp.valueOf('2013-07-04 00:00:00')
```

## services
```python
from sagas.ofbiz.services import OfService as s
from sagas.ofbiz.entities import OfEntity as e
import sagas.ofbiz.entities as ee

ok, result=s().calculateProductPrice(product=e().refProduct('GZ-2002'))
ee.format(result)

# show the service meta as a dataframe
s('meta').calculateProductPrice
s('meta', False).createBillingAccount # don't show internal parameter

# service definition
from sagas.ofbiz.util import print_table
model=s('model').createProductReview
print_table(model, 'engineName', 'location', 'invoke', 'defaultEntityName')

## testing service
s().testScv(defaultValue=5.5, message="hello world")  # with kwargs
s().testScv({'defaultValue':5.5, 'message':"hello world"})  # with dict
# Out[2]: (True, {'responseMessage': 'success', 'resp': 'service done'})

## service logs
from sagas.ofbiz.entities import OfEntity as e, oc
oc.import_package('org.apache.ofbiz.service.ServiceDispatcher')
log=oc.j.ServiceDispatcher.getServiceLogMap()
for rs,value in log.items():
    print(oc.get(rs.getModelService(), 'name'), rs.getLocalName(), rs.getMode(), rs.getStartStamp(), rs.getEndStamp())

## track service run
from sagas.ofbiz.services import OfService as s, oc, track
ok, r=track(lambda a: s().testScv(defaultValue=5.5, message="hello world"))
print(ok, r)    

## search service
from sagas.ofbiz.services import OfService as s, search_service
search_service('billingAccount')

## hybrid mode
from sagas.ofbiz.services import OfService as s, oc, track
ok, r=await s('srv').testScv(defaultValue='x', message="hello world")
print(ok,r)

## date-time
from sagas.ofbiz.date_time import DateTime
ok,r=s().createPerson(firstName='Kid', 
                      lastName='Person',
                      birthDate=DateTime.date('2010-12-10'))                      
## specific user-login
admin=e().refUserLogin('TestManufAdmin')
ok,r=s().createProductionRun(userLogin=admin,...)
```

## entities
```python
from sagas.ofbiz.entities import OfEntity as e
e('meta').Person
e('relations').Person

import sagas.ofbiz.entities as ee
product=e().refProduct('GZ-2002')

import sagas.ofbiz.entities as ee
from sagas.ofbiz.entities import OfEntity as e
rec=e().refProductReview('Test_review')
ee.format(rec)

from sagas.ofbiz.entities import oc,finder,OfEntity

OfEntity().createProductType(productTypeId="Test_type_2")
OfEntity().storeProductType(productTypeId="Test_type_2")
OfEntity().getProductType(productTypeId="Test_type_2")
OfEntity().removeProductType(productTypeId="Test_type_2")
OfEntity().queryProductType(productTypeId="Test_type_2")

for p in OfEntity().listProductType():
    print(p['productTypeId'])
for p in OfEntity().allProductType():
    print(p['productTypeId'])

from sagas.ofbiz.entities import OfEntity as e, oc, format
format(e().getProductPrice(productId="Test_product_A",
                   productPriceTypeId='AVERAGE_COST',
                   productPricePurposeId='COMPONENT_PRICE',
                   productStoreGroupId='Test_group',
                   currencyUomId='USD',
                   fromDate=oc.j.Timestamp.valueOf('2013-07-04 00:00:00')))

## 使用dataframe显示记录集, query*/list*/all*均支持
rs=e('df').queryCostComponent(productId='PROD_MANUF')
rs

## search entity model
from sagas.ofbiz.entities import search_entity
search_entity('order')    

## turn on meausre
# on cli: start eecas
hub=oc.component('entity_event_hub')
hub.setMeasureUpdaterOn(True)
e().storeProductType(productTypeId="Test_type_2")

## jsonify
product=e('json').refProduct('GZ-2002')
json.loads(product)
products=e('json').listProduct(_limit=2)
json.loads(products)

```

## components
```python
from sagas.ofbiz.entities import OfEntity as e, oc, finder
hub=oc.component('entity_event_hub')
forms=oc.component('form_mgr')

## forms
form=forms.getMetaForm("component://content/widget/forum/BlogForms.xml;EditBlog;en_US")
print(form)
```

## eca
* 通过eecas/secas, 可以跟踪到所有的实体和服务事件, 可以挂接一个实现了EntityEcaHandler的代理类, 以便将指定的实体/服务事件通过kafka发送到外部的监听器, 做日志和统计分析, 因为发送是异步的, 不会影响正常的业务过程.
+ log from: DelegatorEcaHandler
    * e().storeProductType(productTypeId="Test_type_2")

```ini
|I| Handler.evalRules for entity UserLogin, operation find, event cache-check, no eventMap for this entity
|I| Handler.evalRules for entity UserLogin, operation find, event validate, no eventMap for this entity
|I| Handler.evalRules for entity UserLogin, operation find, event run, no eventMap for this entity
|I| Handler.evalRules for entity UserLogin, operation find, event return, no eventMap for this entity
|I| Handler.evalRules for entity UserLogin, operation find, event cache-put, no eventMap for this entity

|I| Handler.evalRules for entity ProductType, operation find, event validate, no eventMap for this entity
|I| Handler.evalRules for entity ProductType, operation find, event run, no eventMap for this entity
|I| Handler.evalRules for entity ProductType, operation find, event return, no eventMap for this entity

|I| Handler.evalRules for entity ProductType, operation store, event validate, no eventMap for this entity
|I| Handler.evalRules for entity ProductType, operation store, event run, no eventMap for this entity
|I| Handler.evalRules for entity ProductType, operation store, event cache-clear, no eventMap for this entity
|I| Handler.evalRules for entity ProductType, operation store, event return, no eventMap for this entity
```

## json
```python
import json
jsonstr=oc.j.ValueHelper.entityToJson(e().refProduct('GZ-2002'), oc.jmap())
json.loads(jsonstr)

result = finder.find_list(entity, limit, offset)
result = oc.j.ValueHelper.valueListToJson(result)
```

## data sources
```sh
$ python -m sagas.ofbiz.tools import_dir ./data/product/
$ python -m sagas.ofbiz.tools import_dir ./data/party/
```

## cli
```sh
python -m sagas.ofbiz.tools ping
python -m sagas.ofbiz.tools users
```

## entity maintainer
```sh
. env.sh
$ tool entity_model DssOrdinalSales
$ tool remove_model DssOrdinalSales

# python -m sagas.ofbiz.gen_tool gen-model-cls
gen_model
# python -m sagas.ofbiz.gen_tool gen-dss-model
gen_dss

# generate data and import to database
$ python -m sagas.ofbiz.gen_data
$ tool import_dir ./data/dss/
$ tool entity_data DssOrdinalSales

# display entity list within the special package
$ tool entity_package com.sagas.dss
# generate dart entity class
$ gen_pkg com.sagas.dss /Users/xiaofeiwu/jcloud/assets/langs/workspace/flutter/sagas_meta/lib/src/models
$ gen_json com.sagas.dss /Users/xiaofeiwu/jcloud/assets/langs/workspace/flutter/sagas_meta/lib/src/jsonifiers

## persist prefabs
$ python -m sagas.ofbiz.entity_prefabs persist_component ofbizDemo
$ python -m sagas.ofbiz.entity_prefabs persist_all
```

## pandas
```python
df=e('df').allPartyRoleDetailAndPartyDetail()
df.info()

# ⊕ [删除DataFrame中值全为NaN或者包含有NaN的列或行 - calorand的博客 - CSDN博客](https://blog.csdn.net/calorand/article/details/53742290)
df=df.dropna(axis=1,how='all') 
# 删除表中全部为NaN的行
df.dropna(axis=0,how='all')  
# 删除表中含有任何NaN的行
df.dropna(axis=0,how='any') #drop all rows that have any NaN values
# 删除表中含有任何NaN的列
df.dropna(axis=1,how='any') #drop all rows that have any NaN values
```

## resources
```sh
$ python -m sagas.ofbiz.resources build_all 'Sagas应用程序'
$ python -m sagas.ofbiz.resources lookup 'Sagas应用程序'
$ lookup '美国'
$ lookup Product en
$ lookup Color en
$ lookup Couleur fr
$ lookup CommonStatus key

$ python -m sagas.ofbiz.resources stats

$ python -m sagas.ofbiz.resource_indexer index_all
$ python -m sagas.ofbiz.resource_indexer search 产品价格

## forms
$ tool form_list
## form resource build
$ python -m sagas.ofbiz.resource_mappings build
$ python -m sagas.ofbiz.resource_mappings query 'PartyLastName'
```


