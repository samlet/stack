import pandas as pd
from sagas.nlu.utils import fix_sents

def list_chapter_titles(lang):
    dfjson = pd.read_json(f'/pi/stack/crawlers/langcrs/all_{lang}.json')
    return [name for name, group in dfjson.groupby('chapter')]

class IntentsTool(object):
    def __init__(self):
        from pymongo import MongoClient
        self.client = MongoClient(port=27017)
        self.db = self.client.lang

    def init_chapters(self):
        self.db.meta.update_one({'item': 'corpus'}, {'$set': {'chapters': list_chapter_titles('id')}}, upsert=True)

    def get_chapters(self):
        """
        $ python -m sagas.tool.intents_tool get_chapters
        :return:
        """
        return self.db.meta.find_one({'item': 'corpus'})

    def list_chapter_text(self, lang, chapter, fix=False):
        """
        >>> intents_tool.list_chapter_text('fr', 'People', True)
        >>> intents_tool.list_chapter_text('en', 'People')

        :param lang:
        :param chapter:
        :param fix:
        :return:
        """
        field = f'lang_{lang}' if lang != 'en' else 'text'
        print(*[doc[field] if not fix else fix_sents(doc[field], lang)
                for doc in self.db.corpus.find({'chapter': chapter})], sep='\n')

    def store_dataset(self, lang):
        """
        $ python -m sagas.tool.intents_tool store_dataset de
        :param lang:
        :return:
        """
        dfjson = pd.read_json(f'/pi/stack/crawlers/langcrs/all_{lang}.json')
        for index, row in dfjson.iterrows():
            result = self.db.corpus.update_one({'text': row['text'], 'chapter': row['chapter'], 'index': row['index']},
                                          {'$set': {f'lang_{lang}': row['translate']}},
                                          upsert=True)

    def init_datasets(self):
        self.store_dataset('id')
        self.store_dataset('fr')

    def corpus_count(self):
        """
        $ python -m sagas.tool.intents_tool corpus_count
        :return:
        """
        return self.db.corpus.count_documents({})

    def find_corpus(self, filters):
        """
        >>> intents_tool.find_corpus({'chapter': 'People', 'index': 3})
        >>> rec=intents_tool.find_corpus({'text': 'both of us'})
        >>> rec['intent'] if 'intent' in rec else 'none.'

        :param filters:
        :return:
        """
        return self.db.corpus.find_one(filters)

    def set_intent(self, filters, intent):
        """
        >>> intents_tool.set_intent({'text': 'both of us'}, 'person_plural')
        :return:
        """
        result = self.db.corpus.update_many(filters, {'$set': {'intent': intent}}, upsert=True)
        return result

    def set_intent_by_text(self, text, intent):
        return self.set_intent({'text':text}, intent)

    def list_intents(self):
        """
        $ python -m sagas.tool.intents_tool list_intents

        :return:
        """
        rs = self.db.corpus.find({'$and': [
            {"intent": {'$not': {'$size': 0}}},
            {"intent": {'$exists': True}}
        ]})
        # print(rs.count())
        rm = {r['text']: r['intent'] for r in rs}
        print('.. intents', {r for r in rm.values()})
        print(rm)

intents_tool=IntentsTool()

if __name__ == '__main__':
    import fire
    fire.Fire(IntentsTool)

