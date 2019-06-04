from sagas.ofbiz.entities import OfEntity as e, oc, MetaEntity, all_entities
import resources_pb2 as res
import protobuf_utils

def build_field_index(ents):
    field_index={}
    for ent_name in ents:
        ent=MetaEntity(ent_name)
        if not oc.j.Utils.isViewEntity(ent.model):
            for fld in ent.model.getFieldsIterator():
                if not fld.getIsAutoCreatedInternal():
                    fld_name=fld.getName()
                    if fld_name not in field_index:
                        field_index[fld_name]=[ent_name]
                    else:
                        field_index[fld_name].append(ent_name)
    return field_index

class EntityMetaIndexer(object):
    def __init__(self):
        self.rs=None
        self.resource=None
        self.rs_lookups=None

    def build_samples(self):
        ents=['Person', 'Party']
        result=build_field_index(ents)
        print(result)

    def build(self):
        """
        $ python -m sagas.ofbiz.entity_meta_indexer build
        :return:
        """
        ents = all_entities()
        idx = build_field_index(ents)
        print('total fields:', len(idx))

        idx_b = {}
        for k, v in idx.items():
            idx_b[k] = res.RsEntityReference(entities=v)
        rs = res.RsEntities(fieldRefs=idx_b)
        protobuf_utils.write_proto_to(rs, 'data/resources/entities_index.data')

        print('total field-refs:', len(rs.fieldRefs))

    def init_rs(self):
        from sagas.ofbiz.resources import read_resource

        target = 'data/resources/entities_index.data'
        self.rs = res.RsEntities()
        protobuf_utils.read_proto(self.rs, target)

        print('total field-refs:', len(self.rs.fieldRefs))
        # print(rs.fieldRefs['lastName'])

        self.resource, self.rs_lookups = read_resource()

    def is_field(self, qname):
        if self.rs is None: self.init_rs()
        return qname in self.rs.fieldRefs

    def is_description(self, word, lang='zh'):
        if self.rs is None: self.init_rs()
        lang_idx = self.rs_lookups.indexTable[lang]

        if word in lang_idx.indexes:
            keys = lang_idx.indexes[word]
            for key in keys.value:
                # print(word, "☞", key)
                if '.description.' in key:
                    return True
        return False

    def testing(self):
        """
        $ python -m sagas.ofbiz.entity_meta_indexer testing
        :return:
        """
        lang = 'zh'
        word = '会员'
        print('会员(zh) is a type description?', self.is_description(word, lang))

        print('lastName is field?', self.is_field('lastName'))
        print('fakeName is field?', self.is_field('fakeName'))

if __name__ == '__main__':
    import fire
    fire.Fire(EntityMetaIndexer)
