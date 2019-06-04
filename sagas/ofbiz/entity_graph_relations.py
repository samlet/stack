import json_utils
import sagas.ofbiz.entities as ee
import json

oc=ee.oc
def to_json(val):
    # import sagas.graph.value_filter as vf
    # ret = oc.j.ValueHelper.entityToJson(val, oc.jmap())
    # jval = json.loads(ret)
    # model = oc.delegator.getModelEntity(val.getEntityName())
    # if filter:
    #     return vf.filter_json_val(model, jval)
    # return jval
    return ee.MetaEntity(val.getEntityName()).to_json(val, True, True)

def is_rel_one(val, relname):
    """
    # 1. null relation
    rv=val.getRelatedOne('InventoryItemType', False)
    print(is_rel_one(val, 'InventoryItemType'), rv)

    # 2. multiple relations
    rv=val.getRelated('ProductKeyword', None, None, False)
    print(is_rel_one(val, 'ProductKeyword'))
    print(json.dumps(to_json_list(rv), indent=2))

    :param val:
    :param relname:
    :return:
    """
    relation = val.getModelEntity().getRelation(relname)
    reltype=relation.getType()
    return reltype=='one' or reltype=='one-nofk'

def to_json_list(vals):
    import sagas.graph.value_filter as vf
    ret = oc.j.ValueHelper.valueListToJson(vals)
    jval = json.loads(ret)
    return jval

def rel_recs(val, rel_name, jsonifier=True):
    """
    import sagas.ofbiz.entities as ee
    ent=ee.entity('Product')
    val=ent.record('GZ-2002')
    rs=rel_recs(val, 'ProductKeyword')
    :param val:
    :param rel_name:
    :return:
    """
    rv = val.getRelated(rel_name, None, None, False)
    rs = []
    for el in rv:
        rs.append(to_json(el))
    if jsonifier:
        return(json.dumps(rs, indent=2))
    return rs

def get_rel_values(val, rel_name):
    if is_rel_one(val, rel_name):
        rv=val.getRelatedOne(rel_name, False)
        return to_json(rv)
    return rel_recs(val, rel_name)

def get_entity_relates(entity):
    ent = ee.entity(entity)
    rels = ent.rels
    rel_ents = set([str(fld.getRelEntityName()) for fld in rels])
    return(rel_ents)


def proc_rels(entity, key, rel):
    ent = ee.entity(entity)
    val = ent.record(key)
    rs = rel_recs(val, rel, False)
    print('total related recs:', len(rs))


def proc_entity(entity, key, rels):
    ent = ee.entity(entity)
    val = ent.record(key)
    ent_r = ent.to_json(val, True, True)
    for rel in rels:
        rs = rel_recs(val, rel, False)
        if len(rs) > 0:
            ent_r[rel] = rs
    return ent_r


def proc_entity_recs(entity):
    ent = ee.entity(entity)
    vals = ent.all()
    result = []
    for val in vals:
        ent_r = ent.to_json(val, True, True)
        rels = ent.get_rel_ent_names(False)
        for rel in rels:
            if is_rel_one(val, rel):
                rv = val.getRelatedOne(rel, False)
                if rv is not None:
                    ent_r[rel] = to_json(rv)
            else:
                rs = rel_recs(val, rel, False)
                if len(rs) > 0:
                    ent_r[rel] = rs
        result.append(ent_r)
    return result

class EntityGraphRels(object):
    def rels(self, entity, key, rel):
        """
        $ python -m sagas.ofbiz.entity_graph_relations rels Product 'GZ-2002' 'ProductKeyword'

        :param entity:
        :param key:
        :param rel:
        :return:
        """
        ent = ee.entity(entity)
        val = ent.record(key)
        rs = rel_recs(val, rel)
        print(rs)

    def entity_rels(self, entity):
        """
        $ python -m sagas.ofbiz.entity_graph_relations entity_rels Product
        :param entity:
        :return:
        """
        print(get_entity_relates(entity))

    def get_entity_global_ids(self):
        from sagas.ofbiz.entity_global_ref import EntityGlobalRef
        ent_ref = EntityGlobalRef('Survey')
        rs = ent_ref.fill_records('surveyId', 'description')
        [print(r[0], r) for r in rs]

    def write_recs(self, entity):
        """
        $ python -m sagas.ofbiz.entity_graph_relations write_recs 'Survey'
        $ python -m sagas.ofbiz.entity_graph_relations write_recs 'Example'
        :param entity:
        :return:
        """
        total = oc.delegator.findCountByCondition(entity, None, None, None)
        print('total records for %s: %d'%(entity, total))

        rs = proc_entity_recs(entity)
        # json_utils.write_json_to_file('./out/rs_Survey.json', rs)
        json_utils.write_json_to_file('./data/ofbiz/rs_%s.json'%entity, rs)
        print('done.')

if __name__ == '__main__':
    import fire
    fire.Fire(EntityGraphRels)

