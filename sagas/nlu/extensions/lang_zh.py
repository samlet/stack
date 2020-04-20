from sagas.nlu.uni_intf import RootWordImpl, WordIntf, SentenceIntf

rel_mapping={'hed': 'root', 'sbv': 'nsubj',
             'vob': 'obj', 'iob': 'iobj', 'fob': 'obj', 'pob': 'obl',
             'wp': 'punct',
            }

class LtpWordWrapper(WordIntf):
    def setup(self, token):
        deprel=token['dependency_relation']
        token['dependency_relation']=rel_mapping[deprel] if deprel in rel_mapping else deprel
        token['dependency_relation_raw']=deprel
        return token

class LtpSentWrapper(SentenceIntf):
    def setup(self, json_words):
        words = []
        for word in json_words:
            words.append(LtpWordWrapper(word))
        return words, []

