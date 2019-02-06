import sagas.ofbiz.connector
from py4j.java_gateway import java_import

class Finder(object):
    def __init__(self, oc):
        self.oc=oc

        java_import(oc.j, 'org.apache.ofbiz.service.ServiceUtil')
        java_import(oc.j, 'org.apache.ofbiz.base.util.UtilDateTime')
        java_import(oc.j, 'org.apache.ofbiz.entity.util.*')

        self.user=self.default_user()

    def success(self, ret):
        return self.oc.j.ServiceUtil.isSuccess(ret)

    def hash_map(self, *args):
        arg_len = len(args)
        if arg_len % 2 == 1:
            raise ValueError("You must pass an even sized array to the toMap method (size = " + str(arg_len) + ")")

        m = self.oc.j.HashMap()
        i = 0
        while i < arg_len:
            m[args[i]] = args[i + 1]
            i = i + 2
        return m

    def default_user(self):
        return self.oc.gateway.getUserLogin()

    def find(self, entity, inputs):
        # inputs=oc.jmap(testingId="PERF_TEST_1")
        ret = self.oc.call("performFind", userLogin=self.user, entityName=entity, inputFields=inputs)
        if self.oc.j.ServiceUtil.isSuccess(ret):
            listIt = ret['listIt']
            foundElements = listIt.getCompleteList()
            return (True, foundElements)
        else:
            return (False, self.oc.j.ServiceUtil.getErrorMessage(ret))

    def find_one(self, entity, params):
        return self.oc.delegator.findOne(entity, params, True)

    def find_list(self, entity, limit=20, offset=0):
        findOptions = self.oc.j.EntityFindOptions()
        findOptions.setLimit(limit)
        findOptions.setOffset(offset)
        rows = self.oc.delegator.findList(entity, None, None, None, findOptions, False)
        return rows

    def now(self):
        UtilDateTime = self.oc.j.UtilDateTime
        nowTimestamp = UtilDateTime.nowTimestamp()
        return nowTimestamp

    def create(self, entity, *args):
        # print(hash_map(*args))
        return self.oc.delegator.create(entity, self.hash_map(*args))

