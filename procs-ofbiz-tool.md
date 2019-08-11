# procs-ofbiz-tool.md
```sh
## entity
$ tool entity_model UserLogin
$ tool entity_data UserLogin
$ tool entity_ref ProductType Test_type_114
# +--------------------+-------------------------+
# | name               | value                   |
# |--------------------+-------------------------|
# | lastUpdatedStamp   | 2019-03-30 21:41:05.336 |
# | isPhysical         |                         |
# | parentTypeId       |                         |
# | isDigital          |                         |
# | hasTable           |                         |
# | createdTxStamp     | 2019-03-08 18:10:38.66  |
# | createdStamp       | 2019-03-08 18:10:38.664 |
# | description        | xxxttt                  |
# | lastUpdatedTxStamp | 2019-03-30 21:41:05.04  |
# | productTypeId      | Test_type_114           |
# +--------------------+-------------------------+

## form
$ tool product_forms
$ tool form_meta AddProductPaymentMethodType en_US

## 渲染表单数据
$ tool render AddProductPaymentMethodType
$ tool render EditProductContentEmail
$ tool render AddProductPaymentMethodType True en_US
$ tool render_pc True en_US

## service
$ tool service_model createOfbizDemo
```

## messages
```sh
$ python sagas/hybrid/sender.py user.system.hi xxx
```
