from sagas.ofbiz.runtime_context import platform
import pandas as pd

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
            else:
                raise ValueError("Cannot support operator "+self.operator)

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
            elif method.startswith('remove'):
                entity = method[6:]
                pk = oc.delegator.makePK(entity, params)
                result = oc.delegator.removeByPrimaryKey(pk)
            elif method.startswith('get'):
                entity = method[3:]
                result = oc.delegator.findOne(entity, params, True)
            elif method.startswith('query'):
                entity = method[5:]
                result = oc.delegator.findByAnd(entity, params, None, True)
            elif method.startswith('list'):
                entity = method[4:]
                limit = 10
                offset = 0
                result = finder.find_list(entity, limit, offset)
            elif method.startswith('all'):
                entity = method[3:]
                result = oc.delegator.findAll(entity, False)
            elif method.startswith('ref'):
                entity = method[3:]
                result = MetaEntity(entity).record(args[0])
                if result is None:
                    raise ValueError("Cannot find record "+args[0])
            return result

        return entity_method

    def __repr__(cls):
        return "OfEntity(%r)" % (cls._name)


class MetaEntity(object):
    def __init__(self, name):
        self.name = name
        self.model = oc.delegator.getModelEntity(self.name)

    @property
    def primary(self):
        return self.model.getPkFieldNames()

    @property
    def field_names(self):
        names = self.model.getAllFieldNames()
        return names

    def find_one(self, **kwargs):
        params = oc.jmap(**kwargs)
        return oc.delegator.findOne(self.name, params, True)

    def find_list(self, limit=10, offset=0):
        return finder.find_list(self.name, limit, offset)

    def record(self, id_val):
        pk = self.model.getOnlyPk()
        ctx = oc.j.HashMap()
        ctx.put(pk.getName(), id_val)
        return oc.delegator.findOne(self.name, ctx, True)

    def desc(self, include_auto_fields=True):
        from sagas.ofbiz.builder import desc_model
        desc_model(self.name, include_auto_fields)


def search_entity(name_filter):
    name_filter=name_filter.lower()
    model_reader=oc.delegator.getModelReader()
    names=model_reader.getEntityNames()
    # print(len(names))
    for name in names:
        if name_filter in name.lower():
            print(name)

def create_data_frame(ent_name):
    ent=MetaEntity(ent_name)
    model_desc={'name':[str(fld.getName()) for fld in ent.model.getFieldsIterator()],
                'type':[str(fld.getType()) for fld in ent.model.getFieldsIterator()],
                'primary': ['*' if fld.getIsPk() else ' '  for fld in ent.model.getFieldsIterator()]
               }
    df = pd.DataFrame(model_desc)
    df['field type']=df['type'].astype('category')
    # df.sort_values(by='field type')
    return df

def create_relation_data_frame(ent_name):
    ent=MetaEntity(ent_name)
    rels=ent.model.getRelationsList(True, True, True)
    model_desc={'entity name':[str(fld.getRelEntityName()) for fld in rels],
                'type':[str(fld.getType()) for fld in rels],
                'relation':[rel.getTitle()+rel.getRelEntityName() for rel in rels]
               }
    df = pd.DataFrame(model_desc)
    df['relation type']=df['type'].astype('category')
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
