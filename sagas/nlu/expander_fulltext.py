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

def get_samples_ja():
    return [("First document", "/a", "このたんごのいみをおぼえてください"),
            ("Second document", "/b", "彼女を呼びます。")
            ]

def get_samples_zh():
    return [("first test-document", "/c", "This is the document for test, 水果和米饭."),
            ("test-document-2", "/d", "This is the document for test, 水果和大蒜.")
            ]

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
    def __init__(self):
        from jieba.analyse import ChineseAnalyzer
        from sagas.ja.whoosh.MeCabTokenizer import MeCabTokenizer
        # zh: procs-whoosh.ipynb
        # ja: procs-whoosh-ja.ipynb
        self.analyzers={'zh':lambda : ChineseAnalyzer(),
                        'ja': lambda : MeCabTokenizer(),
                        }
        self.sources={'address':lambda limit=20: get_addresses(limit),
                      "samples_ja": lambda : get_samples_ja(),
                      "samples_zh": lambda : get_samples_zh(),
                      }

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

    def create_index(self, source='address', lang=None):
        """
        $ python -m sagas.nlu.expander_fulltext create_index
        $ python -m sagas.nlu.expander_fulltext create_index samples_ja ja
        $ python -m sagas.nlu.expander_fulltext create_index samples_zh zh
        :return:
        """
        import os
        index_dir = f'data/indexes/{source}'
        if not os.path.exists(index_dir):
            os.mkdir(index_dir)

        if lang is not None and lang in self.analyzers:
            tk=self.analyzers[lang]()
            schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True, analyzer=tk), ref=STORED)
        else:
            schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True), ref=STORED)

        ix = create_in(index_dir, schema)
        writer = ix.writer()

        for rec in self.sources[source]():
            writer.add_document(title=rec[0], content=rec[2], ref=rec[1])
        writer.commit()
        print('ok.')

    def query_index(self, q, source='address'):
        """
        $ python -m sagas.nlu.expander_fulltext query_index Blvd
        $ python -m sagas.nlu.expander_fulltext query_index 'Industrial Park'
        $ python -m sagas.nlu.expander_fulltext query_index 'a industrial park'
        $ python -m sagas.nlu.expander_fulltext query_index "呼び" samples_ja
        $ python -m sagas.nlu.expander_fulltext query_index "大蒜" samples_zh
        :param q:
        :return:
        """
        disp=IndexDispatcher(index_dir = f"data/indexes/{source}")
        disp.execute(q)

    def expander(self, source='address'):
        """
        $ python -m sagas.nlu.expander_fulltext expander
        :return:
        """
        disp=IndexDispatcher(index_dir = f"data/indexes/{source}")
        texts = [('The city was the first to create an industrial park.', ['obj'], 'en'),
                 ]
        for text in texts:
            data = {'lang': text[2], "sents": text[0]}
            expand(disp, data, keys=text[1], specific_domains=['default'])
            print('✁', '-' * 30)

if __name__ == '__main__':
    import fire
    fire.Fire(FullTextExpander)

