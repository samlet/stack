# procs-ofbiz-product-price.md
## services
```python
product=MetaEntity("Product").record("GZ-2002")
ok, ret=OfService().calculateProductPrice(product=product)
print(ret['defaultPrice'], ret['listPrice'])
```

## entities
```python
MetaEntity('ProductPrice').desc(False)
```
