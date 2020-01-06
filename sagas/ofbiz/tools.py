import os

from sagas.ofbiz.services import OfService as s, oc, search_service
from sagas.ofbiz.entities import OfEntity as e, MetaEntity, load_xml_seed, get_serv


def set_value(type, value):
    if type == 'BigDecimal':
        value = 'oc.j.BigDecimal(' + value + ')'
    elif type == 'Timestamp':
        value = "oc.j.Timestamp.valueOf('" + value + "')"
    elif type == 'Integer':
        pass
    elif type == 'Boolean':
        value = "True" if value == "true" else "False"
    else:
        value = "'" + value + "'"
    return value

def delete_table(entity_name):
    group_name = oc.delegator.getEntityGroupName(entity_name)
    helper_info = oc.delegator.getGroupHelperInfo(group_name)
    msgs=oc.jlist()
    util=oc.j.DatabaseUtil(helper_info)
    ent = oc.delegator.getModelEntity(entity_name)
    util.deleteTable(ent, msgs)
    if len(msgs)>0:
        for msg in msgs:
            print(msg)
    else:
        print('ok')

class OfTools(object):
    def import_dir(self, dir):
        """
        Usage: $ python -m sagas.ofbiz.tools import_dir ./data/product/
        :param dir: data source directory
        :return: none
        """
        full_path=os.path.abspath(dir)
        ok, result=s().entityImportDir(path=full_path)
        if ok:
            for msg in result['messages']:
                print(msg)
        else:
            print("fail to import data files from directory.")
            print(result)

    def service_logs(self):
        from sagas.ofbiz.entities import OfEntity as e, oc
        oc.import_package('org.apache.ofbiz.service.ServiceDispatcher')
        log = oc.j.ServiceDispatcher.getServiceLogMap()
        for rs, value in log.items():
            print(oc.get(rs.getModelService(), 'name'), rs.getLocalName(), rs.getMode(), rs.getStartStamp(),
                  rs.getEndStamp())

    def ping(self):
        ok, ret=s().testScv(defaultValue=5.5, message="hello world")
        print(ok, ret)

    def users(self):
        from sagas.ofbiz.entities import OfEntity as e, oc
        rs=e().allUserLogin()
        for r in rs:
            print(r['userLoginId'])

    def entity_model(self, entity_name):
        from sagas.ofbiz.entities import OfEntity as e, oc, create_data_frame, create_relation_data_frame
        if not oc.has_entity(entity_name):
            print("Not found entity", entity_name)
            return

        df=create_data_frame(entity_name)
        print(df)
        print("---- ✁ relations")
        df=create_relation_data_frame(entity_name)
        print(df)

    def remove_model(self, entity_name):
        oc.import_package('org.apache.ofbiz.entity.jdbc.*')
        delete_table(entity_name)
        print('done.')

    def entity_data(self, entity_name, limit=10):
        """
        $ python -m sagas.ofbiz.tools entity-data DataResourceType 1000
        $ tool entity-data DataResourceType 1000
        $ tool entity-data WorkEffortType 1000
        :param entity_name:
        :param limit:
        :return:
        """
        from sagas.ofbiz.entities import OfEntity as e, finder, record_list_df
        # limit = 10
        offset = 0
        result = finder.find_list(entity_name, limit, offset)
        result = record_list_df(entity_name, result, drop_null_cols=True, contains_internal=False)
        print(result)

    def entity_package(self, package_name):
        from sagas.ofbiz.entities import OfEntity as e, get_package_entities
        ents=get_package_entities('com.sagas.dss')
        print(ents)

    def entity_ref(self, entity, id_val, disp='table'):
        from sagas.ofbiz.entities import format
        result = MetaEntity(entity).record(id_val)
        if disp == 'json':
            result = oc.j.ValueHelper.entityToJson(result, oc.jmap())
            print(result)
        else:
            format(result)

    def search_entity(self, name_filter):
        """
        $ tool search_entity DataResourceType
        $ tool search_entity WorkEffort
        :param name_filter:
        :return:
        """
        name_filter=name_filter.lower()
        model_reader=oc.delegator.getModelReader()
        names=model_reader.getEntityNames()
        # print(len(names))
        for name in names:
            if name_filter in name.lower():
                print(name)

    def entity_model_list(self):
        """
        $ tool entity_model_list
        :return:
        """
        import services_common_pb2 as sc
        q = sc.InfoQuery(queryItems=[""])
        serv=get_serv()
        names = serv.GetEntityNames(q)
        print(names)
        # print(f".. total entities {len(names)}")

    def load_entity_data(self, data_file):
        """
        $ tool load_entity_data '/pi/stack/data/product/ProductPriceTestData.xml'
        :param data_file:
        :return:
        """
        load_xml_seed(data_file)

    def service_model(self, service_name):
        from sagas.ofbiz.services import OfService as s, create_service_data_frame
        meta=create_service_data_frame(service_name)
        print(meta)

    def search_service(self, name_filter):
        """
        $ tool search_service WorkEffort
        :param name_filter:
        :return:
        """
        rs=search_service(name_filter)
        for el in rs:
            print(el)

    def form(self, form_name):
        from sagas.ofbiz.entities import OfEntity as e, oc, finder
        hub = oc.component('entity_event_hub')
        forms = oc.component('form_mgr')

        # form_loc="component://content/widget/forum/BlogForms.xml;EditBlog;en_US"
        # form_loc = 'component://party/widget/partymgr/LookupForms.xml;LookupPartyName;en_US'
        form_loc='component://product/widget/catalog/ProductForms.xml;AddProductPaymentMethodType;en_US'
        form = forms.getMetaForm(form_loc)
        print(form)

    def form_meta(self, form_name, locale='zh_CN'):
        from sagas.ofbiz.forms import get_form_meta
        meta_list=get_form_meta(form_name, locale)
        for meta in meta_list:
            print(meta)

    def form_list(self):
        """
        $ tool form_list
        :return:
        """
        from sagas.ofbiz.forms import print_form_list
        print_form_list()

    def search_form(self, name_filter):
        """
        $ tool search_form WorkEffort
        :param name_filter:
        :return:
        """
        from sagas.ofbiz.forms import print_form_list
        print_form_list(name_filter=name_filter)

    def convert_minilang_from_clip(self):
        """
        Will convert the xml content in clipboard:
        <set field="serviceCtx.currencyUomId" value="USD"/>
        <set field="serviceCtx.costComponentTypePrefix" value="EST_STD"/>
        :return:
        """
        import xml.etree.ElementTree as ET
        import clipboard
        sett = clipboard.paste()
        root = ET.fromstring('<routine>' + sett + '</routine>')
        # print('root', root.tag)
        result = []
        for setter in root.findall('set'):
            field = setter.get('field')
            type = setter.get('type')
            value = setter.get('value')
            if '.' in field:
            # if field.startswith("serviceCtx.") or field.startswith("searchParams."):
                if value is not None:
                    value=set_value(type, value)
                else:
                    value=setter.get('from-field')
                line = "{}={}".format(field.split('.')[1], value)
                result.append(line)

        text = ",\n".join(result)
        print(text)
        clipboard.copy(text)

    def clip_vars(self):
        """
        <set field="productId" value="PROD_MANUF"/>
        :return:
        """
        import xml.etree.ElementTree as ET
        import clipboard
        sett = clipboard.paste()
        root = ET.fromstring('<routine>' + sett + '</routine>')
        # print('root', root.tag)
        result = []
        for setter in root.findall('set'):
            field = setter.get('field')
            value= set_value(setter.get('type'), setter.get('value'))
            result.append("%s=%s"%(field, value))

        text = "\n".join(result)
        print(text)
        clipboard.copy(text)

    def test_form(self):
        oc.import_package('org.apache.ofbiz.base.util.UtilMisc')

        forms = oc.component('form_mgr')
        locale = oc.j.UtilMisc.ensureLocale('zh_CN')
        loc = 'component://product/widget/catalog/ProductForms.xml'
        # form_name='FindProduct'
        form_name = 'EditProduct'
        form = forms.getModelForm(form_name, loc)
        forms.renderForm(form, locale)

    def test_render(self):
        from sagas.ofbiz.entities import OfEntity as e

        oc.import_package('org.apache.ofbiz.base.util.UtilMisc')
        oc.import_package('com.sagas.meta.PropertiesManager')
        oc.import_package('org.apache.ofbiz.widget.renderer.fo.FoFormRenderer')
        oc.import_package('org.apache.ofbiz.widget.renderer.FormRenderer')
        ffr = oc.j.FoFormRenderer()

        forms = oc.component('form_mgr')
        loc = 'component://product/widget/catalog/ProductForms.xml'
        # form_name='FindProduct'
        form_name = 'EditProduct'
        form = forms.getModelForm(form_name, loc)
        fr = oc.j.FormRenderer(form, ffr)
        writer = oc.j.StringBuilder()

        locale = oc.j.UtilMisc.ensureLocale(None)
        ctx = oc.jmap(locale=locale)
        ctx.put('product', e().refProduct('GZ-2002'))
        oc.j.PropertiesManager.execPropertyMap(ctx, "ContentUiLabels", "uiLabelMap", True)

        fr.render(writer, ctx)
        print(writer.toString())

    def product_forms(self):
        fm=oc.component('product_forms')
        print(fm.renderEditProduct("GZ-2002", 'zh_CN'))

    def product_render(self):
        fm=oc.component('product_forms')
        print(fm.renderForm("AddProductPaymentMethodType", 'zh_CN'))

    def render(self, form_name, proto=False, locale='zh_CN'):
        from sagas.ofbiz.forms import render_form
        render_form(form_name, locale=locale, params=None, proto=proto)

    def render_pc(self, proto=False, locale='zh_CN'):
        from sagas.ofbiz.forms import render_form
        params=oc.jmap(contentId='HELP_PRODUCT')
        form_name='EditProductContentEmail'
        render_form(form_name, locale=locale, params=params, proto=proto)

    def render_ep(self):
        from sagas.ofbiz.forms import render_form
        params=oc.jmap(product=e().refProduct("GZ-2002"))
        form_name='EditProduct'
        render_form(form_name, locale='zh_CN', params=params)

if __name__ == '__main__':
    import fire
    fire.Fire(OfTools)
