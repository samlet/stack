from sagas.modules.deles import *

oc.import_package('org.apache.ofbiz.service.eca.ServiceEcaUtil')

class Secas(object):
    def get_secas(self, name):
        """
        $ python -m sagas.ofbiz.secas get_secas storeOrder
        :param name:
        :return:
        """
        model = MetaService(name).model
        default_ent = model.getDefaultEntityName()
        eventMap = oc.j.ServiceEcaUtil.getServiceEventMap(model.getName())
        print('➿ events', eventMap.keySet())
        for key, evs in eventMap.items():
            # print(key, evs.size())
            print(f"{name} has {evs.size()} {key} events")
            for ecaRule in evs:
                conds=[cond.getShortDisplayDescription(False) for cond in ecaRule.getEcaConditionList()]
                print("\t❓ conditions", conds)
                acts=[(action.getServiceName(), action.getServiceMode()) for action in ecaRule.getEcaActionList()]
                print('\t➡️   ️️actions', acts)
                for action in ecaRule.getEcaActionList():
                    print('\t 〰️', action.getServiceName(), ':', MetaService(action.getServiceName()).description)

if __name__ == '__main__':
    import fire
    fire.Fire(Secas)
