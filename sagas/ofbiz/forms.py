import logging
import sys

from sagas.ofbiz.entities import OfEntity as e, oc, finder
from sagas.ofbiz.entity_prefabs import all_components
import os
import io_utils
from sagas.ofbiz.util import component_loc, norm_loc

logger = logging.getLogger(__name__)
# logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s',
#                      level=logging.DEBUG, stream=sys.stdout)

class FormResource(object):
    def __init__(self, comp, name, location):
        self.comp = comp
        self.name = name
        self.location = location
        self.uri=component_loc(location)
        self.unique_name=norm_loc(location)

        self.forms = []

class FormDescriptor(object):
    def __init__(self, tag, name, type, target, extends):
        self.tag = tag
        self.name = name
        self.type = type
        self.target = target
        self.extends = extends

# hub=oc.component('entity_event_hub')
# forms=oc.component('form_mgr')

def get_form_list():
    oc.import_package('org.apache.ofbiz.base.component.ComponentConfig')
    allComponents = oc.j.ComponentConfig.getAllComponents()

    form_list=[]
    for c in allComponents:
        # print(c.getRootLocation())
        widget_dir=c.getRootLocation()+"widget"
        if os.path.isdir(widget_dir):
            files=io_utils.list_files(widget_dir)
            logging.info(c.getGlobalName(), len(files))
            counts={'forms':0, 'screens':0, 'menus':0, 'trees':0, 'others':0}
            for f in files:
                base=os.path.basename(f)
                name=os.path.splitext(base)[0]
                if 'Form' in name:
                    counts['forms']=counts['forms']+1
                    form_list.append(FormResource(c.getGlobalName(), name, f))
                elif 'Screen' in name:
                    counts['screens']=counts['screens']+1
                elif 'Menu' in name:
                    counts['menus']=counts['menus']+1
                elif 'Tree' in name:
                    counts['trees']=counts['trees']+1
                elif name=='Theme':
                    pass
                else:
                    counts['others']=counts['others']+1
                    logging.info('** get unexpected file type %s', name)
            logging.debug('\t%s', counts)

    logging.info("total form files %d", len(form_list))
    return form_list

def collect_forms(form_list, verbose=True):
    import xml.etree.ElementTree as ET

    total = 0
    # key is form's name, value is FormResource list;
    # each FormResource contains a FormDescriptor list
    form_index = {}
    for form_res in form_list:
        tree = ET.parse(form_res.location)
        root = tree.getroot()
        # print(root.tag)
        if root.tag=='{http://ofbiz.apache.org/Widget-Form}forms':
            for child in root:
                # tag, name, type, target
                form_name=child.get('name')
                if child.tag=='{http://ofbiz.apache.org/Widget-Form}grid':
                    form_name='@'+form_name
                    if verbose:
                        print('-> find a grid', form_name)
                elif child.tag=='{http://ofbiz.apache.org/Widget-Form}form':
                    pass
                else:
                    raise ValueError("cannot process tag", child.tag, '; in', form_res.location)

                # print(child.tag, form_name)
                fd = FormDescriptor(child.tag, form_name,
                                    child.get('type'),
                                    child.get('target'),
                                    child.get('extends')
                                    )
                form_res.forms.append(fd)
                if fd.name not in form_index:
                    form_index[fd.name] = [form_res]
                else:
                    form_index[fd.name].append(form_res)
                    logging.debug('duplicate form name %s, extends -> %s' % (fd.name, fd.extends))
                total = total + 1

    logging.info("total forms %d", total)
    return form_index

def print_form(form):
    import json
    print(form.name, form.location)
    # print(form.forms)
    printstr = json.dumps(form, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
    print(printstr)

def print_form_locations(form_index, form_name):
    locs = form_index[form_name]
    for loc in locs:
        print('✎', loc.name, loc.location, loc.uri)

def render_form(form_name, locale='zh_CN', params=None, proto=False):
    form_list = get_form_list()
    form_index = collect_forms(form_list)
    print_form_locations(form_index, form_name)

    forms = oc.component('form_mgr')
    locs = form_index[form_name]
    for loc in locs:
        result=forms.renderFormData(form_name, loc.uri, locale, params)
        print('-------------------- ✁', loc.unique_name)
        print(result.getRepr())
        if proto:
            print(result.getFormData())

        print('uri:', loc.uri+";"+form_name+";"+locale)


def contains_loc(locs, name_filter):
    if name_filter is None:
        return True

    for loc in locs:
        if name_filter in loc.name:
            return True
    return False

def print_form_list(name_filter=None):
    form_list = get_form_list()
    form_index = collect_forms(form_list)
    count=0
    for k,locs in form_index.items():
        if contains_loc(locs, name_filter):
            count=count+1
            print('♥', count, k)
            for loc in locs:
                print('\t✎', loc.name, loc.location, loc.uri)

def get_form_locs():
    form_list = get_form_list()
    form_index = collect_forms(form_list)
    print("total forms:", len(form_index.items()))

    forms = []
    for k, locs in form_index.items():
        for loc in locs:
            # loc.name, loc.location, loc.uri
            form_loc = loc.uri + ';' + k + ';zh_CN'
            forms.append(form_loc)
    return forms

def get_form_meta(form_name, locale='zh_CN'):
    form_list = get_form_list()
    form_index = collect_forms(form_list)
    forms = oc.component('form_mgr')
    locs = form_index[form_name]
    meta_list=[]
    for loc in locs:
        location=loc.uri+";"+form_name+";"+locale
        meta=forms.getMetaForm(location)
        meta_list.append(meta)

    return meta_list


if __name__ == '__main__':

    # form_name='AddTimesheetEntry'
    # form_name = 'AddForumMessage'
    # form_name='EditCombo'
    render_form('EditCombo')



