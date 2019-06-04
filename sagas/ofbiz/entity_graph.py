import sagas.ofbiz.entities as ee
from sagas.ofbiz.entity_gen import get_dgraph_type
import json

def get_record_json(entity_name, id_val):
    ent=ee.entity(entity_name)
    val=ent.record(id_val)
    return(ent.to_json(val,True))

model_schema = """
mo_name: string @index(exact) .
mo_relation: uid @reverse .
mo_total: int .
mo_last_modified: datetime .
mo_table: string .
mo_service: string .
mo_form_uri: string .
mo_field: uid .
mo_type: string .
mo_mode: string .
mo_primary: bool .
mo_primary_keys: [string] @index(term) .    
"""

def deduce_type(a,b):
    src=set([a,b])
    result='string'
    if src==set(['string','int']):
        result='string'
    elif src==set(['int','float']):
        result='float'
    elif src==set(['string','datetime']):
        result='datetime'
    else:
        raise ValueError('cannot reduce: %s-%s', a,b)
    return result

def collect_internal_fields(ent_name, fld_mapping):
    ent= ee.MetaEntity(ent_name)
    for fld in ent.model.getFieldsIterator():
        # print(fld.getName(), fld.getType(), fld.getIsPk(), fld.getIsAutoCreatedInternal())
        if fld.getIsAutoCreatedInternal():
            fld_name=str(fld.getName())
            fld_type=get_dgraph_type(fld.getType())
            fld_mapping[fld_name]=fld_type

def to_schema(var_map):
    all_types=[]
    for k,v in var_map.items():
        all_types.append("%s: %s ."%(k,v))
    schema='\n'.join(all_types)+"\n"
    return schema

def collect_fields(ent_name, fld_mapping, skip_fields, pks, messages):
    ent= ee.MetaEntity(ent_name)
    for fld in ent.model.getFieldsIterator():
        # print(fld.getName(), fld.getType(), fld.getIsPk(), fld.getIsAutoCreatedInternal())
        if not fld.getIsAutoCreatedInternal():
            fld_name=str(fld.getName())
            fld_type=get_dgraph_type(fld.getType())
            # if fld.getIsPk():
            if fld.getIsPk() and fld_type!='datetime':
                pks.add(fld_name)
            if fld_name in fld_mapping:
                if fld_type!=fld_mapping[fld_name]:
                    messages.append("%s's field %s has different field type: %s-%s"%
                         (ent_name, fld_name, fld_type, fld_mapping[fld_name])
                        )
                    skip_fields.append((ent_name, fld_name, fld_type))
                    dtype=deduce_type(fld_type, fld_mapping[fld_name])
                    fld_mapping[fld_name]=dtype
                else:
                    pass
            else:
                fld_mapping[fld_name]=fld_type

def collect_schema(entities):
    fld_mapping = {}
    skip_fields = []
    messages = []
    pks=set()
    for ent in entities:
        collect_fields(ent, fld_mapping, skip_fields, pks, messages)
    print('deduce fields', len(skip_fields))
    print('total fields', len(fld_mapping))
    for sf in skip_fields[:5]:
        print(sf)
    for m in messages:
        if 'datetime' in m:
            print(m)

    all_types = []
    for k, v in fld_mapping.items():
        if k in pks:
            all_types.append("%s: %s @index(exact) ." % (k, v))
        else:
            all_types.append("%s: %s ." % (k, v))
    # print(all_types[:5])
    schema = '\n'.join(all_types)

    fld_map = {}
    collect_internal_fields('Person', fld_map)
    # print(fld_map)
    return (model_schema + to_schema(fld_map) + schema)

class EntityGraph(object):
    def __init__(self):
        import sagas.graph.graph_manager as g
        self.gm = g.GraphManager()

    def internal_schema(self):
        """
        $ python -m sagas.ofbiz.entity_graph internal-schema
        :return:
        """
        fld_map = {}
        collect_internal_fields('Person', fld_map)
        # print(fld_map)
        print(model_schema+to_schema(fld_map))

    def setup_schema(self, entities, do_set=False):
        """
        $ python -m sagas.ofbiz.entity_graph setup_schema [Person,Party,Product]
        $ python -m sagas.ofbiz.entity_graph setup_schema [Person,Party,Product] True
        :param entities:
        :return:
        """

        schema=collect_schema(entities)
        print(schema)
        if do_set:
            self.gm.reset_schema(schema)
            print('done.')

    def get_schema(self, entity, include_relates=True):
        """
        $ python -m sagas.ofbiz.entity_graph get_schema Example
        $ python -m sagas.ofbiz.entity_graph get_schema Example False
        :param entity:
        :param include_relates:
        :return:
        """
        if include_relates:
            entities = ee.entity(entity).get_rel_ent_names(True)
            print('.. getting schema for entities:', ', '.join(entities))
            schema = collect_schema(entities)
            print(schema)
        else:
            schema = collect_schema([entity])
            print(schema)

    def setup_schema_head(self, entity):
        """
        $ python -m sagas.ofbiz.entity_graph setup_schema_head Example
        :param entity:
        :return:
        """
        try:
            entities=ee.entity(entity).get_rel_ent_names(True)
            print('.. getting schema for entities:', ', '.join(entities))
            self.setup_schema(entities, True)
        except ValueError as err:
            print(err)

    def add_val(self, entity_name, id_val, verbose=True):
        """
        $ python -m sagas.ofbiz.entity_graph add_val Product 'GZ-2002'
        :param entity_name:
        :param id_val:
        :return:
        """
        # import sagas.graph.graph_manager as g
        # gm = g.GraphManager()
        jval=get_record_json(entity_name, id_val)
        if verbose:
            print(json.dumps(jval, indent=2))
        self.gm.add_object(jval)
        print('done.')

    def load_json_data(self, schema_head, file_name, reset=True):
        import json_utils
        if reset:
            self.setup_schema_head(schema_head)
        ps = json_utils.read_json_file(file_name)
        self.gm.add_object(ps)

    def q_product(self):
        """
        $ python -m sagas.ofbiz.entity_graph q_product
        :return:
        """
        query = """{
          find_product(func: eq(productId, "GZ-2002")) {
            uid
            productName
            description
          }
        }
        """
        rs=self.gm.query(query)
        print(json.dumps(rs, indent=True))

    def stuff(self):
        """
        $ python -m sagas.ofbiz.entity_graph stuff
        :return:
        """
        self.setup_schema(['Person','Party','Product'], True)
        self.add_val('Product', 'GZ-2002')
        self.q_product()

if __name__ == '__main__':
    import fire
    fire.Fire(EntityGraph)

