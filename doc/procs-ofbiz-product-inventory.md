# procs-ofbiz-product-inventory.md
+ applications/product/minilang/product/test/InventoryTests.xml

## services
```python
## meta
MetaService('getInventoryAvailableByFacility').desc(False)

## invoke
OfService().createPhysicalInventoryAndVariance(inventoryItemId='9024',
                                              varianceReasonId='VAR_LOST')
# (True, {'responseMessage': 'success', 'physicalInventoryId': '10000'})
```

## entities
```python
MetaEntity("InventoryItem").record('9024')
```
