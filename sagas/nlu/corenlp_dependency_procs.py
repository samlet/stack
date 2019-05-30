#!/usr/bin/env python
from stanfordcorenlp import StanfordCoreNLP
from sagas.nlu.common import get_from_clip
# from tasks import oplog
import sagas.nlu.tts_utils as tts_utils
import yaml

explains='''
abbrev: 缩写
acomp: 形容词的补充
advcl: 状语从句修饰
advmod: 状语
agent: 代理
amod: 形容
appos: 同位词
attr: 属性
aux: 非主要动词和助词
auxpass: 被动
cc: 并列关系
ccomp: 从句补充
complm: 引导从句
conj: 并列连接
cop: 系动词
csubj: 从主关系
csubjpass: 主从被动关系
dep: 依赖关系
det: 限定词
dobj: 直接宾语
expl: 填补
infmod: 动词不定式
iobj: 间接宾语
mark: marker
mwe: 多词表示
neg: 否定
nn: 名词组合
npadvmod: 名词作状语
nsubj: 名词主语
nsubjpass: 被动名词主语
num: 数值修饰
number: 组合数字
parataxis: 并列关系
partmod: 动词形式的修饰
pcomp: 介词补充
pobj: 介词的宾语
poss: 所有格
possessive: 从属
preconj: preconjunct
predet: 前缀决定
prep: 前置
prepc: 前置项
prt: 动词短语
punct: 符号
purpcl: 目的从句
quantmod: 数量短语
rcmod: 相关
ref: 指代
rel: relative
root: 根
tmod: temporal
xcomp: open-clausal-complement
xsubj: 掌控者
case: 投影
'''

class DependencyProcs(object):
    def __init__(self, lang='fr', port=9003):
        self.explains_dict=yaml.load(explains)
        self.lang=lang
        self.nlp = StanfordCoreNLP('http://localhost', port=port, lang=lang)

    def explain_rel(self, rel):
        suffix=''
        if rel=="dobj":
            suffix="@直接对象"
        elif rel=="nsubj":
            suffix=".actor"
        elif ':' in rel:
            if rel.startswith('nmod:'):
                suffix='@复合名词修饰'
        elif rel in self.explains_dict:
            suffix="@"+self.explains_dict[rel]
        return rel+suffix

    def print_structure(self, tags, tree, logs):
        # rootindex start from 1
        rootindex=0
        # get the root node index
        for node in tree:
            if node[0]=='ROOT':
                rootindex=node[2]
                log="☑ "+str(tags[rootindex-1])
                print(log)
                logs.append(log)
        for node in tree:
            refindex=node[1]
            relname=node[0]
            if refindex==rootindex and relname!='punct':
                target=node[2]
                log=str(self.explain_rel(relname)+": "+str(tags[target-1]))
                logs.append(log)
                print(log)

    def parse(self, sentence):
        logs=[]
        # print("✉ parse with lang "+langname+" ...")
        # nlp = StanfordCoreNLP(folder, lang='zh')

        tags=self.nlp.pos_tag(sentence)
        treelog=str(self.nlp.parse(sentence))
        logs.append(treelog)
        print(treelog)
        tree=self.nlp.dependency_parse(sentence)
        logs.append("⊕ "+str(tree))
        print(tree)
        print("------------ ✁")
        self.print_structure(tags, tree, logs)
        print("**raw sentence: "+sentence)
        logs.append("% "+sentence)
        print("------------ ☼")

        # result=oplog({"lang":langname}, logs)
        # print("oplog result: "+result)

    def tree_parse_clip(self):
        import clipboard
        sentence=get_from_clip()
        clipboard.copy(sentence)

        self.parse(sentence)
        tts_utils.say_lang(sentence, self.lang)

# def tree_en():
#     tree_parse("en", 9001)
#
# def tree_sp(self ):
#     tree_parse("es", 9002)
#
# def tests(self ):
#     sentence = 'Several times a year we distribute a new version of the software'
#     parse_european(sentence, 'en', 9001)
#     sentence = 'Nosotros vivimos cerca de la plaza.'
#     parse_european(sentence, 'es', 9002)

if __name__ == '__main__':
    import fire
    fire.Fire(DependencyProcs)

