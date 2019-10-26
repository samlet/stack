from functools import singledispatch
import streamlit as st

from sagas.ofbiz.entities import MetaEntity
from sagas.ofbiz.services import OfService
from sagas.ofbiz.entities import OfEntity as e, format
from sagas.ofbiz.services import OfService as s, oc
from datetime import datetime

# product("GZ-2002", 'price')
# product(dt('2013-07-04 00:00:00'), "Test_product_A")

@singledispatch
def product(arg, prop, verbose=False):
    raise NotImplementedError('Unsupported type')

def product_price(id):
    product = MetaEntity("Product").record(id)
    ok, ret = OfService().calculateProductPrice(product=product)
    st.markdown(f"The **default** price is `{ret['defaultPrice']}`, the **list** price is `{ret['listPrice']}`")

def output_rec(rec, show_null=True):
    import sagas
    table_header = ['name','value']
    table_data = []

    for k,v in rec.items():
        if v is None and not show_null:
            pass
        else:
            table_data.append((k, v))
    st.table(sagas.to_df(table_data, ['key','val']))

def price_from_date(id, dt):
    props=e().getProductPrice(productId=id,
                        productPriceTypeId='AVERAGE_COST',
                        productPricePurposeId='COMPONENT_PRICE',
                        productStoreGroupId='Test_group',
                        currencyUomId='USD',
                        fromDate=oc.j.Timestamp.valueOf(str(dt)))
    # st.table(sagas.dict_df(props))
    output_rec(props, False)

@product.register(str)
def _(arg, prop, verbose=False):
    st.write(".. argument is of type ", type(arg))
    if prop=='price':
        product_price(arg)
    else:
        st.error(f'No such prop {prop}')

@product.register(datetime)
def _(arg, product_id, verbose=False):
    st.write(".. argument is of type ", type(arg))
    price_from_date(product_id, arg)

exports={product}



