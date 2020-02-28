from typing import Text, Any, Dict, List, Union
import json
import io
from sagas.nlu.transliterations import translits
from nltk.corpus import wordnet as wn

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
             return list(obj)
        return json.JSONEncoder.default(self, obj)

def write_indexes(output_path, lookups_nor, lookups_tra):
    with io.open(f"{output_path}/ko_nor.json", 'w', encoding="utf-8") as f:
        f.write(json.dumps(lookups_nor, indent=2, ensure_ascii=False,
                           cls=SetEncoder))
    with io.open(f"{output_path}/ko_tra.json", 'w', encoding="utf-8") as f:
        f.write(json.dumps(lookups_tra, indent=2, ensure_ascii=False,
                           cls=SetEncoder))

def build_omw(lookups_nor, lookups_tra):
    import pandas as pd
    data_path = '/pi/ai/nltk/data/wikt/wn-wikt-kor.tab'
    df = pd.read_csv(data_path, sep='\t')
    for index, row in df.iterrows():
        refid = row['# Wiktionary']
        kw = row['http://wiktionary.org/']
        offset, pos = refid.split('-')
        syn = wn.synset_from_pos_and_offset(pos, int(offset))
        if kw not in lookups_nor:
            lookups_nor[kw] = {syn.name()}
            lookups_tra[translits.translit(kw, 'ko')] = {syn.name()}
        else:
            lookups_nor[kw].add(syn.name())
            lookups_tra[translits.translit(kw, 'ko')].add(syn.name())

def build_kwn(lookups_nor, lookups_tra):
    rs = []
    import pandas as pd
    data_path = '/pi/ai/nltk/kwn_1.0/kwn_synset_list.tsv'
    df = pd.read_csv(data_path, sep='\t')

    for index, row in df.iterrows():
        ko_lemmas = row['korean_lemmas'].split(', ')
        refid = row['# synset_id']
        offset, pos = refid.split('-')
        syn = wn.synset_from_pos_and_offset(pos, int(offset))
        en_lemmas=str(row['english_lemmas']).split(', ')
        rs.append({'id': refid,
                   'en': en_lemmas,
                   'ko': ko_lemmas,
                   'translit': [translits.translit(le, 'ko') for le in ko_lemmas],
                   'name': syn.name(),
                   'definition': syn.definition()
                   })
        for kw in ko_lemmas:
            if kw not in lookups_nor:
                lookups_nor[kw] = {syn.name()}
                lookups_tra[translits.translit(kw, 'ko')] = {syn.name()}
            else:
                lookups_nor[kw].add(syn.name())
                lookups_tra[translits.translit(kw, 'ko')].add(syn.name())
    return rs

class KwnProcs(object):
    """
    See also: procs-ko-kwn.ipynb
    """
    def __init__(self):
        self.idx_nor={}
        self.idx_tra={}
        self.index_dir = '/pi/stack/sagas/conf/synsets'

    def write_indexes(self):
        """
        $ python -m sagas.ko.kwn_procs write_indexes
        :return:
        """
        lookups_nor = {}
        lookups_tra = {}

        build_kwn(lookups_nor, lookups_tra)
        build_omw(lookups_nor, lookups_tra)
        write_indexes(self.index_dir, lookups_nor, lookups_tra)
        print('ok.')

    def lookup_nor(self, word):
        """
        $ python -m sagas.ko.kwn_procs lookup_nor '미생물'
        :param word:
        :return:
        """
        import json_utils
        if not self.idx_nor:
            self.idx_nor=json_utils.read_json_file(f"{self.index_dir}/ko_nor.json")
        return self.idx_nor[word] if word in self.idx_nor else []

    def get_synsets(self, word, first=False) -> List[Any]:
        """
        >>> from sagas.ko.kwn_procs import kwn
        >>> kwn.get_synsets('필요')

        :param word:
        :param first:
        :return:
        """
        refs=self.lookup_nor(word)
        if first and refs:
            return [wn.synset(refs[0])]
        return [wn.synset(w) for w in refs]

    def get_synsets_by_pos(self, word, pos):
        ws=self.get_synsets(word, first=False)
        if pos is None or pos=='*':
            return ws
        return [w for w in ws if w.pos()==pos]

    def lookup_tra(self, word):
        """
        $ python -m sagas.ko.kwn_procs lookup_tra mi-saeng-mur
        :param word:
        :return:
        """
        import json_utils
        if not self.idx_tra:
            self.idx_tra=json_utils.read_json_file(f"{self.index_dir}/ko_tra.json")
        return self.idx_tra[word] if word in self.idx_tra else []

kwn=KwnProcs()

if __name__ == '__main__':
    import fire
    fire.Fire(KwnProcs)

