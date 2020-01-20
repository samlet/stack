from bert_serving.client import BertClient
import pandas as pd
import numpy as np
import json
import sagas.tracker_fn as tc

def search_in(text, lang):
    with open(f'/pi/stack/crawlers/langcrs/all_{lang}.json') as json_file:
        sents=json.load(json_file)
        return [sent for sent in sents if sent['text']==text]

def search_in_list(text, langs):
    rs={}
    for lang in langs:
        rs[lang]=search_in(text, lang)
    return rs

def sents_summary(sents, source):
    from sagas.nlu.uni_remote import dep_parse
    from sagas.nlu.uni_remote_viz import list_contrast
    from sagas.conf.conf import cf
    from sagas.nlu.utils import fix_sents
    from sagas.nlu.corenlp_parser import get_chunks

    sents=fix_sents(sents, source)
    engine=cf.engine(source)
    doc_jsonify, resp = dep_parse(sents, source, engine, ['predicts'])
    types=[]
    if doc_jsonify is None:
        raise Exception(f'Cannot parse sentence for lang {source}')
    if len(resp['predicts']) > 0:
        rs=resp['predicts']
    else:
        rs = get_chunks(doc_jsonify)

    for serial, r in enumerate(rs):
        print(f"{serial}. {r['type']} -> {r['word']}")
        types.append(f"{source}:{r['type']}")
    list_contrast(rs, source)
    return types

class CorpusSearcher(object):
    def __init__(self, model_file='spacy-2.2/data/embedded_corpus.pkl'):
        self.bc = BertClient()
        self.model_file=model_file

    def train(self, quotes, source_col='text'):
        embeddings = self.bc.encode(quotes[source_col].to_list())
        quotes['EMBEDDINGS'] = embeddings.tolist()

        # Persist to pickle
        quotes.to_pickle(self.model_file)

    def train_corpus(self, data_file, source_col='text'):
        # f'/pi/stack/crawlers/langcrs/all_{lang}.json'
        dfjson = pd.read_json(data_file)
        self.train(dfjson, source_col=source_col)

    def load_quotes_and_embeddings(self, file):
        quotes = pd.read_pickle(file)

        # change dtype in place for memory efficiency
        quotes['EMBEDDINGS'] = quotes['EMBEDDINGS'].apply(
            lambda arr: np.array(arr, dtype='float32')
        )

        quote_embeddings = np.stack(quotes.EMBEDDINGS.values)

        # reduce memory footprint by dropping column
        quotes.drop('EMBEDDINGS', axis='columns')

        # normalize embeddings for cosine distance
        embedding_sums = quote_embeddings.sum(axis=1)
        normed_embeddings = quote_embeddings / embedding_sums[:, np.newaxis]
        return quotes, normed_embeddings

    def create_index(self, embeddings):
        import faiss
        """
        Create an index over the quote embeddings for fast similarity search.
        """
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)
        return index

    def search(self, text, cols, top_result=5):
        text_embedding = self.bc.encode([text])
        normalized_text_embedding = text_embedding / text_embedding.sum()
        quotes, embeddings = self.load_quotes_and_embeddings(self.model_file)
        index = self.create_index(embeddings)

        _, idx = index.search(normalized_text_embedding, top_result)

        # relevant_quotes = quotes.iloc[idx.flatten()].text.values
        # relevant_chapters = quotes.iloc[idx.flatten()].chapter.values
        rs=[]
        for col in cols:
            rs.append(quotes.iloc[idx.flatten()][col].values)
            # relevant_chapters = quotes.iloc[idx.flatten()]['chapter'].values
        return rs

    @staticmethod
    def parse_controls(results):
        rs = []
        for lang, v in results.items():
            for sent in v:
                rs.append((sent['translate'], lang, sent['translit']))
        return rs

    def run(self, text, langs=None, top_result=5, summary=False, verbose=True):
        """
        $ python -m sagas.corpus.searcher run 'I read a letter.'
        $ python -m sagas.corpus.searcher run 'I read a letter.' ja,id
        $ python -m sagas.corpus.searcher run 'I read a letter.' ja,id,fa 2 True False
        :param text:
        :return:
        """
        # 先按相似度查找到与给定内容近似的英文句子
        relevant_quotes, relevant_chapters = self.search(text, ['text', 'chapter'], top_result)
        summary_info=[]
        for q in range(top_result):
            tc.emp('magenta', '>' + relevant_quotes[q])
            tc.emp('green', relevant_chapters[q])

            if langs is not None:
                # 因为语料都是按英文作对照的, 所以直接按英文句子查找到其它语言的句子就可以了
                # search_in_list('I write a letter.', ['ja', 'fa', 'id'])
                results=search_in_list(relevant_quotes[q], langs)
                if verbose:
                    tc.emp('blue', json.dumps(results, indent=2, ensure_ascii=False))

                if summary:
                    all_types = []
                    rs_c=CorpusSearcher.parse_controls(results)
                    for r in rs_c:
                        if r[2]!='':
                            tc.emp('red', f".. {r[2]}")
                        types=sents_summary(r[0], r[1])
                        all_types.extend(types)
                    summary_info.append((relevant_quotes[q], all_types))

            tc.emp('cyan', '✁', '-' * 30)

        for s in summary_info:
            tc.info(s)

    def end(self):
        self.bc.close()

if __name__ == '__main__':
    import fire
    fire.Fire(CorpusSearcher)

