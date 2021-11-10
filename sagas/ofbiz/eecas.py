from sagas.modules.deles import *

class Eecas(object):
    def all_eecas(self):
        """
        $ python -m sagas.ofbiz.eecas all_eecas
        :return:
        """
        models = oc.hubs.getComponent('models')
        rules = models.getEcaRules()
        ent_names=rules.keySet()
        print(ent_names, "☑️ ️", len(ent_names))

if __name__ == '__main__':
    import fire
    fire.Fire(Eecas)
