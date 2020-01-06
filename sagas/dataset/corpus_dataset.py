from sqlalchemy import create_engine
import json

# engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine('sqlite:///sagas/dataset/corpus.db', convert_unicode=True)

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
metadata = MetaData()
corpus = Table('corpus', metadata,
              Column('id', Integer, primary_key=True),
              Column('index', Integer),
              Column('chapter', String),
              Column('text', String),
              Column('translate', String),
              Column('translite', String),
              Column('audio', String),
              Column('lang', String),
)

def load_corpus(langs):
    rs=[]
    for lang in langs:
        with open(f'/pi/stack/crawlers/langcrs/all_{lang}.json') as json_file:
            sents=json.load(json_file)
            for s in sents:
                s['lang']=lang
            rs.extend(sents)
    return rs

class CorpusDataset(object):
    def all_corpus(self):
        import glob
        corpus_prefix = '/pi/stack/crawlers/langcrs'
        ds = [f for f in glob.glob(f'{corpus_prefix}/all_*.json')]
        print('\n'.join(ds))

    def build(self):
        """
        $ python -m sagas.dataset.corpus_dataset build

        :return:
        """
        print('.. create meta')
        metadata.drop_all(engine)
        metadata.create_all(engine)

        print('.. load corpus')
        conn = engine.connect()
        rs = load_corpus(['fr', 'es', 'ja'])
        # print(rs[:3])
        conn.execute(corpus.insert(), rs)

    def query(self, lang, chapter='People'):
        """
        $ python -m sagas.dataset.corpus_dataset query fr 'People'
        :param lang:
        :param chapter:
        :return:
        """
        from sqlalchemy.sql import select
        from sqlalchemy.sql import and_, or_, not_

        conn = engine.connect()

        s = select([corpus]).where(and_(corpus.c.chapter == chapter,
                                        corpus.c.lang == lang))
        for row in conn.execute(s):
            print(row.text, '☞', row.translate)

if __name__ == '__main__':
    import fire
    fire.Fire(CorpusDataset)

