from bs4 import BeautifulSoup

from client_wrapper import ServiceClient
import services_common_pb2 as sc
import services_common_pb2_grpc as sc_service
from values_pb2 import TaStringEntries, TaStringEntriesBatch

import sagas.ofbiz.entities as ee
from sagas.util.date_time_util import *

def parse_product(text, verbose=True):
    soup = BeautifulSoup(text, 'html.parser')
    props=[]
    images=[]
    for c in soup:
        if verbose:
            print(c.name,'~', c)
        if c.string is not None and len(c.string.strip())>0:
            if verbose:
                print('\t@', c.string)
            props.append(c.string)
    if verbose:
        print('** find images')
    imgs=soup.find_all('img')
    for img in imgs:
        if verbose:
            print(img)
            print('\t', img['src'])
        images.append(img['src'])
    return props, images

def map_list(a):
    b = {a[i]: a[i+1] for i in range(0, len(a), 2)}
    return b

def get_product_attrs(entry):
    text=entry['summary']
    props, images=parse_product(text, verbose=False)
    return {**map_list(props), 'image':images[0]}

def extract_id(id):
    """
    id="https://umall.vip.qq.com/v2/?_wv=1025&_wwv=4&product=32482&path=/product/33154"
    extract_id(id)
    :param id:
    :return:
    """
    prefix='&path='
    return id[id.index(prefix)+len(prefix):]

def filter_entity(entity_name, props, pickups):
    values={}
    for p in pickups:
        if p in props:
            values[p]=str(props[p])
    record=TaStringEntries(entityName=entity_name, values=values)
    return record

def load_rss_seed(json_file='./data/rss/westore_new.json'):
    import json_utils
    rss_doc = json_utils.read_json_file(json_file)
    # rss_doc['title']
    product_set = []
    for entry in rss_doc['entry']:
        # print(entry["title@zh"], entry['published'])
        data = {}
        data['productName'] = entry["title@zh"]
        data['createdDate'] = now_jdbc()
        data['lastModifiedDate'] = now_jdbc()
        data['fromDate'] = to_jdbc(entry['published'])
        data['isVirtual'] = 'N'
        data['productTypeId'] = "FINISHED_GOOD"
        data['productId'] = extract_id(entry['id'])

        data['productPricePurposeId'] = "PURCHASE"
        data['productPriceTypeId']="DEFAULT_PRICE"
        data['productStoreGroupId']="Test_group"

        data['priceDetailText']=entry['summary']

        attrs = get_product_attrs(entry)
        if "价格:" in attrs:
            data['price'] = float(attrs['价格:'].strip().replace('元', ''))
            data['currencyUomId'] = 'CNY'
        if "image" in attrs:
            data['largeImageUrl'] = attrs['image']
        product_set.append(data)

    # print(json.dumps(product_set, indent=2, ensure_ascii=False))
    return product_set

class ProductData(object):
    def persist_seed(self, json_file='./data/rss/westore_new.json',
                     only_first=False):
        """
        $ python -m sagas.ofbiz.product.product_data persist_seed
        :return:
        """
        import json

        product_set=load_rss_seed(json_file=json_file)
        print(json.dumps(product_set, indent=2, ensure_ascii=False))
        rs=[]
        if only_first:
            print('filtering [Product] ...')
            ent = ee.entity('Product')
            rec=filter_entity('Product', product_set[0], ent.field_names)
            print(rec)
            rs=[rec]
        else:
            for ent_name in ['Product','ProductPrice']:
                ent = ee.entity(ent_name)
                print('filtering [%s] ...'%ent_name)
                for prod in product_set:
                    rec = filter_entity('Product', prod, ent.field_names)
                    rs.append(rec)

        batch = TaStringEntriesBatch(records=rs)
        serv = ee.get_serv()
        ret = serv.StoreAll(batch)
        print(ret)

if __name__ == '__main__':
    import fire
    fire.Fire(ProductData)

