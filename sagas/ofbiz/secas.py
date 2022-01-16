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


def get_define_loc(model) -> str:
    loc=model.getDefinitionLocation()
    return loc[loc.find('ofbiz-framework/')+len('ofbiz-framework/'):]

def filter_params(model, prec):
    params = [{"name": param.getName(),
               "type": param.getType(),
               "required": not param.isOptional(),
               "overrideOptional": param.isOverrideOptional(),
               "entity": param.getEntityName(),
               "mode": param.getMode(),
               "formDisplay": param.isFormDisplay(),
               "formLabel": param.getFormLabel(),
               "internal": param.isInternal()
               } for param in model.getModelParamList()
              if prec(param.getMode())]
    params = [p for p in params if not p['internal']]
    return list({v['name']: v for v in params}.values())

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

    def abi(self, service):
        """
        $ python service_meta.py abi createPerson
        :param service:
        :return:
        """
        # from sagas.util.str_converters import to_camel_case
        model = MetaService(service).model
        service_def = {
            "name": service,
            # "className": to_camel_case(service, True),
            "className": service[0].capitalize()+service[1:],
            "description": model.getDescription(),
            'defaultEntity': model.getDefaultEntityName(),
            'engine': model.getEngineName(),
            "paramsInput": filter_params(model, lambda m: m == "IN" or m == "INOUT"),
            "paramsOutput": filter_params(model, lambda m: m == "OUT" or m == "INOUT")
        }

        return service_def

    def write_all_srvs(self):
        """
        $ python -m sagas.ofbiz.secas write_all_srvs
        :return:
        """
        services = oc.all_service_names()
        total=len(services)
        for i, serv_name in enumerate(services):
            self.get_secas(serv_name, 'json')
            print(f"{i}/{total}", serv_name)
        print(f'write all ok, total {total}')

    def get_secas(self, name, format=None, target_file=None):
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

        define_loc = get_define_loc(model)
        output('* define-loc', define_loc)
        output('* impl-loc', model.getLocation())

        ecas = {}

        eventMap = oc.j.ServiceEcaUtil.getServiceEventMap(model.getName())
        if eventMap is None:
            output(f"Service {name} doesn't have secas")
            # return
        else:
            output('➿ events', eventMap.keySet())

            for key, evs in eventMap.items():
                indicator = indicators.get(key, "▶️")
                # output(key, evs.size())
                output(colored(f"{indicator}  {name} has {evs.size()} {key} events", attrs=["bold"]))
                rules = []
                for ecaRule in evs:
                    conds = [cond.getShortDisplayDescription(False) for cond in ecaRule.getEcaConditionList()]
                    output("\t❓ conditions", colored(conds, "magenta", attrs=['underline']))
                    acts = [(action.getServiceName(), action.getServiceMode()) for action in ecaRule.getEcaActionList()]
                    output('\t➡️   ️️actions', acts)
                    acts = []
                    for action in ecaRule.getEcaActionList():
                        desc = MetaService(action.getServiceName()).description
                        output('\t 〰️', colored(action.getServiceName(), "green", attrs=["bold", "reverse"]), ':',
                               colored(desc, "green"))
                        succ_srvs = secas_summary(action.getServiceName())
                        for succ_srv in succ_srvs:
                            output("\t\t", succ_srv)
                        acts.append({"serviceName": action.getServiceName(),
                                     "description": desc,
                                     "succSrvs": succ_srvs,
                                     })
                    rules.append({"conditionList": conds,
                                  "actionList": acts})
                ecas[key] = rules

        if format is not None:
            srv_meta = {"name": name,
                        "defaultEnt": default_ent,
                        'defineLoc': define_loc,
                        'implLoc': model.getLocation(),
                        'abi': self.abi(name),
                        "ecas": ecas
                        }
            cnt = json.dumps(srv_meta, ensure_ascii=False, indent=2)
            # print(cnt)

            if target_file is None:
                parts = define_loc.split('/')
                # as: 'accounting/services_payment'
                sub_dir=parts[1]+"/"+parts[-1].replace('.xml','')
                prefix='/opt/app/hubs-common/asset/services'
                target_file=f"{prefix}/{sub_dir}/{name}.json"

            io_utils.write_to_file(target_file, cnt, True)


if __name__ == '__main__':
    import fire

    fire.Fire(Secas)
