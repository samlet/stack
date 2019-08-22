import spacy
from spacy.symbols import nsubj, VERB
from spacy.tokens import Doc

import resources_pb2 as res
import protobuf_utils
from tqdm import tqdm, trange

from sagas.nlu.spacy_helper import chunks_df


def lines(filename):
    with open(filename) as f:
        lines = f.readlines()
        return [line.split('\t') for line in lines]

def data_ja_en():
    dataf = "/pi/ai/seq2seq/jpn-eng/jpn.txt"
    pairs = lines(dataf)
    return pairs

def put_entities(doc, props):
    """
    props={}
    put_entities(doc, props)
    print(json.dumps(props, indent=2))
    :param doc:
    :param props:
    :return:
    """
    for ent in doc.ents:
        # print(ent.text, ent.start_char, ent.end_char, ent.label_)
        props[ent.label_]=ent.text
        facet="%s|%s"%(ent.label_, 'loc')
        props[facet]="%d %d"%(ent.start_char, ent.end_char)

def put_chunks(doc, props):
    """
    props={}
    put_chunks(doc, props)
    print(json.dumps(props, indent=2))
    :param doc:
    :param props:
    :return:
    """
    toks = {'text': [], 'root_text': [], 'root_dep': [], 'head': []}
    for chunk in doc.noun_chunks:
        # print(chunk.text, chunk.root.text, chunk.root.dep_,
        #      chunk.root.head.text)
        toks['text'].append(chunk.text)
        toks['root_text'].append(chunk.root.text)
        toks['root_dep'].append(chunk.root.dep_)
        toks['head'].append(chunk.root.head.text)
        props[chunk.root.dep_]=chunk.root.text
        props[chunk.root.dep_+'|text']=chunk.text
        props[chunk.root.dep_+'|head']=chunk.root.head.text
    return toks

class SpacyViz(object):
    def __init__(self, nlp=None):
        from graphviz import Digraph
        self.f = Digraph('deps', filename='deps.gv')
        self.f.attr(rankdir='LR', size='6,4')
        self.f.attr('node', shape='circle')

        if nlp is not None:
            self.nlp=nlp
        else:
            self.nlp = spacy.load("en_core_web_sm")

    def print_dependencies(self, doc, segs, file=None):
        for word in doc:
            print("%s --(%s)--> %s" % (word.lemma_, word.dep_, word.head.lemma_))
            self.f.edge(word.lemma_, word.head.lemma_, label=word.dep_)

    def analyse(self, sents):
        """
        SpacyViz().analyse('Revenue exceeded twelve billion dollars')
        :param sents:
        :return:
        """
        segs = []
        doc = self.nlp(sents)
        for word in doc:
            self.f.node(word.lemma_)
            segs.append(word.lemma_)
        self.print_dependencies(doc, segs)
        return self.f

    def analyse_chunks(self, sents):
        """
        SpacyViz().analyse_chunks('Revenue exceeded twelve billion dollars')
        :param sents:
        :return:
        """
        segs = []
        doc = self.nlp(sents)
        print(chunks_df(doc))
        for chunk in doc.noun_chunks:
            self.f.edge(chunk.root.text,
                        chunk.root.head.text,
                        label=chunk.root.dep_)
        return self.f

"""
ref# procs-dgraph-spacy.ipynb
"""
class SpacyBuilder(object):
    def __init__(self):
        # from ipywidgets import IntProgress
        # from IPython.display import display

        self.nlp = spacy.load("en_core_web_sm")
        self.pairs = data_ja_en()

        max_count = len(self.pairs)
        # self.f = IntProgress(min=0, max=max_count)  # instantiate the bar
        # display(self.f)  # display the bar

    # def step(self, val=1):
    #     self.f.value += val  # signal to increment the progress bar

    def procs(self, out_file='/pi/data/langs/jpn_eng_spacy.data'):
        """
        $ python -m sagas.graph.dgraph_spacy procs
        :param out_file:
        :return:
        """
        import numpy as np
        englist = []
        for lang in self.pairs:
            englist.append(lang[0])
        x = np.array(englist)
        lang_rs = np.unique(x)

        verb_maps = {}
        rs = []
        # for pair in tqdm(self.pairs):
        for lang in tqdm(lang_rs):
            # doc = self.nlp(pair[0])
            doc = self.nlp(str(lang))
            # Finding a verb with a subject from below — good
            # verbs = set()
            verbs =[]
            lemmas=[]
            for possible_subject in doc:
                if possible_subject.dep == nsubj and possible_subject.head.pos == VERB:
                    verbs.append(possible_subject.head.text)
                    lemmas.append(possible_subject.head.lemma_)
            if len(verbs) > 0:
                verb_maps[lang] = verbs

            # self.step()
            data = doc.to_bytes()
            lang = res.RsLang(entries=[lang], store=data, verbs=verbs, verbLemmas=lemmas)
            rs.append(lang)

        print(len(verb_maps))
        # randomly print some data
        print(self.pairs[2000], verb_maps[self.pairs[2000][0]])
        print(self.pairs[3000], verb_maps[self.pairs[3000][0]])

        # write to file
        print('.. write to file')
        # self.write_samples(False, './data/langs/jpn_eng_spacy.data')
        langs = res.RsLangs(langs=rs)
        protobuf_utils.write_proto_to(langs, out_file)
        print('done.')

    def parse(self, pair, rs):
        doc = self.nlp(pair[0])
        data = doc.to_bytes()
        lang = res.RsLang(entries=pair, store=data)
        rs.append(lang)

    def write_samples(self, only_samples=True, out_file='/pi/data/langs/samples_100.data'):
        rs = []
        if only_samples:
            for i in range(2000, 2100):
                self.parse(self.pairs[i], rs)
        else:
            for p in self.pairs:
                self.parse(p, rs)

        langs = res.RsLangs(langs=rs)
        protobuf_utils.write_proto_to(langs, out_file)

    def load_samples(self, input_file='/pi/data/langs/samples_100.data'):
        load_langs = res.RsLangs()
        protobuf_utils.read_proto(load_langs, input_file)
        print(len(load_langs.langs))

        for lang in load_langs.langs:
            doc = Doc(self.nlp.vocab).from_bytes(lang.store)
            print(lang.entries[0], self.get_verbs(doc))

    def get_verbs(self, doc):
        verbs = set()
        for possible_subject in doc:
            if possible_subject.dep == nsubj and possible_subject.head.pos == VERB:
                verbs.add(possible_subject.head)
        return verbs


if __name__ == '__main__':
    import fire
    fire.Fire(SpacyBuilder)

