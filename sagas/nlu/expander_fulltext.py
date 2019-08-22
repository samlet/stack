import json

from sagas.nlu.expanders import DispatcherIntf, expand
from sagas.ofbiz.entities import OfEntity as e
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, STORED
from whoosh.qparser import QueryParser

pretty_json=lambda o: json.dumps(o, indent=2, ensure_ascii=False)

def addr(rec, fields):
    rs=[]
    for f in fields:
        if f in rec and rec[f] is not None:
            rs.append(rec[f])
    return ' ; '.join(rs)

def get_addresses(limit=20):
    rs=e('json').listPostalAddress(_limit=limit)
    return [(r['toName'], r, addr(r, ['postalCode', 'address1', 'address2', 'city', 'toName'])) for r in json.loads(rs)]

class IndexDispatcher(DispatcherIntf):
    def __init__(self, index_dir = 'data/indexes/address'):
        self.index_dir=index_dir
        self.ix = open_dir(index_dir)

    def print_r(self, results):
        for n, hit in enumerate(results):
            print(f"{n}.", hit["title"])
            print('\t', hit.highlights('content'))
            print('\t', hit['ref'])

    # def search_a(self, q):
    def execute(self, sents):
        with self.ix.searcher() as searcher:
            query = QueryParser("content", self.ix.schema).parse(sents)
            results = searcher.search(query)

            print('.. total hit', len(results))
            self.print_r(results)

class FullTextExpander(object):
    def list_addrs(self, jsonify=True):
        """
        $ python -m sagas.nlu.expander_fulltext list_addrs
        :param jsonify:
        :return:
        """
        import sagas
        if not jsonify:
            df=e('df').listPostalAddress()
            sagas.print_df(df)
        else:
            rs = e('json').listPostalAddress(_limit=2)
            print(pretty_json(json.loads(rs)))

    def create_index(self):
        """
        $ python -m sagas.nlu.expander_fulltext create_index
        :return:
        """
        index_dir = 'data/indexes/address'
        schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True), ref=STORED)
        ix = create_in(index_dir, schema)
        writer = ix.writer()

        for addr in get_addresses():
            writer.add_document(title=addr[0], content=addr[2], ref=addr[1])
        writer.commit()
        print('ok.')

    def query_index(self, q):
        """
        $ python -m sagas.nlu.expander_fulltext query_index Blvd
        $ python -m sagas.nlu.expander_fulltext query_index 'Industrial Park'
        $ python -m sagas.nlu.expander_fulltext query_index 'a industrial park'
        :param q:
        :return:
        """
        disp=IndexDispatcher()
        disp.execute(q)

    def expander(self):
        """
        $ python -m sagas.nlu.expander_fulltext expander
        :return:
        """
        disp=IndexDispatcher()
        texts = [('The city was the first to create an industrial park.', ['obj']),
                 ]
        for text in texts:
            data = {'lang': 'en', "sents": text[0]}
            expand(disp, data, keys=text[1], domains=['default'])
            print('✁', '-' * 30)

if __name__ == '__main__':
    import fire
    fire.Fire(FullTextExpander)

