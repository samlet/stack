import logging

from py4j.java_gateway import JavaGateway, JavaObject, GatewayParameters
from py4j.java_gateway import java_import, get_field

logger = logging.getLogger(__name__)

class OfbizConnector(object):
    def __init__(self, host="localhost", port=22333, callback_port=22334):
        logger.info("connect to py4j-gateway %s %d"%(host, port))

        # self.gateway = JavaGateway()  # connect to the JVM
        self.gateway = JavaGateway(python_proxy_port=callback_port,
                                   gateway_parameters=GatewayParameters(address=host, port=port))
        self.delegator = self.gateway.entry_point.getDelegator()
        self.dispatcher=self.gateway.entry_point.getDispatcher()
        self.ctx= self.dispatcher.getDispatchContext()

        self.j = self.gateway.new_jvm_view()
        self.srv_rpc=None
        java_import(self.j, 'java.util.*')
        java_import(self.j, 'org.apache.ofbiz.base.util.*')
        java_import(self.j, 'com.sagas.generic.*')
        java_import(self.j, 'org.apache.ofbiz.entity.transaction.TransactionUtil')

    def import_package(self, pkg):
        java_import(self.j, pkg)

    def component(self, name):
        """
        Get a component: oc.component('entity_event_hub')
        :param name:
        :return:
        """
        return self.gateway.entry_point.getComponent(name)

    async def srv_connector(self):
        import asyncio
        from sagas.hybrid.srv_client import SrvClient

        loop = asyncio.get_event_loop()
        if self.srv_rpc is None:
            self.srv_rpc = await SrvClient(loop).connect()
        return self.srv_rpc

    def get(self, obj, attr):
        return get_field(obj, attr)
    def string_array(self, count, second_index=0):
        if second_index!=0:
            return self.gateway.new_array(self.gateway.jvm.java.lang.String,count, second_index)
        return self.gateway.new_array(self.gateway.jvm.java.lang.String, count)
    def int_array(self, count):
        int_class = self.gateway.jvm.int
        return self.gateway.new_array(int_class,count)

    def all(self, entity) -> JavaObject:
        return self.delegator.findAll(entity, False)

    def remove_all(self, entity):
        self.delegator.removeAll(entity)

    def create(self, entity, **kwargs) -> JavaObject:
        m = self.j.HashMap()
        for key, value in kwargs.items():
            m[key] = value
        return self.delegator.create(entity, m)

    def jmap(self, **kwargs) -> JavaObject:
        m = self.j.HashMap()
        for key, value in kwargs.items():
            m[key] = value
        return m

    def jlist(self, *args):
        m = self.j.ArrayList()
        for e in args:
            m.append(e)
        return m
    def jset(self, *args):
        s = self.j.HashSet()
        for e in args:
            s.add(e)
        return s

    def all_service_names(self):
        names = self.ctx.getAllServiceNames()
        return [str(v) for v in names]

    def service_model(self, service) -> JavaObject:
        s = self.ctx.getModelService(service)
        return s

    def call(self, service, **kwargs):
        ret = self.dispatcher.runSync(service, self.jmap(**kwargs))
        return ret

    def delete_table(self, entity_name):
        self.import_package('org.apache.ofbiz.entity.jdbc.*')

        group_name = self.delegator.getEntityGroupName(entity_name)
        helper_info = self.delegator.getGroupHelperInfo(group_name)

        msgs = self.jlist()
        util = self.j.DatabaseUtil(helper_info)
        ent = self.delegator.getModelEntity(entity_name)
        util.deleteTable(ent, msgs)
        if len(msgs) > 0:
            for msg in msgs:
                print(msg)
        else:
            print('ok')

    def has_entity(self, entity):
        return self.delegator.getModelEntity(entity) is not None
