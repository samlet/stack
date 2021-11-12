import json
from typing import Text, Any, Dict, List, Union, Optional

import io_utils
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
            ☑️ ️ 188
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

    def all_groups(self):
        """
        $ python -m sagas.ofbiz.secas all_groups
            ☑️ ️ 26
        :return:
        """
        from termcolor import colored

        services = oc.hubs.getComponent('services')
        groups = services.getServiceGroups()
        for g in groups:
            m = g.getModel()
            groupModel = g.getGroup()
            print(colored(m.getName(), attrs=["bold"]))
            print('\t', [(s.getName(), s.getMode()) for s in groupModel.getServices()])
        print("☑️ ️", len(groups))

    def get_secas(self, name, format=None):
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
            $ python -m sagas.ofbiz.secas get_secas setPaymentStatus json
        :param name:
        :return:
        """
        from termcolor import colored

        def null_print(*args, sep=' ', end='\n', file=None):
            pass

        output = print
        if format is not None:
            output = null_print
        else:
            output = print

        model = MetaService(name).model
        if model is None:
            output(f"No such service {name}")
            return
        default_ent = model.getDefaultEntityName()
        eventMap = oc.j.ServiceEcaUtil.getServiceEventMap(model.getName())
        if eventMap is None:
            output(f"Service {name} doesn't have secas")
            return
        output('➿ events', eventMap.keySet())
        ecas={}
        for key, evs in eventMap.items():
            indicator = indicators.get(key, "▶️")
            # output(key, evs.size())
            output(colored(f"{indicator}  {name} has {evs.size()} {key} events", attrs=["bold"]))
            rules=[]
            for ecaRule in evs:
                conds = [cond.getShortDisplayDescription(False) for cond in ecaRule.getEcaConditionList()]
                output("\t❓ conditions", colored(conds, "magenta", attrs=['underline']))
                acts = [(action.getServiceName(), action.getServiceMode()) for action in ecaRule.getEcaActionList()]
                output('\t➡️   ️️actions', acts)
                acts=[]
                for action in ecaRule.getEcaActionList():
                    desc=MetaService(action.getServiceName()).description
                    output('\t 〰️', colored(action.getServiceName(), "green", attrs=["bold", "reverse"]), ':',
                           colored(desc, "green"))
                    succ_srvs=secas_summary(action.getServiceName())
                    for succ_srv in succ_srvs:
                        output("\t\t", succ_srv)
                    acts.append({"serviceName": action.getServiceName(),
                                 "description": desc,
                                 "succSrvs": succ_srvs,
                                 })
                rules.append({"conditionList": conds,
                        "actionList": acts})
            ecas[key]=rules

        if format is not None:
            srv_meta= {"name": name,
                    "defaultEnt": default_ent,
                    "ecas": ecas
                    }
            cnt=json.dumps(srv_meta, ensure_ascii=False, indent=2)
            print(cnt)
            io_utils.write_to_file(f"/opt/asset/meta/services/{name}.json", cnt, True)

if __name__ == '__main__':
    import fire

    fire.Fire(Secas)
