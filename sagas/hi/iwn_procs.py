from typing import Text, Any, Dict, List, Union
from sagas.nlu.transliterations import translits
from sagas.nlu.google_translator import translate, with_words, WordsObserver

tr=lambda w:translits.translit(w, 'hi')
def trans(w):
    r,t=translate(w, source='hi', target='en', options={'get_pronounce'}, tracker=with_words())
    df=t.observer(WordsObserver).word_trans_df
    if df is not None:
        candidates=[w for w in df['word']][:3]
    else:
        candidates=[]
    return {'word': r.lower(),
            'candidates':candidates}

def word_map(id:int, all_ws:List[Any]) -> Dict[Text,Any]:
    return {tr(w.head_word()):{'index':w.synset_id(),
                               'head':w.head_word(),
                               'trans':trans(w.head_word())} for w in all_ws if w.synset_id()==id}

def load_hypernymy(file_path):
    d = {}
    for line in open(file_path):
        line_parts = line.split('\t')
        synset_id, synset_ids = line_parts
        synset_id = int(synset_id)
        synset_ids = list(map(int, synset_ids.split(',')))
        # synset_ids = list(filter(lambda x: True if x in self._synset_df.index else False, synset_ids))
        if synset_id in d:
            d[synset_id].extend(synset_ids)
        else:
            if synset_ids:
                d[synset_id] = synset_ids
    return d

class IwnProcs(object):
    def __init__(self):
        import os
        from pathlib import Path
        import pyiwn
        from pyiwn import PosTag

        USER_HOME = str(Path.home())
        IWN_DATA_PATH = os.path.join(*[USER_HOME, 'iwn_data'])

        self.iwn = pyiwn.IndoWordNet()
        noun_data_path = f'{IWN_DATA_PATH}/synset_relations/hypernymy.noun'
        verb_data_path = f'{IWN_DATA_PATH}/synset_relations/hypernymy.verb'
        self.all_hypers={PosTag.NOUN.value: load_hypernymy(noun_data_path),
                         PosTag.VERB.value: load_hypernymy(verb_data_path),
                     }
        self.all_ws={PosTag.NOUN.value: self.iwn.all_synsets(pos=PosTag.NOUN),
                     PosTag.VERB.value: self.iwn.all_synsets(pos=PosTag.VERB),
                     }

    def get_all_hypers(self, syn_ids, results, pos:Text):
        hypers=self.all_hypers[pos]
        for syn_id in syn_ids:
            if syn_id in hypers:
                results.append(syn_id)
                self.get_all_hypers(hypers[syn_id], results, pos=pos)

    def get_word_hypers(self, word:Text, pos:Text='noun'):
        try:
            results = []
            ids = [syn.synset_id() for syn in self.iwn.synsets(word)]
            self.get_all_hypers(ids, results, pos=pos)
            return [word_map(sid, self.all_ws[pos]) for sid in results]
        except KeyError:
            return []

    def get_hypers_by_id(self, ids, pos:Text='noun'):
        """
        >>> iwn_procs.get_hypers_by_id(8358)
        :param ids:
        :param pos:
        :return:
        """
        results = []
        self.get_all_hypers(ids if isinstance(ids, list) else [ids], results, pos=pos)
        return [word_map(sid, self.all_ws[pos]) for sid in results]

iwn_procs=IwnProcs()

class IwnCli(object):
    def hypers(self, word:Text, pos:Text='noun'):
        """
        $ python -m sagas.hi.iwn_procs hypers 'सेब'

        :param word:
        :return:
        """
        return iwn_procs.get_word_hypers(word, pos=pos)

if __name__ == '__main__':
    import fire
    fire.Fire(IwnCli)


