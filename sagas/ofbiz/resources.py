from sagas.ofbiz.services import OfService as s, oc, track
import os
import io_utils
import xml.etree.ElementTree as ET
from resources_pb2 import RsResource, RsProperty, RsIndex, RsLookups, RsStrings

'''
Usage:
import sagas.ofbiz.resources as rs
rd=rs.ResourceDigester()
rd.lookup('产品')
'''

def property_json(prop_key, prop):
    rs={'key':prop_key}
    for key in prop.values.keys():
        if key not in ['zh-TW']:
            parts=key.split('-')
            rs['value@'+parts[0]]=prop.values[key]
    return rs

def properties_json(props):
    rs=[]
    for k,v in props.items():
        rs.append(property_json(k,v))
    return rs

class ResourceDigester(object):
    def __init__(self, verbose=True):
        self.verbose=verbose

    def process(self):
        oc.import_package('org.apache.ofbiz.base.component.ComponentConfig')
        allComponents = oc.j.ComponentConfig.getAllComponents()
        properties = {}
        for c in allComponents:
            conf_dir=c.getRootLocation()+'config'
            if os.path.isdir(conf_dir):
                files=io_utils.list_files(conf_dir)
                for f in files:
                    if f.endswith('.xml'):
                        self.parse_resource_file(f, properties)

        resource = RsResource(properties=properties)
        return resource

    def process_resource(self, xml_file):
        properties = {}
        self.parse_resource_file(xml_file, properties)
        resource = RsResource(properties=properties)
        return resource

    def parse_resource_file(self, xml_file, properties):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        if root.tag == 'resource':
            print('-', os.path.basename(xml_file))
            self.process_xml_file(xml_file, properties)

    def process_xml_file(self, xml_file, properties):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        # properties = {}
        for child in root:
            if child.tag == 'property':
                key = child.get('key')
                if self.verbose:
                    print(key, '⊕' ,os.path.basename(xml_file))
                props = {}
                for vnode in child:
                    # print(vnode.tag, vnode.attrib, vnode.get('{http://www.w3.org/XML/1998/namespace}lang'))
                    lang = vnode.get('{http://www.w3.org/XML/1998/namespace}lang')
                    textval=vnode.text
                    if self.verbose:
                        print('\t', vnode.tag, textval, lang)
                    if textval is not None and len(textval.strip())>0:
                        props[lang] = textval
                property = RsProperty(key=key, values=props, location=xml_file)
                if key in properties:
                    print('❣ the key %s has already exists' % key)
                properties[key] = property

    def get_index(self, lang, lookups):
        if lang in lookups:
            return lookups[lang]
        lookups[lang] = {}
        return lookups[lang]

    def build_index(self, resource:RsResource):
        lookups = {}
        for key, prop in resource.properties.items():
            # print(key, prop)
            for pname, pval in prop.values.items():
                index = self.get_index(pname, lookups)
                if pval in index:
                    index[pval].value.append(key)
                else:
                    index[pval] = RsStrings(value=[key])

        lookup_builder = {}
        for k, v in lookups.items():
            index = RsIndex(indexes=v)
            lookup_builder[k] = index

        rs_lookups = RsLookups(indexTable=lookup_builder)
        # print(rs_lookups)
        return rs_lookups

    def testing(self, word):
        """
        $ python -m sagas.ofbiz.resources testing 'Sagas应用程序'
        :param word:
        :return:
        """
        # resource=self.process()
        resource=self.process_resource(xml_file='data/i18n/SagasUiLabels.xml')
        rs_lookups=self.build_index(resource)
        zh = rs_lookups.indexTable['zh']
        # print(zh.indexes['Sagas应用程序'])
        print(word, "☞", zh.indexes[word])

    def build_all(self, word='Sagas应用程序', verbose=False):
        """
        $ python -m sagas.ofbiz.resources build_all 'Sagas应用程序'
        :param word:
        :param verbose:
        :return:
        """
        self.verbose=verbose
        resource = self.process()
        rs_lookups = self.build_index(resource)
        with open('./data/resources/labels_res.data', "wb") as f:
            f.write(resource.SerializeToString())
        with open('./data/resources/labels_index.data', "wb") as f:
            f.write(rs_lookups.SerializeToString())

        print('done.')

        # tests
        zh = rs_lookups.indexTable['zh']
        print(word, "☞", zh.indexes[word])

    def print_property(self, prop):
        from tabulate import tabulate
        # print all labels
        table_header = ['lang', 'value']
        table_data = []
        print('¤', prop.location)
        # print(prop.values['en'], ',', prop.values['zh'])
        for key in prop.values.keys():
            # print(key, '☈', prop.values[key])
            table_data.append((key, prop.values[key]))
        print(tabulate(table_data, headers=table_header, tablefmt='psql'))

    def lookup(self, word, lang='zh'):
        """
        $ python -m sagas.ofbiz.resources lookup 'Sagas应用程序'
        $ python -m sagas.ofbiz.resources lookup '产品'
        $ lookup Product en
        $ lookup CommonStatus key
        $ lookup EmplLeaveReasonType.description.CASUAL key
        :param word:
        :return:
        """
        resource, rs_lookups=read_resource()

        if lang=='key':
            prop = resource.properties[word]
            self.print_property(prop)
        else:
            lang_idx = rs_lookups.indexTable[lang]

            if word in lang_idx.indexes:
                keys = lang_idx.indexes[word]
                for key in keys.value:
                    print(word, "☞", key)
                    prop = resource.properties[key]

                    self.print_property(prop)
            else:
                print('the word %s is not exists in resources'%word)

    def get_all_properties(self):
        resource, _ = read_resource()
        return resource.properties

    def stats(self):
        from tabulate import tabulate

        resource, rs_lookups = read_resource()
        table_header = ['lang', 'total']
        table_data = []
        for index in rs_lookups.indexTable:
            lang_items = rs_lookups.indexTable[index]
            table_data.append((index, len(lang_items.indexes)))
        print(tabulate(table_data, headers=table_header, tablefmt='psql'))

    def label_json(self, label):
        """
        $ python -m sagas.ofbiz.resources label_json 'CommonStatus'
        $ python -m sagas.ofbiz.resources label_json 'CostComponentType.description.ACTUAL_LABOR_COST'
        :param label:
        :return:
        """
        import json
        props = self.get_all_properties()
        jval = json.dumps(property_json(label, props[label]),
                          indent=2, ensure_ascii=False)
        print(jval)

    def create_resources_data(self):
        """
        $ python -m sagas.ofbiz.resources create_resources_data
        :return:
        """
        import json_utils
        props = self.get_all_properties()
        json_utils.write_json_to_file(
            './data/labels/labels.json', properties_json(props))

def read_resource():
    import protobuf_utils
    rs_lookups = RsLookups()
    resource = RsResource()
    protobuf_utils.read_proto(rs_lookups, './data/resources/labels_index.data')
    protobuf_utils.read_proto(resource, './data/resources/labels_res.data')
    return resource, rs_lookups

if __name__ == '__main__':
    import fire
    fire.Fire(ResourceDigester)


