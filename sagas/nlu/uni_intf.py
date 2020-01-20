import abc
import io

sub_comps=['ccomp', 'xcomp', # general
           # advcl：状语从句修饰语, 状语从句修饰语是将动词或其他谓词（形容词等）修饰为修饰语
           # 而不是核心补语的从句。这包括诸如时间子句，结果，条件子句，目的子句等之类的东西。
           # 从属必须是子句（否则它是advmod），并且从属是该子句的主要谓词。
           'advcl', 'obj', # occurs in id
           # acl：名词的句法修饰语（adjectival clause）
           # acl代表修改名义的有限和非有限条款。这种acl关系与advcl关系形成对比，
           # advcl关系用于修改谓词的状语从句。acl关系的头部是被修改的名词，
           # 而从属关系是修饰名词的子句的头部。
           'acl',
           'adv', 'coo', 'vob', 'att', # zh
           ]

class WordIntf(abc.ABC):
    def __init__(self, data):
        self.ctx = self.setup(data)

    @abc.abstractmethod
    def setup(self, data):
        pass

    @property
    def dependency_relation(self):
        return self.ctx['dependency_relation']

    @property
    def lemma(self):
        """ Access lemma of this word. """
        return self.ctx['lemma'] if 'lemma' in self.ctx else ''

    @property
    def governor(self):
        """ Access governor of this word. """
        return self.ctx['governor']

    @property
    def pos(self):
        """ Access (treebank-specific) part-of-speech of this word. Example: 'NNP'"""
        return self.ctx['pos']

    @property
    def text(self):
        """ Access text of this word. Example: 'The'"""
        return self.ctx['text']

    @property
    def xpos(self):
        """ Access treebank-specific part-of-speech of this word. Example: 'NNP'"""
        return self.ctx['xpos']

    @property
    def upos(self):
        """ Access universal part-of-speech of this word. Example: 'DET'"""
        return self.ctx['upos']

    @property
    def feats(self):
        """ Access morphological features of this word. Example: 'Gender=Fem'"""
        return self.ctx['feats']

    @property
    def index(self):
        """ Access index of this word. """
        return self.ctx['index']

    @property
    def entity(self):
        return self.ctx['entity'] if 'entity' in self.ctx else []

    def __repr__(self):
        features = ['index', 'text', 'lemma', 'upos', 'xpos',
                    'feats', 'governor', 'dependency_relation']
        feature_str = ";".join(["{}={}".format(k, getattr(self, k)) for k in features if getattr(self, k) is not None])

        return f"<{self.__class__.__name__} {feature_str}>"


class RootWordImpl(WordIntf):
    def setup(self, token):
        features = {'index':0, 'text':'ROOT', 'lemma':'root', 'upos':'', 'xpos':'',
                    'feats':[], 'governor':0, 'dependency_relation':''}
        return features

class SentenceIntf(abc.ABC):
    def __init__(self, sent, predicts=None):
        if predicts is None:
            predicts=[]
        self.predicts=predicts
        self._words, self._dependencies = self.setup(sent)
        if self._dependencies is None or len(self._dependencies)==0:
            self.build_dependencies()
        # print('.......')

    def has_predicts(self):
        return self.predicts is not None and len(self.predicts)>0

    @abc.abstractmethod
    def setup(self, sent):
        pass

    @property
    def dependencies(self):
        """ Access list of dependencies for this sentence. """
        return self._dependencies

    @property
    def words(self):
        """ Access list of words for this sentence. """
        return self._words

    def build_dependencies(self):
        for word in self.words:
            if word.governor == 0:
                # make a word for the ROOT
                governor = RootWordImpl(None)
            else:
                # id is index in words list + 1
                governor = self.words[word.governor - 1]
            self.dependencies.append((governor, word.dependency_relation, word))

    def print_words(self, file=None):
        for word in self.words:
            print(word, file=file)

    def words_string(self):
        wrds_string = io.StringIO()
        self.print_words(file=wrds_string)
        return wrds_string.getvalue().strip()

    def print_dependencies(self, file=None):
        for dep_edge in self.dependencies:
            print((dep_edge[2].text, dep_edge[0].index, dep_edge[1]), file=file)

    def dependencies_string(self):
        dep_string = io.StringIO()
        self.print_dependencies(file=dep_string)
        return dep_string.getvalue().strip()
