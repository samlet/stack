import org.apache.ofbiz.base.util.UtilDateTime
import org.apache.ofbiz.base.util.UtilProperties
import org.apache.ofbiz.entity.GenericValue
import org.apache.ofbiz.entity.util.EntityUtil
import org.apache.ofbiz.service.ServiceUtil

import java.sql.Timestamp

//Generic fonction to resolve a rate amount from a pk field
def getRatesAmountsFrom(String field) {
    String entityName = null
    if (field == 'workEffortId') entityName = 'WorkEffort'
    if (field == 'partyId') entityName = 'Party'
    if (field == 'emplPositionTypeId') entityName = 'EmplPositionType'

    Map condition = [rateTypeId: parameters.rateTypeId,
                     periodTypeId: parameters.periodTypeId,
                     rateCurrencyUomId: parameters.rateCurrencyUomId]
    condition.put(field, parameters.get(field))
    List ratesList = from('RateAmount').where(condition).filterByDate().queryList()
    if (!ratesList) {
        GenericValue periodType = from('PeriodType').where(parameters).queryOne()
        GenericValue rateType = from('RateType').where(parameters).queryOne()
        GenericValue partyNameView = from('PartyNameView').where(parameters).queryOne()
        logError('A valid rate entry could be found for rateType:' + rateType.description + ', ' + entityName + ':' + parameters.get(field)
                + ', party: ' + partyNameView.lastName + partyNameView.middleName + partyNameView.firstName + partyNameView.groupName
                + ' However.....not for the period:' + periodType.description + ' and currency:' + parameters.rateCurrencyUomId)
    }
    Map result = success()
    result.ratesList = ratesList
    return result
}

// Get all the rateAmount for a given workEffortId
def getRatesAmountsFromWorkEffortId() {
    return getRatesAmountsFrom('workEffortId')
}
// Get all the rateAmount for a given partyId
def getRatesAmountsFromPartyId() {
    return getRatesAmountsFrom('partyId')
}
// Get all the rateAmount for a given emplPositionTypeId
def getRatesAmountsFromEmplPositionTypeId() {
    return getRatesAmountsFrom('emplPositionTypeId')
}

