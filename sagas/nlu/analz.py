from typing import Text, Any, Dict, List, Union, Optional, Tuple

from dataclasses import dataclass

from sagas.nlu.anal_conf import AnalConf
from sagas.nlu.anal_defs import terms_list
from sagas.nlu.analz_base import Docz


class Analz(object):
    """
    >>> from sagas.nlu.analz import analz
    >>> analz.add_pats('typ', ['寄账单地址'])
    >>> analz.add_pats('srv', ['新建'])
    >>> doc=analz.parse("我想要新建一些寄账单地址")
    >>> analz.vis(doc)
    >>> doc.terms
    """
    def __init__(self):
        import os
        from sagas.conf.conf import cf
        from pyltp import Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller
        from spacy.strings import StringStore

        self.stringstore = StringStore()

        MODELDIR = f'{cf.conf_dir}/ai/ltp/ltp_data_v3.4.0'
        self.postagger = Postagger()
        self.postagger.load(os.path.join(MODELDIR, "pos.model"))
        par_model_path = os.path.join(MODELDIR, 'parser.model')
        self.parser = Parser()
        self.parser.load(par_model_path)
        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(os.path.join(MODELDIR, "ner.model"))
        self.labeller = SementicRoleLabeller()
        self.labeller.load(os.path.join(MODELDIR, "pisrl.model"))

        self.conf = AnalConf('zh')
        self.conf.setup(self)

    def add_pats(self, pat_name, pat_text_ls: List[Text]):
        import jieba
        id_hash = self.stringstore.add(pat_name)
        for t in pat_text_ls:
            jieba.add_word(t, tag=id_hash)

    def tokenize(self, sents: Text) -> List[Dict[Text,Text]]:
        import jieba.posseg as pseg
        toks = pseg.cut(sents)
        terms = []
        for i, (word, flag) in enumerate(toks):
            if not isinstance(flag, str):
                ref = self.stringstore[flag]
            else:
                ref = flag
            terms.append({'term': ref, 'value': word})
        return terms

    def parse(self, sents: Text) -> Docz:
        terms=self.tokenize(sents)
        words=[w['value'] for w in terms]
        postags = self.postagger.postag(words)
        arcs = self.parser.parse(words, postags)
        roles = self.labeller.label(words, postags, arcs)
        netags = self.recognizer.recognize(words, postags)

        # terms=list(filter(lambda x: x['term'] in terms_list, terms))
        return Docz(words, postags, arcs, roles, netags, terms)

    def vis(self, doc):
        from graphviz import Digraph
        f = Digraph('deps', filename='deps.gv')
        f.attr(rankdir='LR', size='8,5')
        f.attr('node', shape='egg', fontname='Calibri')
        for i in range(len(doc.words)):
            idx=int(doc.arcs[i].head) - 1
            if idx==-1:
                continue
            a = doc.words[idx]
            print("%s --> %s|%s|%s|%s" % (a, doc.words[i],
                                          doc.arcs[i].relation,
                                          doc.postags[i], doc.netags[i]))
            f.edge(a, doc.words[i], label=doc.arcs[i].relation.lower())
        return f


analz=Analz()
