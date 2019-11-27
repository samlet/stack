from sagas.corpus.searcher import CorpusSearcher, search_in_list

class IndexTrainer(object):
    def __init__(self):
        self.default_models={
            'id': '/pi/data/bert/embedded_id.pkl'
        }

    def train(self, lang_col, corpus_file, model_file):
        """
        $ python -m sagas.corpus.index_trainer train id '/pi/ai/seq2seq/ind-eng/ind.txt' '/pi/data/bert/embedded_id.pkl'
        :param corpus_file:
        :return:
        """
        from sagas.train.parallel_corpus import load_corpus, take_samples
        import sagas
        items = load_corpus(corpus_file)
        corpus_df = sagas.to_df(items, ['en', lang_col])
        print('.. head rows')
        print(corpus_df.head())

        searcher = CorpusSearcher(model_file=model_file)
        print(f'.. training {corpus_file}')
        searcher.train(corpus_df, 'en')
        print('done.')

    def search(self, text, lang_col, model_file, top_result=5):
        """
        $ python -m sagas.corpus.index_trainer search 'hi' id '/pi/data/bert/embedded_id.pkl'
        :param text:
        :param lang_col:
        :param model_file:
        :param top_result:
        :return:
        """
        from sagas.tool.misc import color_print
        searcher = CorpusSearcher(model_file=model_file)
        relevant_en, relevant_l = searcher.search(text, ['en', lang_col], top_result)
        for q in range(top_result):
            print(relevant_en[q], end=' ')
            color_print('cyan', relevant_l[q])

    def search_id(self, text, top_result=5):
        """
        $ python -m sagas.corpus.index_trainer search_id 'hi'

        :param text:
        :param top_result:
        :return:
        """
        self.search(text, 'id', self.default_models['id'], top_result)

if __name__ == '__main__':
    import fire
    fire.Fire(IndexTrainer)



