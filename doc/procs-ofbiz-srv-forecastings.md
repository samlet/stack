# procs-ofbiz-services.md
## invoice
```python
s().createInvoice(invoiceDate=DateTime.now_timestamp(), 
                invoiceTypeId='PURCHASE_INVOICE',
                partyIdFrom='DEMO_COMPANY',
                partyId='DEMO_COMPANY1')
ok,r=s().getInvoice(invoiceId='1001')
s().setInvoiceStatus(invoiceId='1002',
    statusId='INVOICE_APPROVED')

```
```python
e('meta').InvoiceItem
    6   productId       id  id
    7   productFeatureId        id  id
    8   parentInvoiceId     id  id
    9   parentInvoiceItemSeqId      id  id
    10  uomId       id  id
    11  taxableFlag     indicator   indicator
    12  quantity        fixed-point fixed-point
    13  amount      currency-precise    currency-precise
    14  description     description description
    15  taxAuthPartyId      id  id
    16  taxAuthGeoId        id  id
    17  taxAuthorityRateSeqId       id  id
    18  salesOpportunityId      id  id    
e('meta').Invoice
    0   invoiceId   *   id  id
    1   invoiceTypeId       id  id
    2   partyIdFrom     id  id
    3   partyId     id  id
    4   roleTypeId      id  id
    5   statusId        id  id
    6   billingAccountId        id  id
    7   contactMechId       id  id
    8   invoiceDate     date-time   date-time
    9   dueDate     date-time   date-time
    10  paidDate        date-time   date-time    
```


