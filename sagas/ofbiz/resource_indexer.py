from __future__ import unicode_literals

import os
from whoosh.index import open_dir
from whoosh.index import create_in
from whoosh.fields import *

from jieba.analyse import ChineseAnalyzer
from whoosh.qparser import QueryParser
from sagas.ofbiz.resources import ResourceDigester, read_resource

class ResourceIndexer(object):
    def __init__(self, out_dir='out/labels'):
        self.out_dir=out_dir
        self.rd=ResourceDigester()

        self.analyzer = ChineseAnalyzer()
        self.schema = Schema(en=TEXT(stored=True),
                        fr=TEXT(stored=True),
                        key=ID(stored=True),
                        zh=TEXT(stored=True, analyzer=self.analyzer))
        self.idx=None

    def process(self, xml_file):
        # resource = self.rd.process_resource(xml_file='data/i18n/SagasUiLabels.xml')
        resource = self.rd.process_resource(xml_file)
        return resource

    def index_resource(self, resource):
        ## rewrite mode
        # out_dir='out/labels'
        if not os.path.exists(self.out_dir):
            os.mkdir(self.out_dir)
        self.idx = create_in(self.out_dir, self.schema)

        writer = self.idx.writer()

        for key, prop in resource.properties.items():
            writer.add_document(
                key=key,
                en=prop.values['en'],
                zh=prop.values['zh'],
                fr=prop.values['fr']
            )

        writer.commit()

    def search(self, keyword, lang='zh'):
        """
        $ python -m sagas.ofbiz.resource_indexer search 产品
        $ python -m sagas.ofbiz.resource_indexer search 产品价格
        :param keyword:
        :param lang:
        :return:
        """
        if self.idx is None:
            self.idx = open_dir(self.out_dir)

        searcher = self.idx.searcher()
        parser = QueryParser(lang, schema=self.idx.schema)

        q = parser.parse(keyword)
        results = searcher.search(q)
        for hit in results:
            print(hit["key"])
            print('\t', hit.highlights(lang))
            print('\t', hit['en'])

    def index_all(self):
        """
        $ python -m sagas.ofbiz.resource_indexer index_all
        :return:
        """
        resource, rs_lookups = read_resource()
        self.index_resource(resource)
        print('done.')

if __name__ == '__main__':
    import fire
    fire.Fire(ResourceIndexer)
