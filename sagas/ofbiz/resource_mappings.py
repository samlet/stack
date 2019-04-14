from sagas.ofbiz.entities import OfEntity as e, oc, finder
from forms_pb2 import MetaForm, MetaMappingPackage, MetaFieldMapping, MetaFieldMappings, SUBMIT, RESET

hub=oc.component('entity_event_hub')
forms=oc.component('form_mgr')

def extract_key(original):
    return original.replace('${uiLabelMap.', '').replace('}', '').strip()

class ResourceMappings(object):
    def get_form(self, form_loc):
        # form_loc="component://content/widget/forum/BlogForms.xml;EditBlog;en_US"
        # form_loc='component://party/widget/partymgr/LookupForms.xml;LookupPartyName;en_US'
        # form_loc='component://party/widget/partymgr/LookupForms.xml;LookupPartyName;zh'
        form=forms.getMetaForm(form_loc)
        # print(form)
        return form

    def build_package(self, form_locs):
        package = {}

        for form_loc in form_locs:
            form=self.get_form(form_loc)
            py_form = MetaForm()
            form_data = form.toByteString().toByteArray()
            py_form.ParseFromString(form_data)

            for fld in py_form.fields:
                if fld.titleOriginal is not None and len(fld.titleOriginal) > 0 and fld.fieldType not in (SUBMIT, RESET):
                    key = extract_key(fld.titleOriginal)
                    # print(fld.name, '♯', fld.title, fld.titleOriginal, '♯', key)
                    mapping = MetaFieldMapping(key=key, fieldName=fld.name,
                                               fieldTitle=fld.title,
                                               fieldTitleOriginal=fld.titleOriginal,
                                               formUri=form_loc
                                               )
                    if key in package:
                        package[key].fields.append(mapping)
                        # print('+', package[key])
                    else:
                        # print('add', key)
                        package[key] = MetaFieldMappings(fields=[mapping])

        meta_package = MetaMappingPackage(mappings=package)
        # print(meta_package)
        return meta_package

    def testing(self):
        """
        $ python -m sagas.ofbiz.resource_mappings testing
        :return:
        """
        forms=['component://party/widget/partymgr/LookupForms.xml;LookupPartyName;zh']
        meta_package=self.build_package(forms)
        mapflds=meta_package.mappings['PartyLastName']
        for mapfld in mapflds.fields:
            print(mapfld.fieldName, mapfld.fieldTitle)

if __name__ == '__main__':
    import fire
    fire.Fire(ResourceMappings)
