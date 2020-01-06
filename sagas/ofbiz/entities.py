import datetime

from sagas.ofbiz.runtime_context import platform
import pandas as pd
import json

import services_common_pb2 as sc
import services_common_pb2_grpc as sc_service
from values_pb2 import TaStringEntriesBatch

oc=platform.oc
finder=platform.finder

class OfEntity(object):
    """
    ## Use OfEntity

    from sagas.ofbiz.entities import oc,finder,OfEntity

    OfEntity().createProductType(productTypeId="Test_type_2")
    OfEntity().storeProductType(productTypeId="Test_type_2")
    OfEntity().getProductType(productTypeId="Test_type_2")
    OfEntity().removeProductType(productTypeId="Test_type_2")
    OfEntity().queryProductType(productTypeId="Test_type_2")

    for p in OfEntity().listProductType():
        print(p['productTypeId'])
    for p in OfEntity().allProductType():
        print(p['productTypeId'])

    ---

    from sagas.ofbiz.entities import OfEntity as e
    e('meta').Person
    e('relations').Person

    import sagas.ofbiz.entities as ee
    product=e().refProduct('GZ-2002')
    """
    _name = None
    _fields = {}  # {field: field object}

    def __init__(self, operator=None):
        super(OfEntity, self).__init__()
        self.operator=operator

    def __getattr__(self, method):
        """Provide a dynamic access to a CRUD method."""
        if method.startswith('_'):
            return super(OfEntity, self).__getattr__(method)

        if self.operator is not None:
            if self.operator == "meta":
                return create_data_frame(method)
            elif self.operator == 'relations':
                return create_relation_data_frame(method)
            elif self.operator=='model':
                return oc.delegator.getModelEntity(method)
            else:
                # raise ValueError("Cannot support operator "+self.operator)
                # the others will process in entity_method
                pass

        def entity_method(*args, **kwargs):
            """Return the result of the service request."""
            # check args with runSync/runSyncIgnore/...

            params = oc.jmap(**kwargs)
            result = None
            if method.startswith('create'):
                entity = method[6:]
                result = oc.delegator.create(entity, params)
            elif method.startswith('store'):
                entity = method[5:]
                val = oc.delegator.makeValue(entity, params)
                result = oc.delegator.createOrStore(val)
            elif method.startswith('delete'):
                entity = method[6:]
                pk = oc.delegator.makePK(entity, params)
                result = oc.delegator.removeByPrimaryKey(pk)
            elif method.startswith('remove'):
                entity = method[6:]
                result = oc.delegator.removeByAnd(entity, params)
            elif method.startswith('get'):
                entity = method[3:]
                result = oc.delegator.findOne(entity, params, True)
            elif method.startswith('query'):
                entity = method[5:]
                result = oc.delegator.findByAnd(entity, params, None, True)
                if self.operator=='df':
                    result=record_list_df(entity, result)
            elif method.startswith('list'):
                entity = method[4:]
                limit = 10
                offset = 0
                if '_limit' in kwargs:
                    limit=kwargs['_limit']
                if '_offset' in kwargs:
                    offset=kwargs['_offset']
                result = finder.find_list(entity, limit, offset)
                if self.operator=='df':
                    result=record_list_df(entity, result)
                elif self.operator=='json':
                    result = oc.j.ValueHelper.valueListToJson(result)
            elif method.startswith('all'):
                entity = method[3:]
                result = oc.delegator.findAll(entity, False)
                if self.operator=='df':
                    result=record_list_df(entity, result)
            elif method.startswith('ref'):
                entity = method[3:]
                result = MetaEntity(entity).record(args[0])
                if self.operator == 'json':
                    result = oc.j.ValueHelper.entityToJson(result, oc.jmap())
                elif self.operator=='table':
                    format(result)
                if result is None:
                    raise ValueError("Cannot find record "+args[0])
            elif method.startswith('count'):
                entity = method[len('count'):]
                result = MetaEntity(entity).count()
            return result

        return entity_method

    def __repr__(cls):
        return "OfEntity(%r)" % (cls._name)

    @classmethod
    def remove(cls, value):
        oc.delegator.removeByPrimaryKey(value.getPrimaryKey())


class MetaEntity(object):
    def __init__(self, name):
        from sagas.ofbiz.entity_global_ref import EntityGlobalRef
        self.name = name
        self.model = oc.delegator.getModelEntity(self.name)
        if self.model is not None:
            self.rels = self.model.getRelationsList(True, True, True)
            self.global_ref=EntityGlobalRef(name)
        else:
            raise ValueError("Cannot find entity model {}".format(name))

    @property
    def primary(self):
        return [str(v) for v in self.model.getPkFieldNames()]

    @property
    def field_names(self):
        """
        import sagas.ofbiz.entities as ee
        ent=ee.entity('Product')
        ent.field_names
        :return:
        """
        names = self.model.getAllFieldNames()
        return names

    def find_one(self, **kwargs):
        params = oc.jmap(**kwargs)
        return oc.delegator.findOne(self.name, params, True)

    def to_json(self, val, filter=False, contains_gid=False):
        """
        Usage::

            import sagas.ofbiz.entities as ee
            ent=ee.entity('Product')
            val=ent.record('GZ-2002')
            print(ent.to_json(val,True))

        :param val:
        :param filter:
        :return:
        """
        import sagas.graph.value_filter as vf
        ret= oc.j.ValueHelper.entityToJson(val, oc.jmap())
        jval=json.loads(ret)
        if filter:
            jval=vf.filter_json_val(self.model, jval)
        if contains_gid:
            gid=self.global_ref.get_gid(val)
            jval['gid']=gid
            jval['uid']="_:"+gid
            jval['mo_type']=self.name
        return jval

    def find_list(self, limit=10, offset=0):
        return finder.find_list(self.name, limit, offset)

    def all(self):
        return oc.delegator.findAll(self.name, False)

    def count(self):
        total = oc.delegator.findCountByCondition(self.name, None, None, None)
        return(total)

    def record(self, id_val, to_json=False):
        pk = self.model.getOnlyPk()
        ctx = oc.j.HashMap()
        ctx.put(pk.getName(), id_val)
        val= oc.delegator.findOne(self.name, ctx, False)
        if to_json:
            return self.to_json(val)
        else:
            return val

    def desc(self, include_auto_fields=True):
        from sagas.ofbiz.builder import desc_model
        desc_model(self.name, include_auto_fields)

    def get_rel_ent_names(self, only_get_entity_name=False):
        if only_get_entity_name:
            rel_ents = set([str(rel.getRelEntityName()) for rel in self.rels])
        else:
            # relation_name = rel.getTitle() + rel.getRelEntityName()
            rel_ents = set([str(rel.getTitle() + rel.getRelEntityName()) for rel in self.rels])
        return rel_ents


def to_json(val, filter=False):
    import sagas.graph.value_filter as vf
    ret = oc.j.ValueHelper.entityToJson(val, oc.jmap())
    jval = json.loads(ret)
    model = oc.delegator.getModelEntity(val.getEntityName())
    if filter:
        return vf.filter_json_val(model, jval)
    return jval

def entity(entity_name):
    return MetaEntity(entity_name)

def search_entity(name_filter):
    name_filter=name_filter.lower()
    model_reader=oc.delegator.getModelReader()
    names=model_reader.getEntityNames()
    # print(len(names))
    for name in names:
        if name_filter in name.lower():
            print(name)

def all_entities(include_view=True):
    model_reader=oc.delegator.getModelReader()
    names=model_reader.getEntityNames()
    # return names
    if include_view:
        return [str(v) for v in names]
    else:
        rs=[]
        for name in names:
            model=model_reader.getModelEntity(name)
            if not oc.j.Utils.isViewEntity(model):
                rs.append(name)
        return rs

def create_data_frame(ent_name, show_internal=True):
    ent=MetaEntity(ent_name)
    model_desc={'name':[str(fld.getName()) for fld in ent.model.getFieldsIterator()],
                'type':[str(fld.getType()) for fld in ent.model.getFieldsIterator()],
                'primary': ['*' if fld.getIsPk() else ' '  for fld in ent.model.getFieldsIterator()],
                'internal': ['*' if fld.getIsAutoCreatedInternal() else ' ' for fld in ent.model.getFieldsIterator()]
               }
    df = pd.DataFrame(model_desc)
    # df['field type']=df['type'].astype('category')
    # df.sort_values(by='field type')
    if not show_internal:
        df=df[df['internal']!='*']
    return df

def repr_keymaps(keymaps):
    fields=[]
    for k in keymaps:
        fields.append(k.getFieldName()+'►'+k.getRelFieldName())
    return ", ".join(fields)

def create_relation_data_frame(ent_name):
    ent=MetaEntity(ent_name)
    rels=ent.model.getRelationsList(True, True, True)
    model_desc={'entity name':[str(fld.getRelEntityName()) for fld in rels],
                'type':[str(fld.getType()) for fld in rels],
                'relation':[rel.getTitle()+rel.getRelEntityName() for rel in rels],
                'mapping':[repr_keymaps(rel.getKeyMaps()) for rel in rels]
               }
    df = pd.DataFrame(model_desc)
    # df['relation type']=df['type'].astype('category')
    # df.sort_values(by='field type')
    return df

def print_record(ent_name, id, show_null=True):
    rec = MetaEntity(ent_name).record(id)
    format(rec, show_null)

def format(rec, show_null=True):
    from tabulate import tabulate
    table_header = ['name','value']
    table_data = []

    for k,v in rec.items():
        if v is None and not show_null:
            pass
        else:
            table_data.append((k, v))
    print(tabulate(table_data, headers=table_header, tablefmt='psql'))

def default_thru():
    from datetime import date
    import time
    from datetime import timedelta

    year = timedelta(days=365)
    hundred_years = 100 * year
    default_thru = date.today() + hundred_years
    return default_thru

def record_list_df(ent_name, records, drop_null_cols=True, contains_internal=True):
    import pyarrow as pa

    ent = MetaEntity(ent_name)
    field_names = ent.field_names
    data = []
    skip_fields = ['lastModifiedDate']
    pnames = []
    for fld in field_names:
        model_fld = ent.model.getField(fld)
        if not contains_internal and model_fld.getIsAutoCreatedInternal():
            pass
        elif fld not in skip_fields:
            pnames.append(fld)

            field_arr = []
            fld_type = model_fld.getType()
            # print('- ', fld, fld_type)
            for rec in records:
                val = rec[fld]
                if val is None:
                    if fld == 'thruDate':
                        val = default_thru()
                elif fld_type == 'date-time':
                    time_ms = rec[fld].getTime()
                    val = datetime.datetime.fromtimestamp(time_ms / 1000)
                elif fld_type in ('fixed-point', 'currency-amount', 'currency-precise'):
                    val=float(val)

                field_arr.append(val)
            data.append(pa.array(field_arr))

    batch = pa.RecordBatch.from_arrays(data, pnames)
    batches = [batch]
    table = pa.Table.from_batches(batches)
    if drop_null_cols:
        return table.to_pandas().dropna(axis=1,how='all')
    else:
        return table.to_pandas()


def get_package_entities(pkg):
    model_reader = oc.delegator.getModelReader()
    tree_map = model_reader.getEntitiesByPackage(None, None)
    entries = tree_map[pkg]
    return entries

def get_serv():
    from client_wrapper import ServiceClient
    serv = ServiceClient(sc_service, 'EntityServantStub', 'localhost', 50051)
    return serv

def load_xml_seed(xml_file):
    import xml.etree.ElementTree as ET
    from sagas.ofbiz.entity_prefabs import EntityPrefabs
    from sagas.util.string_util import abbrev

    # xml_file = 'data/product/ProductPriceTestData.xml'
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ep = EntityPrefabs()
    record_set, ids = ep.convert_to_record_set(root)
    print(ids)

    rs = []
    for item in record_set:
        rs.append(item[1])
        print(item[1].entityName)  # TaStringEntries
        print('\t', abbrev(item[0]))
    batch = TaStringEntriesBatch(records=rs)
    serv=get_serv()
    ret = serv.StoreAll(batch)
    print(ret)

