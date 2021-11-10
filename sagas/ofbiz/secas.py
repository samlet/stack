from typing import Text, Any, Dict, List, Union, Optional
from sagas.modules.deles import *

oc.import_package('org.apache.ofbiz.service.eca.ServiceEcaUtil')
oc.import_package('com.bluecc.triggers.Hubs')

indicators = {
    "commit": "✅",
    "return": "⤴️",
    "invoke": "↘️",
    "in-validate": "☑️",
}

def secas_summary(name) -> List[str]:
    model = MetaService(name).model
    if model is None:
        print(f"No such service {name}")
        return []
    eventMap = oc.j.ServiceEcaUtil.getServiceEventMap(model.getName())
    if eventMap is None:
        return []
    summary = []
    for key, evs in eventMap.items():
        indicator = indicators.get(key, "▶️")
        summary.append(f"{indicator}  {name} has {evs.size()} {key} events")
    return summary

class Secas(object):
    def all_secas(self):
        """
        $ python -m sagas.ofbiz.secas all_secas
        $ python -m sagas.ofbiz.secas all_secas | grep -i payment
        $ python -m sagas.ofbiz.secas all_secas | grep -i inventory | xargs -I {} python -m sagas.ofbiz.secas get_secas {}
        :return:
        """
        services = oc.hubs.getComponent('services')
        ecas = services.getEcaRules()
        for cas in ecas.keySet():
            print(cas)
        # print(ecas.keySet(), "☑️ ️", len(ecas.keySet()))
        print("☑️ ️", len(ecas.keySet()))

    def get_secas(self, name):
        """
        ## order
            $ python -m sagas.ofbiz.secas get_secas storeOrder
            $ python -m sagas.ofbiz.secas get_secas receiveInventoryProduct
            $ python -m sagas.ofbiz.secas get_secas changeOrderStatus
        ## product
            $ python -m sagas.ofbiz.secas get_secas createProductContent
                $ python -m sagas.ofbiz.secas get_secas createContent
        ## shipment
            $ python -m sagas.ofbiz.secas get_secas updateShipment
        ## payment
            $ python -m sagas.ofbiz.secas get_secas setPaymentStatus
            $ python -m sagas.ofbiz.secas get_secas setFinAccountTransStatus

        :param name:
        :return:
        """
        from termcolor import colored

        model = MetaService(name).model
        if model is None:
            print(f"No such service {name}")
            return
        default_ent = model.getDefaultEntityName()
        eventMap = oc.j.ServiceEcaUtil.getServiceEventMap(model.getName())
        if eventMap is None:
            print(f"Service {name} doesn't have secas")
            return
        print('➿ events', eventMap.keySet())
        for key, evs in eventMap.items():
            indicator = indicators.get(key, "▶️")
            # print(key, evs.size())
            print(colored(f"{indicator}  {name} has {evs.size()} {key} events", attrs=["bold"]))
            for ecaRule in evs:
                conds = [cond.getShortDisplayDescription(False) for cond in ecaRule.getEcaConditionList()]
                print("\t❓ conditions", colored(conds, "magenta", attrs=['underline']))
                acts = [(action.getServiceName(), action.getServiceMode()) for action in ecaRule.getEcaActionList()]
                print('\t➡️   ️️actions', acts)
                for action in ecaRule.getEcaActionList():
                    print('\t 〰️', colored(action.getServiceName(), "green", attrs=["bold", "reverse"]), ':',
                          colored(MetaService(action.getServiceName()).description, "green"))
                    for succ_srv in secas_summary(action.getServiceName()):
                        print("\t\t", succ_srv)


if __name__ == '__main__':
    import fire

    fire.Fire(Secas)
