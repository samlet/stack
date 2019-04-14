import json
from sagas.ofbiz.services import OfService as s, oc, track
from sagas.ofbiz.entities import OfEntity as e

def createProductionRun(**kwargs):
    ctx=oc.jmap(**kwargs)
    json_pars=oc.j.ValueHelper.mapToJson(ctx)

    srv=oc.j.ServiceInvoker(oc.dispatcher, oc.delegator, "createProductionRun", json_pars)
    ret=srv.invoke()
    print(ret, ret.getID())
    json_r=srv.getJsonResult()
    print(json.dumps(json.loads(json_r), indent=2))

class ManufacturingProcs(object):
    def create_demo_run(self):
        admin = e().refUserLogin('TestManufAdmin')

        productId='PROD_MANUF'
        facilityId='WebStoreWarehouse'
        # quantity=oc.j.BigDecimal(5.0)
        quantity=5.0
        # productionRunStartDate=DateTime.now_timestamp()
        productionRunStartDate="2019-02-26 02:12:01.785642"
        createProductionRun(userLogin=admin,
            productId=productId,
            pRQuantity=quantity,
            startDate=productionRunStartDate,
            facilityId=facilityId)

if __name__ == '__main__':
    # import fire
    # fire.Fire(ManufacturingProcs)
    ManufacturingProcs().create_demo_run()

