from sagas.ofbiz.entities import OfEntity as e, oc, finder, MetaEntity
from sagas.ofbiz.services import OfService as s, MetaService, get_params

oc.import_package('com.bluecc.pay.modules.*')

payments=oc.j.Payments(oc.dispatcher, oc.delegator)
invoices=oc.j.Invoices(oc.dispatcher, oc.delegator)

def test_invoices():
    total=invoices.getInvoiceTotal('demo10000')
    print(f"total {total}")

"""
from sagas.modules.deles import *
total=invoices.getInvoiceTotal('demo10000')
print(f"total {total}")
"""


