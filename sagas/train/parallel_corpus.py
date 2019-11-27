import numpy as np
from sagas.nlu.corpus_helper import filter_term, lines, divide_chunks
import numpy
# import spacy
import json

def load_corpus(dataf='/pi/ai/seq2seq/jpn-eng-2019/jpn.txt'):
    """
    >>> from sagas.train.parallel_corpus import load_corpus, take_samples
    >>> items=load_corpus()
    >>> rows=take_samples(items)
    >>> rows
    :param dataf:
    :return:
    """
    pairs = lines(dataf)
    array = numpy.array(pairs)
    items = []
    for r in array:
        sents = str(r[0])
        tr_lang = str(r[1].strip())
        items.append((sents, tr_lang))
    return items

def take_samples(items, count=10):
    random_rows = numpy.random.randint(len(items), size=count)
    array=numpy.array(items)
    rows = array[random_rows, :]
    samples=[]
    for r in rows:
        sents = str(r[0])
        tr_lang = str(r[1].strip())
        samples.append((sents, tr_lang))
    return samples

prefix='/pi/ai/seq2seq'
corpus_locs={
    'fa':f"{prefix}/en_Persian/pes-eng/pes.txt",
    'ja':f"{prefix}/jpn-eng-2019/jpn.txt",
    'ar':f"{prefix}/ara-eng/ara.txt",
    'bg':f"{prefix}/en_Bulgarian/bul-eng/bul.txt",
    'el':f"{prefix}/en_Greek/ell-eng/ell.txt",
    'es':f"{prefix}/spa-eng-2019/spa.txt",
    'fr':f"{prefix}/fra-eng-2019/fra.txt",
    'ru':f"{prefix}/rus-eng/rus.txt",
}
def search_corpus(loc, lang, words):
    from sagas.nlu.transliterations import translits
    items=load_corpus(loc)
    # rows=take_samples(items)
    def search_in(items, phrase):
        for item in items:
            if words in item[0]:
                print(item)
                # print(f"{l[1]} -> {l[0]}")
                print(translits.translit(item[1], lang))
        print('.. done.')
    search_in(items, words)

class ParallelCorpus(object):
    def __init__(self, ipaddr=None):
        from sagas.conf.conf import cf
        self.ipaddr=ipaddr if ipaddr is not None else cf.conf['bert_servant']
        print(f".. bert service port is {self.ipaddr}")
        # self.ipaddr=ipaddr
        self._bc=None
        # self.bc = BertClient(ip=ipaddr)

        self.topk = 5
        # self.dataf=dataf
        self.samples_count=2
        self.samples=[]

    @property
    def bc(self):
        from bert_serving.client import BertClient
        if self._bc is None:
            self._bc = BertClient(ip=self.ipaddr)
        return self._bc

    def load_corpus(self, dataf='/pi/ai/seq2seq/jpn-eng-2019/jpn.txt'):
        pairs = lines(dataf)
        array = numpy.array(pairs)
        questions = []
        for r in array:
            sents = str(r[0])
            tr_lang = str(r[1].strip())
            questions.append((sents, tr_lang))

        # fill samples
        random_rows = numpy.random.randint(len(pairs), size=self.samples_count)
        rows = array[random_rows, :]
        for r in rows:
            sents = str(r[0])
            tr_lang = str(r[1].strip())
            self.samples.append((sents, tr_lang))

        return questions

    def load_samples(self, dataf='/pi/ai/seq2seq/jpn-eng-2019/jpn.txt', samples_count=100):
        print('loading corpus ...')
        pairs = lines(dataf)
        total = len(pairs)
        print('total', total)
        array = numpy.array(pairs)
        random_rows = numpy.random.randint(total, size=samples_count)
        # print('pickup', random_rows)
        # print(array[random_rows, :])

        # print('analyse ...')
        rows = array[random_rows, :]
        dataset = []
        for r in rows:
            sents = str(r[0])
            tr_lang = str(r[1].strip())
            dataset.append(sents)

        print('pickup ok, total %d' % len(dataset))
        return dataset

    def do_test(self):
        """
        $ python -m sagas.train.parallel_corpus do_test
        :return:
        """
        result=self.bc.encode(['First do it', 'then do it right', 'then do it better'])
        print(result)

    def get_similar(self, questions, doc_vecs, query, print_index=-1, play=None):
        from sagas.nlu.tts_utils import say_lang
        from termcolor import colored
        query_vec = self.bc.encode([query])[0]
        score = np.sum(query_vec * doc_vecs, axis=1) / np.linalg.norm(doc_vecs, axis=1)
        topk_idx = np.argsort(score)[::-1][:self.topk]
        print('top %d sentences similar to "%s"' % (self.topk, colored(query, 'green')))
        for idx in topk_idx:
            if print_index==-1:
                qs=colored(questions[idx], 'yellow')
                print('> %s\t%s' % (colored('%.1f' % score[idx], 'cyan'), qs))
            else:
                qs=colored(questions[idx][0], 'yellow')
                print('> %s\t%s' % (colored('%.1f' % score[idx], 'cyan'), qs))
                qst = colored(questions[idx][1], 'blue')
                print('  %s\t%s' % (colored('ﺴ', 'cyan'), qst))

                if play is not None:
                    langs=play.split('/')
                    say_lang(questions[idx][0], langs[0], False)
                    say_lang(questions[idx][1], langs[1], False)

    def samples(self, query = "I want the two of you to quit arguing."):
        questions = self.load_samples()
        print('computing with bert-as ...')
        doc_vecs = self.bc.encode(questions)
        print('getting similar sentences ...')
        self.get_similar(questions, doc_vecs, query)

    def save_docs(self, doc_vecs, file='/pi/data/bert/samples_1000.npy'):
        print(len(doc_vecs))
        np.save(file, doc_vecs)  # save

    def train_docs(self, lang, sample=False, multilang=False):
        """
        $ python -m sagas.train.parallel_corpus train_docs zh True
        $ python -m sagas.train.parallel_corpus train_docs zh
        $ python -m sagas.train.parallel_corpus train_docs fr
        $ python -m sagas.train.parallel_corpus train_docs fr True True

        With Chinese: use model_dir chinese_L-12_H-768_A-12
            $ python -m sagas.train.parallel_corpus train_docs zh True True

        :param dataf:
        :param outf:
        :return:
        """
        from sagas.nlu.nlu_tools import corpus_resources
        import os
        dataf=corpus_resources[lang]
        if multilang:
            outf="/pi/data/bert/%s.npy"%lang
        else:
            outf="/pi/data/bert/en-%s.npy"%lang
        if os.path.isfile(outf):
            print('precomputed file %s has already exists, exit.'%outf)
            return

        pairs = lines(dataf)
        array = numpy.array(pairs)
        questions = []
        for r in array:
            sents = str(r[0])
            tr_lang = str(r[1].strip())
            if multilang:
                questions.append(tr_lang)
            else:
                questions.append(sents)
        if sample:
            questions=questions[:10]
        print('computing with bert-as: %d ...'%(len(questions)))
        doc_vecs = self.bc.encode(questions)
        self.save_docs(doc_vecs, outf)
        print('done.')

    def bert_as_status(self):
        """
        $ python -m sagas.train.parallel_corpus bert_as_status
        :return:
        """
        print(json.dumps(self.bc.server_status, indent=2, ensure_ascii=False))

    def load_docs(self, file='/pi/data/bert/jpn-eng.npy'):
        doc_vecs = np.load(file)  # load
        return doc_vecs

    def query(self, query="I told you to leave.",
              loop_for=1,
              play='en/ja',
              dataf='/pi/ai/seq2seq/jpn-eng-2019/jpn.txt',
              docs='/pi/data/bert/jpn-eng.npy'):
        """
        $ python -m sagas.train.parallel_corpus query
        $ python -m sagas.train.parallel_corpus query .
        $ python -m sagas.train.parallel_corpus query . 2
        $ python -m sagas.train.parallel_corpus query 'you are welcome' 1 None
        :param dataf:
        :param docs:
        :param query:
        :return:
        """
        from termcolor import colored

        print('load precomputed docs ...')
        doc_vecs=self.load_docs(docs)

        print('load corpus ...')
        if loop_for>self.samples_count:
            self.samples_count=loop_for
        qs=self.load_corpus(dataf)

        print('getting similar sentences ...')
        # self.get_similar(qs, doc_vecs, query, 0)

        tuple_idx = 0
        if query == '.':
            tuple_idx = 0
            query = self.samples[0][tuple_idx]
        elif query=='..':
            tuple_idx = 1
            query = self.samples[0][tuple_idx]

        for n in range(loop_for):
            self.get_similar(qs, doc_vecs, query, 1, play)
            if n<loop_for-1:
                query = self.samples[n+1][tuple_idx]
                print('next loop %s ...' % (colored(str(n+1), 'red')))

    def pr(self, lang='ja', loop_for=1, q='.', say=True):
        """
        $ python -m sagas.train.parallel_corpus pr zh
        $ python -m sagas.train.parallel_corpus pr zh 1 'you are welcome' False
        $ python -m sagas.train.parallel_corpus pr fr 1 'you are welcome' False
        :param lang:
        :param loop_for:
        :return:
        """
        from sagas.nlu.nlu_tools import corpus_resources
        dataf = corpus_resources[lang]
        if q.startswith('..'):
            docsf = "/pi/data/bert/%s.npy" % lang
        else:
            docsf = "/pi/data/bert/en-%s.npy" % lang

        if say:
            play="en/"+lang
        else:
            play=None
        self.query(q, loop_for, play, dataf, docsf)

    def refs_shortcut(self, lang, *items):
        """
        $ python -m sagas.train.parallel_corpus refs_shortcut zh you are welcome
        $ python -m sagas.train.parallel_corpus refs_shortcut ja i am a student
        $ ja you are a bad boy
        $ ru i play basketball
        :param lang:
        :param items:
        :return:
        """
        sents=' '.join(items)
        self.pr(lang, loop_for=1, q=sents, say=False)

    def search(self, phrase, lang):
        """
        $ python -m sagas.train.parallel_corpus search dog fa
        :param phrase:
        :param lang:
        :return:
        """
        search_corpus(corpus_locs[lang], lang, phrase)

if __name__ == '__main__':
    import fire
    fire.Fire(ParallelCorpus)

