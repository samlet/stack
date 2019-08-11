# procs-ofbiz-groovy.md
+ procs-ofbiz-groovy.ipynb

## start
```python
from sagas.ofbiz.entities import format
loc="component://ecommerce/groovyScripts/order/ShipmentStatus.groovy"

ctx=oc.jmap(shipmentId="9996")
result_names=oc.j.HashSet()
result_names.add('context')

result=gd.exec(loc,None, ctx, result_names)

format(result['context']['shipment'])
for item in result['context']['shipmentItems']:
    format(item)
print(len(result['context']['orderShipmentInfoSummaryList']))
```

+ 列出所有装运的id:

```python
from sagas.ofbiz.entities import OfEntity as e
for shipment in e().listShipment():
    print(shipment['shipmentId'])
```

+ plugins/ecommerce/groovyScripts/order/ShipmentStatus.groovy

```js
import org.apache.ofbiz.base.util.UtilMisc
import org.apache.ofbiz.entity.Delegator
import org.apache.ofbiz.entity.*
import org.apache.ofbiz.entity.condition.*
import org.apache.ofbiz.entity.util.*

shipmentId = parameters.shipmentId
if (shipmentId) {
    shipment = from("Shipment").where("shipmentId", shipmentId).queryOne()
    shipmentItems = from("ShipmentItem").where("shipmentId", shipmentId).queryList()

    // get Shipment tracking info
    orderShipmentInfoSummaryList = select("shipmentId", "shipmentRouteSegmentId", "shipmentPackageSeqId", "carrierPartyId", "trackingCode")
                                    .from("OrderShipmentInfoSummary")
                                    .where("shipmentId", shipmentId)
                                    .orderBy("shipmentId", "shipmentRouteSegmentId", "shipmentPackageSeqId")
                                    .distinct()
                                    .queryList()

    context.shipment = shipment
    context.shipmentItems = shipmentItems
    context.orderShipmentInfoSummaryList = orderShipmentInfoSummaryList
}
```


