from tabulate import tabulate
import wcwidth
from sagas.crmsfa.odoo_facade import odoo, login
import fire
import odoorpc.fields as fields
from odoorpc.env import FIELDS_RESERVED

# https://stackoverflow.com/questions/2872512/python-truncate-a-long-string
def abbrev(data, l=15):
    info = (data[:l] + '..') if len(data) > l else data
    return info

def model_info():
    login()

    # models = odoo.execute('ir.model', 'browse', [])
    # print(models)
    table_header = ['model','name', 'count']
    table_data = []

    Order = odoo.env['ir.model']
    order_ids = Order.search([])
    print("✔ total models", len(order_ids))
    models=Order.browse(order_ids)
    # print(models[0])
    # odoo/addons/base/ir/ir_model.py
    for order in models:
        # print(order.model, order.name, order.count)    
        table_data.append((abbrev(order.model), 
                           abbrev(order.name), order.count))

    print(tabulate(table_data, headers=table_header, tablefmt='psql'))    

def desc_model(model):
    login()

    table_header = ['name','type', 'string']
    table_data = []

    attrs = {
                '_name': model,
                '_columns': {},
            }
    fields_get = odoo.execute(model, 'fields_get')
    for field_name, field_data in fields_get.items():
        if field_name not in FIELDS_RESERVED:
            Field = fields.generate_field(field_name, field_data)
            attrs['_columns'][field_name] = Field
            attrs[field_name] = Field
            # print(field_name, "%", field_data['type'])
            # print(field_data.keys())
            # ['searchable', 'sortable', 'depends', 'store', 
            # 'manual', 'type', 'company_dependent', 
            # 'change_default', 'readonly', 'string', 'required']
            table_data.append((abbrev(field_name, 20), field_data['type'], 
                               abbrev(field_data['string'], 25)))
            # addi: type(Field)

    # print(tabulate(table_data, headers=table_header, tablefmt='grid'))
    # print(tabulate(table_data, headers=table_header, tablefmt='fancy_grid'))
    print(tabulate(table_data, headers=table_header, tablefmt='psql'))

class OdooInfo(object):
    """docstring for OdooInfo"""
    def __init__(self):
        super(OdooInfo, self).__init__()

    def show_models(self):
        model_info()

    ## odoo_info "res.country"
    def desc_model(self, model):
        desc_model(model)

if __name__ == '__main__':
    fire.Fire(OdooInfo)
