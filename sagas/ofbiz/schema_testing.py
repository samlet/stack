import json
import graphene
from sagas.ofbiz.schema_queries_g import *
from sagas.ofbiz.connector import OfbizConnector
from sagas.ofbiz.finder import Finder
from sagas.ofbiz.util import QueryHelper

oc=OfbizConnector()
finder=Finder(oc)
helper=QueryHelper(oc, finder)

class Query(graphene.ObjectType):
    testing = graphene.List(lambda: Testing)
    testing_node = graphene.List(lambda: TestingNode)

    def resolve_testing(self, info):
        entity_name = "Testing"
        recs = oc.all(entity_name)
        ent = oc.delegator.getModelEntity(entity_name)
        result = helper.fill_records(ent, Testing, recs)
        return result

    def resolve_testing_node(self, info):
        # print("query testing_node")
        entity_name = "TestingNode"
        recs = oc.all(entity_name)
        ent = oc.delegator.getModelEntity(entity_name)
        result = helper.fill_records(ent, TestingNode, recs)
        return result


schema = graphene.Schema(query=Query)

q1 = '''
{
  testing {
    testingId
    testingName
    testingTypeId
    testingType{
        lastUpdatedTxStamp
        description
    }
  }
}
'''.strip()
q2 = '''
{
  testingNode {
    testingNodeId
    testingNodeMember{
        testingNodeId
        testingId
    }
  }
}
'''.strip()


def clear_all():
    oc.delegator.removeAll("TestingNodeMember")
    oc.delegator.removeAll("TestingNode")
    oc.delegator.removeAll("Testing")
    oc.delegator.removeAll("TestingType")


def prepare():
    create = finder.create
    UtilDateTime = finder.oc.j.UtilDateTime
    nowTimestamp = finder.now()

    create("TestingType", "testingTypeId", "PERFOMFINDTEST")

    create("Testing", "testingId", "PERF_TEST_1", "testingTypeId", "PERFOMFINDTEST", "testingName", "nice name one")
    create("Testing", "testingId", "PERF_TEST_2", "testingTypeId", "PERFOMFINDTEST", "testingName",
           "nice other name two")
    create("Testing", "testingId", "PERF_TEST_3", "testingTypeId", "PERFOMFINDTEST", "testingName", "medium name three")
    create("Testing", "testingId", "PERF_TEST_4", "testingTypeId", "PERFOMFINDTEST", "testingName", "bad nme four")
    create("Testing", "testingId", "PERF_TEST_5", "testingTypeId", "PERFOMFINDTEST", "testingName", "nice name one")
    create("Testing", "testingId", "PERF_TEST_6", "testingTypeId", "PERFOMFINDTEST")
    create("Testing", "testingId", "PERF_TEST_7", "testingTypeId", "PERFOMFINDTEST")
    create("Testing", "testingId", "PERF_TEST_8", "testingTypeId", "PERFOMFINDTEST")
    create("Testing", "testingId", "PERF_TEST_9", "testingTypeId", "PERFOMFINDTEST")

    create("TestingNode", "testingNodeId", "NODE_1", "description", "Date Node")
    create("TestingNodeMember", "testingNodeId", "NODE_1", "testingId", "PERF_TEST_5",
           "fromDate", UtilDateTime.addDaysToTimestamp(nowTimestamp, 1),
           "thruDate", UtilDateTime.addDaysToTimestamp(nowTimestamp, 3),
           "extendFromDate", UtilDateTime.addDaysToTimestamp(nowTimestamp, -1),
           "extendThruDate", UtilDateTime.addDaysToTimestamp(nowTimestamp, 3))
    create("TestingNodeMember", "testingNodeId", "NODE_1", "testingId", "PERF_TEST_6",
           "fromDate", UtilDateTime.addDaysToTimestamp(nowTimestamp, -1),
           "thruDate", UtilDateTime.addDaysToTimestamp(nowTimestamp, 1),
           "extendFromDate", UtilDateTime.addDaysToTimestamp(nowTimestamp, -1),
           "extendThruDate", UtilDateTime.addDaysToTimestamp(nowTimestamp, 3))
    create("TestingNodeMember", "testingNodeId", "NODE_1", "testingId", "PERF_TEST_7",
           "fromDate", UtilDateTime.addDaysToTimestamp(nowTimestamp, -1),
           "thruDate", UtilDateTime.addDaysToTimestamp(nowTimestamp, 1),
           "extendFromDate", UtilDateTime.addDaysToTimestamp(nowTimestamp, -1),
           "extendThruDate", UtilDateTime.addDaysToTimestamp(nowTimestamp, 3))
    create("TestingNodeMember", "testingNodeId", "NODE_1", "testingId", "PERF_TEST_8",
           "fromDate", UtilDateTime.addDaysToTimestamp(nowTimestamp, -3),
           "thruDate", UtilDateTime.addDaysToTimestamp(nowTimestamp, 1),
           "extendFromDate", UtilDateTime.addDaysToTimestamp(nowTimestamp, -1),
           "extendThruDate", UtilDateTime.addDaysToTimestamp(nowTimestamp, 3))
    create("TestingNodeMember", "testingNodeId", "NODE_1", "testingId", "PERF_TEST_9",
           "fromDate", UtilDateTime.addDaysToTimestamp(nowTimestamp, -3),
           "thruDate", UtilDateTime.addDaysToTimestamp(nowTimestamp, -1),
           "extendFromDate", UtilDateTime.addDaysToTimestamp(nowTimestamp, -1),
           "extendThruDate", UtilDateTime.addDaysToTimestamp(nowTimestamp, -3))

if __name__ == '__main__':
    clear_all()
    prepare()

    result = schema.execute(q2)
    print(json.dumps(result.data, indent=2, ensure_ascii=False))
