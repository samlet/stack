from sagas.bots.hanlp_client import HanlpClient
import sys

from google.protobuf.json_format import MessageToJson
from client_wrapper import ServiceClient

import nlpserv_pb2 as nlp_messages
import nlpserv_pb2_grpc as nlp_service
from utils import dump
import pandas as pd

class HanlpVizBase(object):
    def __init__(self):
        from graphviz import Digraph
        self.f = Digraph('deps', filename='deps.gv')
        # self.f.attr(rankdir='LR', size='8,5')
        self.f.attr(rankdir='LR', size='6,5')
        self.f.attr('node', shape='circle')

class HanlpViz(HanlpVizBase):
    """
    from sagas.bots.hanlp_viz import HanlpViz
    HanlpViz().analyse('我要找一本英语书')
    """
    def print_dependencies(self, doc, segs, file=None):
        for word in doc.getWordArray():
            print("%s --(%s)--> %s" % (word.LEMMA, word.DEPREL, word.HEAD.LEMMA))
            self.f.edge(word.LEMMA, word.HEAD.LEMMA, label=word.DEPREL)

    def analyse(self, sents):
        from sagas.bots.hanlp_procs import hanlp
        segs = []
        doc = hanlp.j.HanLP.parseDependency(sents)
        words = doc.getWordArray()
        for word in words:
            self.f.node(word.LEMMA)
            segs.append(word.LEMMA)
        self.print_dependencies(doc, segs)
        return self.f

dep_mappings="""SBV	主谓关系	subject-verb	我送她一束花 (我 <-- 送)
VOB	动宾关系	直接宾语，verb-object	我送她一束花 (送 --> 花)
IOB	间宾关系	间接宾语，indirect-object	我送她一束花 (送 --> 她)
FOB	前置宾语	前置宾语，fronting-object	他什么书都读 (书 <-- 读)
DBL	兼语	double	他请我吃饭 (请 --> 我)
ATT	定中关系	attribute	红苹果 (红 <-- 苹果)
ADV	状中结构	adverbial	非常美丽 (非常 <-- 美丽)
CMP	动补结构	complement	做完了作业 (做 --> 完)
COO	并列关系	coordinate	大山和大海 (大山 --> 大海)
POB	介宾关系	preposition-object	在贸易区内 (在 --> 内)
LAD	左附加关系	left adjunct	大山和大海 (和 <-- 大海)
RAD	右附加关系	right adjunct	孩子们 (孩子 --> 们)
IS	独立结构	independent structure	两个单句在结构上彼此独立
WP	标点符号	punctuation	标点符号
HED	核心关系	head	指整个句子的核心"""

def to_df(list_of_tuples, columns):
    return pd.DataFrame(list_of_tuples, columns=columns)

def fix_desc(desc):
    if '，' in desc:
        desc=desc.split('，')[1]
    return desc.replace('-','_').replace(' ','_')

def entities_df(ents):
    rows=[]
    for el in ents:
        rows.append((el.start, el.end, el.value, el.entity))
    return to_df(rows, ['start', 'end', 'word', 'entity'])

class HanlpProtoViz(HanlpVizBase):
    """
        from sagas.bots.hanlp_viz import HanlpProtoViz
        HanlpProtoViz().analyse('我要找一本英语书')
        HanlpProtoViz(verbose=False).analyse('徐先生还具体帮助他确定了把画雄鹰、松鼠和麻雀作为主攻目标。')
        """
    def __init__(self, verbose=True):
        super().__init__()
        self.verbose=verbose
        # self.client = ServiceClient(nlp_service, 'NlpProcsStub', 'localhost', 10052)
        self.hanlp=HanlpClient()
        self.client=self.hanlp.client
        self.dep_map = {}
        for el in dep_mappings.split('\n'):
            parts = el.split('\t')
            depname = fix_desc(parts[2])
            # rows.append((parts[0], depname, "[%s]" % parts[1], parts[3]))
            self.dep_map[parts[0]] = (depname, parts[1])

    def deps(self, text):
        request = nlp_messages.NlTexts(texts=[nlp_messages.NlText(text=text)])
        response = self.client.GetDependencyGraph(request)
        return response

    def deps_df(self, text):
        response = self.deps(text)
        rows = []
        for t in response.words:
            # print(MessageToJson(resp))
            rows.append((t.lemma, self.dep_map[t.deprel][0],
                         self.dep_map[t.deprel][1],
                         t.head))
        return to_df(rows, ['lemma', 'dep', 'dep_t', 'head'])

    def print_dependencies(self, doc, segs, file=None):
        for word in doc.words:
            if self.verbose:
                print("%s --[%s](%s)--> %s" % (word.lemma,
                                               self.dep_map[word.deprel][1],
                                               word.deprel, word.head))
            self.f.edge(word.lemma, word.head,
                        label=self.dep_map[word.deprel][1])

    def analyse(self, sents):
        segs = []
        response=self.deps(sents)
        for word in response.words:
            self.f.node(word.lemma)
            segs.append(word.lemma)
        self.print_dependencies(response, segs)
        return self.f

    def extract(self, text):
        request = nlp_messages.NlTokenizerRequest(text=nlp_messages.NlText(text=text))
        response = self.client.EntityExtractor(request)
        return response
