import odoorpc
from tabulate import tabulate
import wcwidth
from sagas.crmsfa.odoo_facade import odoo, login
import odoorpc.fields as fields
from odoorpc.env import FIELDS_RESERVED
import json
import sagas.util.pandas_helper as ph

# https://stackoverflow.com/questions/2872512/python-truncate-a-long-string
def abbrev(data, l=15):
    info = (data[:l] + '..') if len(data) > l else data
    return info

def model_info():
    # models = odoo.execute('ir.model', 'browse', [])
    # print(models)
    table_header = ['model','name', 'count']
    table_data = []

    Models = odoo.env['ir.model']
    order_ids = Models.search([])

    try:
        models=Models.browse(order_ids)
        # print(models[0])
        # odoo/addons/base/ir/ir_model.py
        for order in models:
            # print(order.model, order.name, order.count)
            table_data.append((abbrev(order.model),
                               abbrev(order.name), order.count))

        print(tabulate(table_data, headers=table_header, tablefmt='psql'))
    except odoorpc.error.RPCError as error:
        print(error)

    print("✔ total models", len(order_ids))

def desc_model(model):
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

def records(model_name, fields_get=None):
    if fields_get is None:
        fields_get = ['name']
    Model = odoo.env[model_name]
    model_ids = Model.search([])
    print("total", len(model_ids))
    rs=[]
    for el in Model.browse(model_ids):
        rec=[]
        for fld in fields_get:
            rec.append(getattr(el, fld))
        rs.append(rec)
    return rs

def list_fields(model='res.lang', lang="zh_CN", get_view=False):
    """
    list_fields(model='res.lang', lang="zh_CN", get_view=False)
    list_fields(model='res.lang', lang="ru_RU", get_view=False)

    :param lang:
    :param get_view:
    :return:
    """
    from sagas import to_df
    # see data ref: stack/sagas/dataset/partner_obj.json
    odoo.env.context['lang'] = lang
    partner_obj = odoo.env[model]
    if get_view:
        obj = partner_obj.fields_view_get()
    else:
        obj = partner_obj.fields_get()
    # text = json.dumps(obj, indent=4, ensure_ascii=False)
    rs = []
    for k, v in obj.items():
        rel = ''
        if 'relation' in v:
            rel = v['relation']

        rs.append((k, v['type'], v['string'], rel))
    return to_df(rs, ['name', 'type', 'title', 'relation'])

class OdooInfo(object):
    """docstring for OdooInfo"""
    def __init__(self):
        super(OdooInfo, self).__init__()
        login(db="demo", username="admin", password="admin")

    def show_models(self, lang='zh_CN'):
        """
        $ start odoo_info
        $ python -m sagas.crmsfa.odoo_info show-models
        $ python -m sagas.crmsfa.odoo_info show-models zh_CN
        $ python -m sagas.crmsfa.odoo_info show-models fr_FR  # 使用法语的数据模型名称
        :return:
        """
        # odoo.env.context['lang'] = 'fr_FR'
        odoo.env.context['lang'] = lang
        model_info()

    ## odoo_info "res.country"
    def desc_model(self, model, lang="zh_CN"):
        """
        显示数据模型的字段信息:
        $ start show res.partner
        $ python -m sagas.crmsfa.odoo_info desc-model res.partner   # 合作伙伴
        $ python -m sagas.crmsfa.odoo_info desc-model crm.lead      # 潜在客户
        $ python -m sagas.crmsfa.odoo_info desc-model res.country
        $ python -m sagas.crmsfa.odoo_info desc-model res.lang
        :param model:
        :return:
        """
        odoo.env.context['lang'] = lang
        desc_model(model)

    def exists_model(self, model):
        """
        $ python -m sagas.crmsfa.odoo_info exists_model res.partner
        :param model:
        :return:
        """
        model_exists = odoo.execute('ir.model', 'search',
                                    [('model', '=', model)])
        print(bool(model_exists))

    def all_products(self, lang='fr_FR', show_df=False):
        """
        显示所有产品的记录
        $ python -m sagas.crmsfa.odoo_info all_products
        $ python -m sagas.crmsfa.odoo_info all_products zh_CN True
        $ python -m sagas.crmsfa.odoo_info all_products ru_RU  # 可以指定语言, 比如俄语
        $ open http://localhost:8069/web#action=283&model=product.template&view_type=kanban&menu_id=168

        :param lang:
        :return:
        """
        import sagas
        Product = odoo.env['product.product']
        odoo.env.context['lang'] = lang
        product_ids = Product.search([])
        if not show_df:
            for p in Product.name_get(product_ids):
                print(p)
        else:
            sagas.print_rs(Product.name_get(product_ids), ['id', 'product'])

    def all_langs(self):
        """
        $ python -m sagas.crmsfa.odoo_info all_langs
        :return:
        """
        cols = ['name', 'code']
        rs = records('res.lang', cols)
        print(ph.to_df(rs, cols))

    def list(self, model, cols):
        """
        # step 1
            $ python -m sagas.crmsfa.odoo_info desc-model stock.picking
        # step 2
            $ python -m sagas.crmsfa.odoo_info list stock.picking partner_id,scheduled_date,origin,state
        # step 3
            $ open http://localhost:8069/web?#action=256&active_id=1&model=stock.picking&view_type=list&menu_id=168

        :param model:
        :param cols:
        :return:
        """
        rs = records(model, cols)
        print(ph.to_df(rs, cols))

    def fields(self, model, lang="zh_CN", get_view=False):
        """
        $ odoo_info fields res.partner
        $ python -m sagas.crmsfa.odoo_info fields res.partner
        $ python -m sagas.crmsfa.odoo_info fields res.partner en_US
        $ python -m sagas.crmsfa.odoo_info fields res.partner ja_JP True
        :param model:
        :return:
        """
        odoo.env.context['lang'] = lang
        partner_obj = odoo.env[model]
        if get_view:
            obj = partner_obj.fields_view_get()
        else:
            obj = partner_obj.fields_get()
        text = json.dumps(obj, indent=4, ensure_ascii=False)
        print(text)

    def list_fields(self, model='res.lang', lang="zh_CN", get_view=False):
        """
        $ python -m sagas.crmsfa.odoo_info list_fields res.partner zh_CN
        $ python -m sagas.crmsfa.odoo_info list_fields res.lang ru_RU
        :return:
        """
        print(list_fields(model, lang, get_view))

if __name__ == '__main__':
    import fire
    fire.Fire(OdooInfo)

