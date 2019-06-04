from sagas.ofbiz.entities import oc,finder,OfEntity as e

class Contents(object):
    def search_entity(self, name_filter):
        name_filter=name_filter.lower()
        model_reader=oc.delegator.getModelReader()
        names=model_reader.getEntityNames()
        # print(len(names))
        for name in names:
            if name_filter in name.lower():
                print(name)

    def tests(self):
        self.search_entity('web')

## procs-ofbiz-content.ipynb

if __name__ == '__main__':
    import fire
    fire.Fire(Contents)
