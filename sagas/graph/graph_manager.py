import datetime
import json
import logging

import json_utils
from sagas.graph.dgraph_spacy import put_entities, put_chunks
from sagas.nlu.spacy_helper import get_lemmas, get_verb_lemmas
import pydgraph
import sagas.graph.dgraph_helper as helper
from tqdm import tqdm

logger = logging.getLogger('sagas_graph')

def create_client_stub():
    """
    Create a client stub.
    :return:
    """
    return pydgraph.DgraphClientStub('localhost:9080')

# Create a client.
def create_client(client_stub):
    return pydgraph.DgraphClient(client_stub)


# Drop All - discard all data and start from a clean slate.
def drop_all(client):
    return client.alter(pydgraph.Operation(drop_all=True))

def list_with_suffix(dir, suffix):
    import os
    rs=[]
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(suffix):
                rs.append(os.path.join(root, file))
    return rs

class GraphManager(object):
    def __init__(self):
        logger.info("connect dgraph server ...")
        self.client_stub = create_client_stub()
        self.client = create_client(self.client_stub)

    def reset_schema(self, schema):
        drop_all(self.client)
        return self.client.alter(pydgraph.Operation(schema=schema))

    def add_object(self, p):
        # Create a new transaction.
        txn = self.client.txn()
        try:
            # Run mutation.
            assigned = txn.mutate(set_obj=p)

            # Commit transaction.
            txn.commit()
            for uid in assigned.uids:
                print('{} => {}'.format(uid, assigned.uids[uid]))
            return assigned
        finally:
            # Clean up. Calling this after txn.commit() is a no-op
            # and hence safe.
            txn.discard()

    def remove_by_field(self, fld_name, fld_val):
        # Create a new transaction.
        txn = self.client.txn()
        try:
            query1 = """query all($a: string)
            {
               all(func: eq(%s, $a)) 
                {
                   uid
                }   
            }"""%(fld_name)
            variables1 = {'$a': fld_val}
            res1 = self.client.txn(read_only=True).query(query1, variables=variables1)
            ppl1 = json.loads(res1.json)
            for obj in ppl1['all']:
                assigned = txn.mutate(del_obj=obj)
                for uid in assigned.uids:
                    print('remove: {} => {}'.format(uid, assigned.uids[uid]))

            txn.commit()

        finally:
            txn.discard()

    def query(self, query, variables=None):
        res = self.client.txn(read_only=True).query(query, variables=variables)
        rs = json.loads(res.json)
        return rs


class GraphCommander(object):
    def __init__(self):
        # print('commander ...')
        self.gm= GraphManager()
        self.hanlp_client=None

    # @property
    def hanlp(self):
        from sagas.bots.hanlp_client import HanlpClient
        if self.hanlp_client is None:
            self.hanlp_client=HanlpClient()
        return self.hanlp_client

    def create_schema_stuff(self):
        schema = """
            name: string @index(exact) .
            friend: uid @reverse .
            age: int .
            married: bool .
            loc: geo .
            dob: datetime .
            """
        self.gm.reset_schema(schema)

    def create_data_stuff(self):
        # Create data.
        p = {
            'name': 'Alice',
            'age': 26,
            'married': True,
            'loc': {
                'type': 'Point',
                'coordinates': [1.1, 2],
            },
            'dob': datetime.datetime(1980, 1, 1, 23, 0, 0, 0).isoformat(),
            'friend': [
                {
                    'name': 'Bob',
                    'age': 24,
                },
                {
                    'name': 'Charlie',
                    'age': 29,
                }
            ],
            'school': [
                {
                    'name': 'Crown Public School',
                }
            ]
        }
        self.gm.add_object(p)

    def create_and_query_stuff(self):
        """
        $ python -m sagas.graph.graph_manager create-and-query-stuff
        :return:
        """
        self.create_schema_stuff()
        self.create_data_stuff()

        query = """{
          find_person(func: eq(name, "Alice")) {
            uid
            name
            age
          }
        }
        """
        rs=self.gm.query(query)
        print(json.dumps(rs, indent=True))

    def create_lang_feeds(self, tr='fr',
                          dataf = "/pi/ai/seq2seq/fra-eng-2019/fra.txt",
                          outf='./data/graph/fra_eng_feed.json',
                          parse_zh=False):
        """
        $ python -m sagas.graph.graph_manager create_lang_feeds
        $ python -m sagas.graph.graph_manager create_lang_feeds ja /pi/ai/seq2seq/jpn-eng-2019/jpn.txt ./data/graph/jpn_eng_feed.json
        :return:
        """
        from sagas.nlu.corpus_helper import filter_term, lines, divide_chunks
        import numpy
        import spacy

        logger.info('loading spacy english model ...')
        nlp_spacy = spacy.load('en_core_web_sm')
        print('loading corpus ...')
        pairs = lines(dataf)
        total = len(pairs)
        print('total', total)
        array = numpy.array(pairs)
        random_rows = numpy.random.randint(total, size=10)
        print('pickup', random_rows)
        print(array[random_rows, :])

        print('analyse ...')
        rows = array[random_rows, :]
        dataset = []
        for r in rows:
            sents=str(r[0])
            tr_lang=str(r[1].strip())
            props = {}
            props['sents@en']=sents
            props['sents@'+tr]=tr_lang

            doc = nlp_spacy(sents)
            props['lemmas'] = get_lemmas(doc)
            verbs=get_verb_lemmas(doc)
            if len(verbs)>0:
                props['verbs']=' '.join(verbs)
                props['verbs|count'] = len(verbs)
            put_entities(doc, props)
            put_chunks(doc, props)

            if parse_zh:
                # self.hanlp.put_deps(tr_lang, props)
                hanlp_c=self.hanlp()
                hanlp_c.put_deps(tr_lang, props)

            dataset.append(props)

        print(json.dumps(dataset, indent=2, ensure_ascii=False))

        print('write to json file %s ...'%outf)
        json_utils.write_json_to_file(outf, dataset)
        print('done.')

    def setup_lang_feeds(self):
        """
        $ python -m sagas.graph.graph_manager setup_lang_feeds
        :return:
        """
        print('.. setup schema')
        client = helper.reset('''
            name: string @index(exact, term) .
            nsubj: string @index(exact, term) .
            dobj: string @index(exact) .
            pobj: string @index(exact) .
            attr: string @index(exact) .
            sents: string @index(fulltext) @lang .
            lemmas: string @index(term) .
            verbs: string @index(term) .
            zh_SBV: string @index(term) @lang .
            zh_VOB: string @index(term) @lang .
        ''')
        files = list_with_suffix('data/graph', '_feed.json')
        for file in tqdm(files):
            feed_json = json_utils.read_json_file(file)
            _ = helper.set_json(client, feed_json)

    def query_lang(self, word):
        """
        $ python -m sagas.graph.graph_manager query_lang 'afraid'
        $ python -m sagas.graph.graph_manager query_lang 'want to'
        $ python -m sagas.graph.graph_manager query_lang 'want learn'
        :param word:
        :return:
        """
        vars = {'$a': word}
        helper.query_with_vars(self.gm.client, '''query data($a: string){
          data(func: allofterms(lemmas, $a)) {
            sents@en:.
            sents@fr
            sents@de
            sents@zh
            sents@ja
            sents@es
            nsubj @facets
            verbs    
          }
        }''', vars)

    def get_current_schema(self):
        """
        $ python -m sagas.graph.graph_manager get_current_schema
        :return:
        """
        import sagas.graph.dgraph_helper as helper
        client = helper.create_client()
        helper.run_q(client, '''schema {}
        ''')

if __name__ == '__main__':
    import fire
    logging.basicConfig(level=logging.INFO)
    fire.Fire(GraphCommander)
