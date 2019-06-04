from sagas.ofbiz.forms import get_form_locs
from sagas.ofbiz.entities import OfEntity as e, oc, finder
import forms_pb2 as fo
import protobuf_utils as pu

def extract_services(form_locs):
    services = oc.all_service_names()
    forms = oc.component('form_mgr')

    form_services=[]
    form_reqs=[]
    for form_loc in form_locs:
        form=forms.getMetaForm(form_loc)
        if len(form.getTarget())>0:
            target=form.getTarget()
            if target in services:
                form_services.append((form.getName(), target))
            else:
                form_reqs.append((form.getName(), target))
    return form_services, form_reqs

def read_services_index():
    fs = fo.MetaFormServices()
    pu.read_proto(fs, 'data/resources/form_services.data')
    return fs.formServices

def retrieve_title():
    import sagas.ofbiz.forms as fo
    from sagas.ofbiz.resources import read_resource

    form_list = fo.get_form_list()
    form_index = fo.collect_forms(form_list, False)
    resource, rs_lookups = read_resource()

    has_titles=[]
    no_titles=[]
    for form_name in form_index.keys():
        form_title="PageTitle"+form_name
        if form_title in resource.properties:
            has_titles.append(form_name)
        else:
            # print('not found title for form %s'%form_name)
            no_titles.append(form_name)
    return has_titles, no_titles

def convert_form_name(form_name):
    """
    Usage: convert_form_name('EditAgreementItem')
    :param form_name:
    :return: like 'Edit Agreement Item'
    """
    from sagas.util.str_converters import to_camel_case, to_snake_case, to_words
    return to_words(to_snake_case(form_name), True)

class FormServices(object):
    def __init__(self):
        self.services_index=read_services_index()
        self.lookups={}
        # tuple[1] is service name, tuple[0] is form name
        for tuple in self.services_index:
            tv=tuple.values
            if tv[1] not in self.lookups:
                self.lookups[tv[1]]=[]
            self.lookups[tv[1]].append(tv[0])

    def get_service_forms(self, service):
        if service in self.lookups:
            return self.lookups[service]
        return None

    def service_forms(self, service):
        """
        $ python -m sagas.ofbiz.form_services service_forms createPortalPage
        :param service:
        :return:
        """
        forms=self.get_service_forms(service)
        if forms is not None:
            print(forms)
        else:
            print('no forms found.')

    def count_forms_title(self):
        """
        $ python -m sagas.ofbiz.form_services count_forms_title
        :return:
        """
        # print(len(form_index.keys()))
        has_titles, no_titles = retrieve_title()
        print('has title:', len(has_titles))
        print('no title:', len(no_titles))

    def build_form_services_index(self):
        """
        $ python -m sagas.ofbiz.form_services build_form_services_index
        :return:
        """
        # form_locs=['component://webtools/widget/ServiceForms.xml;AddJobManagerLock;zh_CN']
        form_locs = get_form_locs()
        form_services, form_reqs = extract_services(form_locs)
        print('form_services', len(form_services))
        print('form_reqs', len(form_reqs))
        print(form_reqs[:5])
        print(form_services[:5])

        folist = []
        frlist = []
        for item in form_services:
            folist.append(fo.MetaTuple(values=item))
        for item in form_reqs:
            frlist.append(fo.MetaTuple(values=item))
        fs = fo.MetaFormServices(formServices=folist, formRequests=frlist)
        pu.write_proto_to(fs, 'data/resources/form_services.data')
        print('done')

if __name__ == '__main__':
    import fire
    fire.Fire(FormServices)

