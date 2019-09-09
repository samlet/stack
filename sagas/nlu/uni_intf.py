import abc
import io

sub_comps=['ccomp', 'xcomp', # general
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
        return self.ctx['lemma']

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
