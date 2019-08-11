# procs-ofbiz-product.md
+ applications/product/minilang/product/test/ProductTest.xml

## services
```python
ms=OfService()
ok, result=ms.createProduct(userLogin=finder.user, 
               internalName='Test_product',
               productTypeId='GOOD')
print(ok, result)

##
product_id=result['productId']
ok, result=ms.updateProduct(productId=product_id, 
                            productName='Test_name_B',
                            description='Updated description')
print(ok, result)

## 
product_id="10013"
entity=MetaEntity("Product")
rec=entity.find_one(productId=product_id)
print(rec['description'])

## show service model
MetaService('getInventoryAvailableByFacility').desc(False)
```

## entities
```python
entity=MetaEntity("Product")
print(entity.primary)
rec=entity.find_one(productId='10005')
print(rec['internalName'])
recs=entity.find_list(5, 0)
print(len(recs))
for r in recs:
    print(r['internalName'])

## use OfEntity
OfEntity().createProductType(productTypeId="Test_type_2")
OfEntity().storeProductType(productTypeId="Test_type_2")
OfEntity().getProductType(productTypeId="Test_type_2")
OfEntity().removeProductType(productTypeId="Test_type_2")
OfEntity().queryProductType(productTypeId="Test_type_2")
for p in OfEntity().listProductType():
    print(p['productTypeId'])
for p in OfEntity().allProductType():
    print(p['productTypeId'])        
```

## data
```python
import os
print(os.getcwd())
# /Users/xiaofeiwu/jcloud/assets/langs/workspace/rasa/stack

data_folder=os.getcwd()+"/data/product"
OfService().entityImportDir(path=data_folder)

# search a seed data
MetaEntity('ProductStore').record('Test_store')
```

