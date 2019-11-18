from functools import singledispatch
import streamlit as st
from sagas.crmsfa.odoo_facade import odoo, login
from sagas.crmsfa.odoo_info import records
import sagas

"""
odoo_list('products'), 
odoo_list('stock_picking')
"""

login(db="demo", username="admin", password="admin")

def list_products(lang='zh_CN'):
    Product = odoo.env['product.product']
    odoo.env.context['lang'] = lang
    product_ids = Product.search([])
    st.table(sagas.to_df(Product.name_get(product_ids), ['id', 'product']))
    st.markdown('[Browse Products](http://localhost:8069/web#action=283&model=product.template&view_type=kanban&menu_id=168)')

def list_stock_picking():
    model='stock.picking'
    cols='partner_id,scheduled_date,origin,state'.split(',')
    rs = records(model, cols)
    st.table(sagas.to_df(rs, cols))
    st.markdown('[Browse Stock Picking](http://localhost:8069/web?#action=256&active_id=1&model=stock.picking&view_type=list&menu_id=168)')

fn_map={'products':list_products,
        'stock_picking':list_stock_picking,
        }

@singledispatch
def odoo_list(arg, verbose=False):
    raise NotImplementedError('Unsupported type')

@odoo_list.register(str)
def _(arg, verbose=False):
    st.write(".. argument is of type ", type(arg))
    if arg in fn_map:
        fn_map[arg]()

exports={odoo_list}

