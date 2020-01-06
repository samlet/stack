from sagas.ofbiz.runtime_context import platform
from py4j.java_gateway import get_field
from sagas.util.string_util import abbrev
import json

oc=platform.oc
finder=platform.finder

oc.import_package('org.apache.ofbiz.service.ServiceDispatcher')
oc.import_package('java.math.BigDecimal')
oc.import_package('java.sql.Timestamp')

class OfService(object):
    """
    from sagas.ofbiz.entities import oc, finder, OfEntity, MetaEntity
    from sagas.ofbiz.services import OfService, MetaService

    product=MetaEntity("Product").record("GZ-2002")
    ok, ret=OfService().calculateProductPrice(product=product)
    print(ret['defaultPrice'], ret['listPrice'])

    ----

    from sagas.ofbiz.services import OfService as s
    from sagas.ofbiz.entities import OfEntity as e
    import sagas.ofbiz.entities as ee

    ok, result=s().calculateProductPrice(product=e().refProduct('GZ-2002'))
    ee.format(result)

    # show the service meta as a dataframe
    s('meta').calculateProductPrice
    """
    # _oc=platform.oc
    _name = None
    _fields = {}  # {field: field object}

    def __init__(self, operator=None, show_internal=False):
        super(OfService, self).__init__()
        self.operator=operator
        self.show_internal=show_internal

    def __getattr__(self, method):
        """Provide a dynamic access to a service method."""
        if method.startswith('_'):
            return super(OfService, self).__getattr__(method)

        if self.operator is not None:
            if self.operator=='meta':
                return create_service_data_frame(method, self.show_internal)
            elif self.operator=='model':
                return oc.service_model(method)

        def service_method(*args, **kwargs):
            """Return the result of the service request."""

            # check args with runSync/runSyncIgnore/...
            params = oc.jmap(**kwargs)
            if "userLogin" not in kwargs:
                params.put('userLogin', finder.user)
            result = oc.dispatcher.runSync(method, params)
            ok = oc.j.ServiceUtil.isSuccess(result)
            if not ok:
                err = oc.j.ServiceUtil.getErrorMessage(result)
            return ok, result

        async def hybrid_method(*args, **kwargs):
            ctx=kwargs
            ctx['_service']=method
            json_pars = json.dumps(ctx)
            rpc=await oc.srv_connector()
            response = await rpc.call(json_pars)
            result=json.loads(response)
            ok=result["_result"]==0

            return ok, result

        if self.operator=='srv':
            return hybrid_method
        else:
            return service_method

    def __repr__(self):
        return "MetaService(%r)" % (self._name)


class MetaService(object):
    def __init__(self, name):
        self.name = name
        self.model = oc.service_model(name)

    @property
    def parameters(self):
        return self.model.getAllParamNames()

    @property
    def inputs(self):
        return self.model.getInParamNames()

    @property
    def outputs(self):
        return self.model.getOutParamNames()

    @property
    def location(self):
        return get_field(self.model, "location")

    @property
    def invoke_method(self):
        return get_field(self.model, "invoke")

    @property
    def interfaces(self):
        return get_field(self.model, "implServices")

    @property
    def default_entity(self):
        return get_field(self.model, "defaultEntityName")

    def desc(self, show_internal=True):
        from tabulate import tabulate

        print(self.name, self.location, self.invoke_method)
        for intf in self.interfaces:
            print(intf)
        print("default entity: ", self.default_entity)

        table_header = ['name', 'type', 'entity', 'mode', 'description']
        table_data = []
        params = self.model.getModelParamList()
        for param in params:
            p_name = get_field(param, "name")
            p_type = get_field(param, "type")
            p_entity = get_field(param, "entityName")
            p_mode = get_field(param, "mode")
            p_desc = get_field(param, "description")

            optional = get_field(param, "optional")
            internal = get_field(param, "internal")

            if internal and not show_internal:
                continue

            if p_desc is None:
                p_desc = " "
            if not optional:
                p_desc = "* " + p_desc
            if internal:
                p_desc = "@ " + p_desc

            table_data.append((abbrev(p_name, 15),
                               abbrev(p_type, 10), p_entity, p_mode,
                               abbrev(p_desc, 20)))

        print(tabulate(table_data, headers=table_header, tablefmt='psql'))


def create_service_data_frame(name, show_internal=False):
    import pandas as pd
    model=MetaService(name).model
    params=model.getModelParamList()
    model_desc={'name':[str(get_field(param, "name")) for param in params],
                'type':[str(get_field(param, "type")) for param in params],
                'required': ['*' if not get_field(param, "optional") else ' '  for param in params],
                'override optional': ['*' if not get_field(param, "overrideOptional") else ' ' for param in params],
                'entity name': [str(get_field(param, "entityName")) for param in params],
                'mode':[str(get_field(param, "mode")) for param in params],
                'internal': ['*' if get_field(param, "internal") else ' '  for param in params],
                'description':[str(get_field(param, "description")) for param in params]
               }
    df = pd.DataFrame(model_desc)
    # df['parameter mode']=df['mode'].astype('category')
    if not show_internal:
        df=df[df['internal']!='*']
    # return df.sort_values(by='parameter mode')
    return df

def track_services(filter_by=0):
    log=oc.j.ServiceDispatcher.getServiceLogMap()
    for rs,value in log.items():
        if rs.getStartStamp().getTime()>=filter_by:
            print('✔', oc.get(rs.getModelService(), 'name'),
                  rs.getLocalName(), rs.getMode(),
                  rs.getStartStamp(), '➷',
                  rs.getEndStamp().getTime()-rs.getStartStamp().getTime(), 'ms')

def track(fn):
    """
    Usage: ok,r=track(lambda a: s().testScv(defaultValue=5.5, message="hello world"))
    :param fn:
    :return:
    """
    now=oc.j.System.currentTimeMillis()
    ret=fn(now)
    # print(ret)
    track_services(now)
    return ret

def search_service(name_filter):
    name_filter=name_filter.lower()
    services=oc.all_service_names()
    result=[]
    for name in services:
        if name_filter in name.lower():
            result.append(name)
    return result


