# procs-ofbiz-rest-routines.md
+ find

{{ _.ofbiz_srvs }}/performFindList
    {
        "entityName":"Party",
        "viewIndex": 0,
        "viewSize": 10,
        "inputFields":{
            "partyTypeId": "PERSON" 
        }
    }
    $.data.list[*].partyId


