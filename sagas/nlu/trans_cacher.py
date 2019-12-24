# import sagas.nlu.google_translator as tr
from pymongo import MongoClient
from sagas.conf.conf import cf

class TransCacher(object):
    def __init__(self):
        # print('.. connect mongo')
        # self.client = MongoClient(cf.ensure('mongo'), 27017)
        self.client = MongoClient(cf.ensure('mongo'))
        self.db = self.client.langs
        self.coll = self.db.trans

    def update(self, meta, arg):
        rec = {}
        result=0
        if self.count(meta)==0:
            # print('.. persist -> %s'%(meta['text']))
            rec.update(meta)
            rec['content'] = arg
            result = self.coll.insert_one(rec)
        else:
            # print('.. text already cached, skip.')
            pass
        return result

    def retrieve(self, meta):
        r = self.coll.find_one(meta)
        return r

    def count(self, meta):
        # r = self.coll.find(meta).count()
        r = self.coll.count_documents(meta)
        return r

    def remove(self, meta):
        return self.coll.delete_many(meta)

    def all_sents(self, s, t):
        rs = []
        for r in self.coll.find({'source': s, 'target': t}):
            rs.append(r['text'])
        return rs

cacher = TransCacher()

class CacherProcs(object):
    def __init__(self):
        # self.cacher=TransCacher()
        pass

    def all_sents(self, s, t):
        """
        $ python -m sagas.nlu.trans_cacher all_sents en es

        # store and query
        $ python -m sagas.nlu.google_translator translate 'Садись, где хочешь.' en ru
        $ python -m sagas.nlu.trans_cacher all_sents ru en

        :param s:
        :param t:
        :return:
        """
        rs=cacher.all_sents(s, t)
        print('\n'.join(rs))

    def all_sources(self, s):
        """
        $ python -m sagas.nlu.trans_cacher all_sources vi
        :param s:
        :return:
        """
        import sagas
        rs = []
        for r in cacher.coll.find({'source': s}):
            rs.append((r['text'], r['target']))
        sagas.print_df(sagas.to_df(rs, ['text', 'target']))

if __name__ == '__main__':
    import fire
    fire.Fire(CacherProcs)
