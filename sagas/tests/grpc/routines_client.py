import services_common_pb2 as sc
import services_common_pb2_grpc as sc_service
from client_wrapper import ServiceClient

serv = ServiceClient(sc_service, 'EntityServantStub', 'localhost', 50051)

def a_query():
    q=sc.InfoQuery(queryItems=[""])
    names=serv.GetEntityNames(q)
    print(names)

def a_store():
    from values_pb2 import TaStringEntries, TaStringEntriesBatch
    from sagas.util.string_util import abbrev
    import xml.etree.ElementTree as ET
    from sagas.ofbiz.entity_prefabs import EntityPrefabs
    xml_file = '/pi/stack/data/product/ProductPriceTestData.xml'
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ep = EntityPrefabs()
    record_set, ids = ep.convert_to_record_set(root)

    rs = []
    for item in record_set:
        rs.append(item[1])
        print(item[1].entityName)  # TaStringEntries
        print('\t', abbrev(item[0]))
    batch = TaStringEntriesBatch(records=rs)
    ret=serv.StoreAll(batch)
    print(ret)

if __name__ == '__main__':
    a_query()
    a_store()
