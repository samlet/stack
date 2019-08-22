from sagas.ofbiz.services import OfService as s, oc, track
from sagas.ofbiz.entities import OfEntity as e
from py4j.java_gateway import get_field
import os
import xml.etree.ElementTree as ET
import json
from sagas.util.name_util import to_global_id, from_global_id
from values_pb2 import TaStringEntries, TaStringEntriesBatch, TaStringEntriesMap, TaRecordset, TaIdBag


class EntityPrefabs(object):
    def __init__(self):
        self.skip_documents=[]

    def collect_component_data_files(self):
        oc.import_package('org.apache.ofbiz.base.component.ComponentConfig')
        allComponents = oc.j.ComponentConfig.getAllComponents()
        index = 1
        self.comp_files = {}
        for c in allComponents:
            self.comp_files[c.getGlobalName()] = []
        for c in allComponents:
            # print(index, c.getComponentName(), c.getRootLocation())
            # print(index, c.getGlobalName(), c.getRootLocation())
            index = index + 1
            ts = c.getTestSuiteInfos()
            # print('\t', 'contains test suites', len(ts))
            ent_res = c.getEntityResourceInfos()
            for es in ent_res:
                data_type = get_field(es, 'type')
                if data_type == 'data':
                    # print('\t', data_type, get_field(es, 'readerName'),
                    #      es.getLocation())
                    self.comp_files[c.getGlobalName()].append(c.getRootLocation() + es.getLocation())
        return self.comp_files


    def get_data_root(self, component, group_name):
        files=self.comp_files[component]
        for f in files:
            base=os.path.basename(f)
            name=os.path.splitext(base)[0]
            if name==group_name:
                # print(name, f)
                tree = ET.parse(f)
                root = tree.getroot()
                return root
        return None

    def to_kv(self, entity_name, values, record_format='json'):
        model=oc.delegator.getModelEntity(entity_name)
        if model is None:
            raise ValueError('Entity model %s is absent'%entity_name)

        pks=model.getPkFieldNames()
        id_parts=[]
        # values=dict(attrib)
        for pk in pks:
            val=values.get(pk)
            id_parts.append(val)

        # generate global id
        id_cnt='▫'.join(id_parts)
        token=to_global_id(entity_name, id_cnt)
        record=""
        if record_format=='protobuf':
            record=TaStringEntries(entityName=entity_name, values=values)
        else:
            record=json.dumps(values)
        return id_cnt, token, record

    def convert_to_record_set(self, root):
        # record_set = {}
        record_set=[]
        ids=[] # preserve the record order
        for child in root:
            if child.tag not in ('delete', 'create', 'create-replace', 'create-update'):
                values=dict(child.attrib)
                for cc in child:
                    # print('\t--', cc.tag, cc.text)
                    values[cc.tag]=cc.text
                id_cnt, token, record = self.to_kv(child.tag, values, "protobuf")
                # print(id_cnt, token, record)
                # record_set[token]=record
                record_set.append((token,record))
                ids.append(token)
        # return TaStringEntriesMap(entries=record_set), ids
        # print("++++++++++", record_set)
        # print("++++++++++")
        return record_set, ids

    def persist_component_data(self, component):
        files=self.comp_files[component]
        groups={}
        rs_map={}
        for f in files:
            print('.. proc %s'%f)
            base=os.path.basename(f)
            group_name=os.path.splitext(base)[0]
            tree = ET.parse(f)
            root = tree.getroot()
            if root.tag!='entity-engine-xml':
                self.skip_documents.append(f)
            else:
                rs, ids = self.convert_to_record_set(root)
                groups[group_name]=TaIdBag(ids=ids)
                # rs_map.update(rs.entries)
                # for k,v in rs.items():
                for item in rs:
                    rs_map[item[0]]=item[1]
                # rs_map.update(rs)

        rs_bag = TaRecordset(recordGroups=groups)
        return rs_bag, rs_map

def all_components():
    prefabs = EntityPrefabs()
    prefabs.collect_component_data_files()
    for c in prefabs.comp_files:
        print(c)

class EntityPersister(object):
    def persist_group(self, component, group_name):
        """
        persist_group('ofbizDemo', 'OfbizDemoDemoData')
        :return:
        """
        prefabs = EntityPrefabs()
        prefabs.collect_component_data_files()
        root=prefabs.get_data_root(component, group_name)
        rs, ids=prefabs.convert_to_record_set(root)
        print(rs)
        print(ids)

    def persist_component(self, comp_name):
        prefabs = EntityPrefabs()
        prefabs.collect_component_data_files()

        # comp_name = 'ofbizDemo'
        rs_bag, rs_map = prefabs.persist_component_data(comp_name)
        print(rs_bag)
        # print(rs_map)

        # entity index persistent group by component
        with open('./data/prefabs/' + comp_name + '.data', "wb") as f:
            f.write(rs_bag.SerializeToString())

        # entity data all in one
        rs_all=TaStringEntriesMap(entries=rs_map)
        with open('./data/prefabs/entities.data', "wb") as f:
            f.write(rs_all.SerializeToString())

        print('--> print some samples')
        val=rs_all.entries['U2VjdXJpdHlHcm91cFBlcm1pc3Npb246U1VQRVLilqtPRkJJWkRFTU9fQURNSU7ilqsyMDAxLTA1LTEzIDEyOjAwOjAwLjA=']
        print(val)

        print('--> print some samples')
        val = rs_all.entries[
            'U2VjdXJpdHlQZXJtaXNzaW9uOk9GQklaREVNT19DUkVBVEU=']
        print(val)

        print('done')

    def persist_all(self):
        prefabs = EntityPrefabs()
        prefabs.collect_component_data_files()

        rs_map={}
        for comp_name in prefabs.comp_files:
            # comp_name = 'ofbizDemo'
            rs_bag, rs = prefabs.persist_component_data(comp_name)
            rs_map.update(rs)  # add all records into rs_map

            print(rs_bag)
            # entity index persistent group by component
            with open('./data/prefabs/' + comp_name + '.data', "wb") as f:
                f.write(rs_bag.SerializeToString())

        # entity data all in one
        rs_all=TaStringEntriesMap(entries=rs_map)
        with open('./data/prefabs/_entities.data', "wb") as f:
            f.write(rs_all.SerializeToString())

        print('.. skip documents:')
        for doc in prefabs.skip_documents:
            print('-', doc)
        print('done')

    # def disp_prefab(self, id):
    def list_data(self, item='entities'):
        """
        $ ls data/prefabs/
        # list samples
            $ python -m sagas.ofbiz.entity_prefabs list_data entities
        # list all data
            $ python -m sagas.ofbiz.entity_prefabs list_data _entities
        :param item:
        :return:
        """
        from values_pb2 import TaStringEntries, TaStringEntriesBatch, TaStringEntriesMap
        with open(f'data/prefabs/{item}.data', 'rb') as f:
            es = TaStringEntriesMap()
            es.ParseFromString(f.read())
            print(es)

if __name__ == '__main__':
    # all_components()
    # pr=EntityPersister()
    # pr.persist_group('ofbizDemo', 'OfbizDemoDemoData')

    import fire
    fire.Fire(EntityPersister)

