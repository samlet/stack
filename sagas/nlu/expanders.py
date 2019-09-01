import json
import numpy as np
import struct
import redis
import json_utils

pretty_json=lambda o: json.dumps(o, indent=2, ensure_ascii=False)

def property_json(prop_key, prop):
    rs={'key':prop_key, 'values':{}}
    for key in prop.values.keys():
        if key not in ['zh-TW']:
            parts=key.split('-')
            rs['values'][parts[0]]=prop.values[key]
    return rs

def save_docs(doc_vecs, file):
    print(len(doc_vecs))
    np.save(file, doc_vecs)  # save

def to_redis(r,a,n):
    """Store given Numpy array 'a' in Redis under key 'n'"""
    h, w = a.shape
    shape = struct.pack('>II',h,w)
    encoded = shape + a.tobytes()

    # Store encoded data in Redis
    r.set(n,encoded)
    return

def from_redis(r,n):
    """Retrieve Numpy array from Redis key 'n'"""
    encoded = r.get(n)
    if encoded is None:
        return None
    h, w = struct.unpack('>II',encoded[:8])
    print(f"h:{h}, w:{w}")
    a = np.frombuffer(encoded, dtype=np.float32, offset=8).reshape(h,w)
    return a

class BertManager(object):
    def __init__(self):
        from sagas.conf.conf import cf
        self.ipaddr=cf.conf['bert_servant']
        print(f".. bert service port is {self.ipaddr}")
        self._bc=None
        # self.topk = 5
        self.topk = 2
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    @property
    def bc(self):
        from bert_serving.client import BertClient
        if self._bc is None:
            self._bc = BertClient(ip=self.ipaddr)
        return self._bc

    def do_test(self):
        """
        >>> bm=BertManager()
        >>> bm.do_test()
        """
        result=self.bc.encode(['First do it', 'then do it right', 'then do it better'])
        print(result)

    def get_similar(self, questions, doc_vecs, query):
        from termcolor import colored

        va = from_redis(self.r, query)
        if va is None:
            va = self.bc.encode([query])
            to_redis(self.r, va, query)

        query_vec = va[0]
        score = np.sum(query_vec * doc_vecs, axis=1) / np.linalg.norm(doc_vecs, axis=1)
        topk_idx = np.argsort(score)[::-1][:self.topk]
        print('top %d sentences similar to "%s"' % (self.topk, colored(query, 'green')))
        result=[]
        for idx in topk_idx:
            row = questions[idx]
            qs = colored(row, 'yellow')
            print('> %s\t%s %s' % (colored('%.1f' % score[idx], 'cyan'), row['key'], qs))
            result.append(row)
        return result

def pickups(key, prop, langs):
    rs=[]
    for k,v in prop.values.items():
        if k in langs:
            rs.append({'key':key, 'lang':k, 'value':v})
    return rs

from sagas.nlu.inspector_fixtures import InspectorFixture
from sagas.nlu.inspector_common import Context
import abc

class DispatcherIntf(abc.ABC):
    @abc.abstractmethod
    def execute(self, sents):
        pass

class BertDispatcher(DispatcherIntf):
    def __init__(self, feat_name):
        self.arranger = json_utils.read_json_file("./data/feats/%s.json" % feat_name)
        self.doc_vecs = np.load("./data/feats/%s.npy" % feat_name)  # load
        self.bm = BertManager()

    def execute(self, sents):
        return self.bm.get_similar(self.arranger, self.doc_vecs, sents)

def expand(dispathcer:DispatcherIntf, data, keys, specific_domains):
    fixt=InspectorFixture()
    domains, meta=fixt.request_domains(data)
    ctx=Context(meta, domains)
    for key in keys:
        for chunk in ctx.chunk_pieces(key):
            dispathcer.execute(chunk)

class Expanders(object):
    def query_property(self, label):
        from sagas.ofbiz.resources import ResourceDigester
        rd = ResourceDigester(True)
        props = rd.get_all_properties()
        # label = 'CostComponentType.description.ACTUAL_LABOR_COST'
        rs=property_json(label, props[label])
        print(pretty_json(rs))

    def build(self, feat_name, location_matcher):
        """
        $ python -m sagas.nlu.expanders build samples 'ProductEntityLabels.xml'
        :param feat_name:
        :param location_matcher:
        :return:
        """
        from os import path
        from sagas.ofbiz.resources import ResourceDigester

        outf = "./data/feats/%s.npy" % feat_name
        if path.exists(outf):
            print(f"Target file {outf} has already exists, exit.")
            return

        rd = ResourceDigester(True)
        props = rd.get_all_properties()
        if location_matcher=='*':
            labels = [k for k, v in props.items()]
        else:
            labels = [k for k, v in props.items() if v.location.endswith(location_matcher)]

        print('total', len(labels))

        arranger = []
        for label in labels:
            arranger.extend(pickups(label, props[label], ['de', 'fr']))
        print(len(arranger))

        bm = BertManager()
        doc_vecs = bm.bc.encode([row['value'] for row in arranger])
        print(len(doc_vecs), doc_vecs[:2])

        # feat_name = 'samples'
        save_docs(doc_vecs, outf)
        meta_outf = "./data/feats/%s.json" % feat_name
        json_utils.write_json_to_file(meta_outf, arranger)

    def similar(self, feat_name, sents):
        """
        $ python -m sagas.nlu.expanders similar samples 'Charge périodique'
        :param feat_name:
        :param sents:
        :return:
        """
        arranger=json_utils.read_json_file("./data/feats/%s.json" % feat_name)
        doc_vecs = np.load("./data/feats/%s.npy" % feat_name)  # load
        bm = BertManager()
        # 'Charge périodique'
        bm.get_similar(arranger, doc_vecs, sents)

    def expander(self, feat_name='samples'):
        """
        $ python -m sagas.nlu.expanders expander
        :return:
        """
        disp=BertDispatcher(feat_name)
        texts = [('Shenzhen ist das Silicon Valley für Hardware-Firmen', ['nmod']),
                 ('Ich stimme dir in diesem Punkt nicht zu.', ['obl']),
                 ('Die Nutzung der Seite ist kostenlos.', ['nsubj']),
                 ]
        for text in texts:
            data = {'lang': 'de', "sents": text[0]}
            expand(disp, data, keys=text[1], specific_domains=['default'])
            print('✁', '-' * 30)

if __name__ == '__main__':
    import fire
    fire.Fire(Expanders)
