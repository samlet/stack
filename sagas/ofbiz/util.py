from sagas.util.str_converters import to_camel_case, to_snake_case
import graphene

class ModelBase(graphene.ObjectType):
    def __init__(self, helper, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper=helper

class QueryHelper(object):
    def __init__(self, oc, finder):
        self.oc=oc
        self.finder=finder

    def fill_record(self, model, val, rec):
        names=model.getAllFieldNames()
        for field_name in names:
            setattr(val, to_snake_case(field_name), rec[field_name])
    def create_list(self, *args):
        m = self.oc.j.ArrayList()
        for e in args:
            m.append(e)
        return m

    def get_related_one(self, entity, of_type, **kwargs):
        model=self.oc.delegator.getModelEntity(entity)
        rec=self.finder.find_one(entity, self.oc.jmap(**kwargs))
        instance=of_type(self)
        self.fill_record(model, instance, rec)
        return instance

    def get_relations(self, entity, of_type, **kwargs):
        model=self.oc.delegator.getModelEntity(entity)
        fields=self.oc.jmap(**kwargs)
        orders=self.create_list()
        recs=self.oc.delegator.findByAnd(entity, fields, orders, True)
        result=[]
        for rec in recs:
            val=of_type(self)
            self.fill_record(model, val, rec)
            result.append(val)
        return result

    def fill_records(self, model, of_type, recs):
        result=[]
        for rec in recs:
            val=of_type(self)
            self.fill_record(model, val, rec)
            result.append(val)
        return result

    def input_to_dictionary(self, input, entity, of_type):
        output = of_type(self)
        m = self.oc.j.HashMap()
        for key in input:
            value = input[key]
            setattr(output, key, value)
            m[to_camel_case(key)] = value
        val = self.oc.delegator.create(entity, m)
        # print(to_snake_case('lastUpdatedStamp'), val['lastUpdatedStamp'], val)
        setattr(output, "last_updated_stamp", val['lastUpdatedStamp'])
        return output


def print_table(obj, *args):
    """
    Usage:
        from sagas.ofbiz.util import print_table
        model=s('model').createProductReview
        print_table(model, 'location')

    :param obj:
    :param args:
    :return:
    """
    from py4j.java_gateway import get_field
    from tabulate import tabulate

    table_header = ['name', 'value']
    table_data = []
    for arg in args:
         table_data.append((arg, get_field(obj, arg)))
    print(tabulate(table_data, headers=table_header, tablefmt='psql'))


def norm_loc(loc):
    pkg_prefixes = ['ofbiz-framework/applications',
                    'ofbiz-framework/framework',
                    'ofbiz-framework/plugins']
    for pkg_prefix in pkg_prefixes:
        idx = loc.find(pkg_prefix)
        if idx != -1:
            return loc[idx + len(pkg_prefix) + 1:].replace('servicedef/', '').replace('widget/', '').replace('.xml', '').replace('/',
                                                                                                          '_').lower()
    raise ValueError('Cannot normalize the location ' + loc)


def component_loc(loc):
    prefix="component://"
    pkg_prefixes = ['ofbiz-framework/applications',
                    'ofbiz-framework/framework',
                    'ofbiz-framework/plugins']
    for pkg_prefix in pkg_prefixes:
        idx = loc.find(pkg_prefix)
        if idx != -1:
            return prefix+loc[idx + len(pkg_prefix) + 1:]
    raise ValueError('Cannot normalize the location ' + loc)

