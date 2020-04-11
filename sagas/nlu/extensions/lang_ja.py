from sagas.nlu.uni_intf import RootWordImpl, WordIntf, SentenceIntf

rel_mapping={'D': 'att', '時間': 'obl:time',
             'ガ': 'nsubj', 'ヲ': 'obj',
             'デ': 'obl', 'ニ':'obl',
            }
class KnpWordWrapper(WordIntf):
    def setup(self, token):
        deprel=token['dependency_relation']
        token['dependency_relation']=rel_mapping[deprel] if deprel in rel_mapping else deprel
        token['dependency_relation_raw']=deprel
        return token

class KnpSentWrapper(SentenceIntf):
    def setup(self, json_words):
        words = []
        for word in json_words:
            words.append(KnpWordWrapper(word))
        return words, []

