import sagas.graph.dgraph_helper as helper
import pydgraph
from sagas.nlu.corpus_helper import filter_term, lines, divide_chunks
from tqdm import tqdm, trange

def add_term(index, pair, rs, lang='ja'):
    rs.append('<_:s%d> <sents> "%s" .'%(index, filter_term(pair[0])))
    rs.append('<_:s%d> <ja> "%s"@%s .'%(index, filter_term(pair[1]), lang))

"""
ref# procs-dgraph-fulltext.ipynb
"""
class JaProcs(object):
    def fill_data(self, do_samples=True):
        """
        $ time python -m sagas.graph.dgraph_ja fill_data False
            real	1m1.421s
            user	0m1.148s
            sys	0m0.364s
            + after use tqdm with chunks divider
            real	1m2.639s
            user	0m0.834s
            sys	0m0.249s
        :param do_samples:
        :return:
        """
        dataf = "/pi/ai/seq2seq/jpn-eng/jpn.txt"
        pairs = lines(dataf)

        client = helper.reset('''
        sents: string @index(fulltext) .
        ja: string @index(fulltext) @lang .
        ''')

        if do_samples:
            rs = []
            for i in range(2000, 2100):
                add_term(i, pairs[i], rs)
            cnt = '\n'.join(rs)
            # print(cnt)
            _ = helper.set_nquads(client, cnt)
        else:
            lists = list(divide_chunks(pairs, 500))
            for chunk in tqdm(lists):
                rs = []
                i=0
                # for i in range(0, count):
                for c in chunk:
                    add_term(i, c, rs)
                    i+=1
                cnt = '\n'.join(rs)
                _ = helper.set_nquads(client, cnt)

    def query_data(self):
        """
        $ python -m sagas.graph.dgraph_ja query_data
        :return:
        """
        client=helper.create_client()
        helper.run_q(client, '''{
          data(func: alloftext(sents, "diet")) {
             sents
             ja
          }
        }''')

        helper.run_q(client, '''{
          data(func: alloftext(ja@ja, "風邪")) {
             sents
             ja@ja
          }
        }''')

        
if __name__ == '__main__':
    import fire
    fire.Fire(JaProcs)

