from sagas.util.name_util import to_global_id, from_global_id
from sagas.ofbiz.entities import oc
# import sagas.ofbiz.entities as ee

def ensure(val, fld):
    r=val.get(fld)
    if r is None:
        return ""
    return r

class EntityGlobalRef(object):
    def __init__(self, entity):
        # entity='ProductType'
        self.entity=entity
        self.model=oc.delegator.getModelEntity(entity)
        self.pks=[]
        for fld in self.model.getPkFieldNames():
            self.pks.append(fld)

    def get_gid(self, value):
        pk_vals=[]
        for pk in self.pks:
            # pk_vals.append(value.get(pk))
            pk_vals.append(value.getString(pk))
        gid=to_global_id(self.entity, '♡'.join(pk_vals))
        return gid

    def get_record(self, gid):
        params = oc.jmap()
        t, idstring = from_global_id(gid)
        ids = idstring.split('♡')
        mapped = zip(self.pks, ids)
        ctx = list(mapped)
        for el in ctx:
            params.put(el[0], el[1])
        result = oc.delegator.findOne(self.entity, params, True)
        return result

    def fill_records(self, name_fld, desc_fld):
        """
        Fill records with specific entity values
        :param name_fld: the name field
        :param desc_fld: the parameter is a field name or a field list
        :return:
        """
        # Cannot do a find that returns an EntityListIterator with no transaction in place.
        # Wrap this call in a transaction.
        began_transaction = oc.j.TransactionUtil.begin()
        iter = oc.delegator.find(self.entity, None, None, None, None, None)
        rs=[]

        # while iter.hasNext():
        # For performance reasons do not use the EntityListIterator.hasNext() method,
        # just call next() until it returns null; see JavaDoc comments in the
        # EntityListIterator class for details and an example
        val = iter.next()
        while val is not None:
            desc_val=''
            if isinstance(desc_fld, list):
                desc_val=' '.join([ensure(val,fld) for fld in desc_fld])
            else:
                desc_val=val.get(desc_fld)
            rs.append((self.get_gid(val), val.get(name_fld), desc_val))
            val = iter.next()
        iter.close()
        oc.j.TransactionUtil.commit(began_transaction)

        return rs

    def write_dataset(self, target_file, name_fld, desc_fld):
        """
        write_dataset('data/resources/rs_product_type.data')
        :param target_file:
        :return:
        """
        import protobuf_utils as pu
        from values_pb2 import ExternalLinks, ExternalLink

        result_st={}

        rs = self.fill_records(name_fld, desc_fld)
        links = []
        for rec in rs:
            link = ExternalLink(gid=rec[0], name=rec[1], description=rec[2])
            links.append(link)
        links_rs = ExternalLinks(links=links)
        result_st['links_count']=len(links)
        pu.write_proto_to(links_rs, target_file)
        return result_st, rs[:5]


class EntityDatasetBuilder(object):
    def print_table(self, samples):
        from tabulate import tabulate
        table_header = ['gid', 'name', 'description']
        print(tabulate(samples, headers=table_header, tablefmt='psql'))

    def product_type(self):
        """
        $ python -m sagas.ofbiz.entity_global_ref product_type
        :return:
        """
        ent_ref = EntityGlobalRef('ProductType')
        st, samples=ent_ref.write_dataset('data/resources/rs_product_type.data',
                              'productTypeId', 'description')
        print(st)
        self.print_table(samples)
        print('ok')

    def product(self):
        """
        $ python -m sagas.ofbiz.entity_global_ref product
        :return:
        """
        ent_ref = EntityGlobalRef('Product')
        st, samples=ent_ref.write_dataset('data/resources/rs_product.data',
                              'productId', 'productName')
        print(st)
        self.print_table(samples)
        print('ok')

    def person(self):
        """
        $ python -m sagas.ofbiz.entity_global_ref person
        :return:
        """
        ent_ref = EntityGlobalRef('Person')
        st, samples=ent_ref.write_dataset('data/resources/rs_person.data',
                              'partyId', ['lastName', 'firstName'])
        print(st)
        self.print_table(samples)
        print('ok')

    def all(self):
        """
        $ python -m sagas.ofbiz.entity_global_ref all
        :return:
        """
        self.product_type()
        self.product()
        self.person()

if __name__ == '__main__':
    import fire
    fire.Fire(EntityDatasetBuilder)
