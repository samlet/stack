from typing import Text, Any, Dict, List
from sagas.conf.conf import cf

langsets={'bg': 'bul', 'ca': 'cat', 'cs': 'ces', 'da': 'dan', 'de': 'deu', 'el': 'ell',
          'en': 'eng', 'eu': 'eus', 'fa': 'fas', 'fi': 'fin', 'fr': 'fra', 'hr': 'hrv',
          'id': 'ind', 'is': 'isl', 'it': 'ita', 'ja': 'jpn', 'nl': 'nld', 'nn': 'nno',
          'nb': 'nob', 'pl': 'pol', 'pt': 'por', 'ro': 'ron', 'ru': 'rus', 'sk': 'slk',
          'sl': 'slv', 'es': 'spa', 'sv': 'swe', 'th': 'tha',
          # fixed
          'zh': 'cmn', 'ar': 'arb', 'ms': 'zsm', 'ko': 'kor', 'he': 'heb', 'hi': 'hin',
          'tr': 'tur', 'af': 'afr', 'lt': 'lit',
          'no': 'nob', # nob -> Bokmål, Norwegian; Norwegian Bokmål
          'hu': 'hun', # Hungarian, 10,213(45%)
          'uk': 'ukr', # Ukrainian, 3,761(20%)
          'ur': 'urd', # Urdu, 2,073(15%)
          'et': 'est', # Estonian, 4,317(21%)
          'vi': 'vie', # Vietnamese, 3,869(23%)
          }

# https://stackoverflow.com/questions/319426/how-do-i-do-a-case-insensitive-string-comparison
def NFD(text):
    import unicodedata
    return unicodedata.normalize('NFD', text)
def canonical_caseless(text):
    # X.casefold() == Y.casefold() in Python 3 implements the "default caseless matching"
    # NFD() is called twice for very infrequent edge cases involving U+0345 character.
    return NFD(NFD(text).casefold())
def equals_ignore(a,b):
    if a is None or b is None:
        return False
    return canonical_caseless(a) == canonical_caseless(b)

class OmwExtended(object):
    def __init__(self):
        self.data_tables={}

    def load_dicts(self, lang) -> List[Any]:
        import pandas as pd
        import json
        import os
        prefix = f'{cf.conf_dir}/ai/nltk/data/wikt/'
        if lang not in langsets:
            raise Exception("No dict data for language %s"%lang)

        if lang not in self.data_tables:
            data_path=prefix + 'wn-wikt-%s.tab'%langsets[lang]
            if os.path.exists(data_path):
                df = pd.read_csv(data_path, sep='\t')
                tab = df.to_json(orient='split')
                json_tab = json.loads(tab)
                data = json_tab['data']
                self.data_tables[lang]=data
                print(lang, 'total:', len(data))
            else:
                self.data_tables[lang] = []

        return self.data_tables[lang]

    def get_word(self, lang, offset, pos='n'):
        """
        $ python -m sagas.nlu.omw_extended get_word ru 9918554
        :param lang:
        :param offset:
        :param pos:
        :return:
        """
        id = '%s-%s' % (str(offset).zfill(8), pos)
        # print('.. query', id)
        rs = []
        data = self.load_dicts(lang)
        for row in data:
            if row[0] == id:
                rs.append({'id':row[0], 'word':row[2]})
        return rs

    def get_synset(self, lang, word):
        """
        $ python -m sagas.nlu.omw_extended get_synset ru ложь
        :param lang:
        :param word:
        :return:
        """
        from nltk.corpus import wordnet as wn
        rs = []
        data = self.load_dicts(lang)
        for row in data:
            # if row[2] == word:
            if equals_ignore(row[2], word):
                refid=row[0]
                offset, pos = refid.split('-')
                syn = wn.synset_from_pos_and_offset(pos, int(offset))
                rs.append({'id': refid, 'word': row[2], 'pos': pos, 'synset':syn})
        return rs

    def disp_by_offset(self, lang, offset, pos = 'n'):
        """
        $ python -m sagas.nlu.omw_extended disp_by_offset ru 9918554
        $ python -m sagas.nlu.omw_extended disp_by_offset de 9918554
        :param offset:
        :return:
        """
        import sagas

        offset = str(offset)
        id = '%s-%s' % (offset.zfill(8), pos)
        rs = []
        print('search for', id)
        if lang in langsets:
            data=self.load_dicts(lang)
            for row in data:
                if row[0] == id:
                    rs.append((row[0], row[2]))
            df=sagas.to_df(rs, ['id', 'word'])
            sagas.print_df(df)
        else:
            print('no data.')

omw_ext=OmwExtended()

def get_synsets(lang, word, pos='*') -> List[Any]:
    """
    from sagas.nlu.omw_extended import get_synsets
    sets=get_synsets(lang, word, pos)

    :param lang:
    :param word:
    :param pos:
    :return:
    """
    from nltk.corpus import wordnet as wn
    from sagas.nlu.locales import is_available, iso_locales
    from sagas.ko.kwn_procs import kwn
    sets=[]

    idx_map={'ko': lambda w,pos: kwn.get_synsets(w, first=False) if pos == '*' else kwn.get_synsets_by_pos(w, pos),
             }
    # idx_map = {}
    if lang in idx_map:
        return idx_map[lang](word, pos)

    if is_available(lang):
        loc, _ = iso_locales.get_code_by_part1(lang)
        sets = wn.synsets(word, lang=loc, pos=None if pos == '*' else pos)
    # search the extended wordnet, if absent
    if len(sets)==0 and lang in langsets:
        sets=omw_ext.get_synset(lang=lang, word=word)
        if pos is not None and pos!='*':
            sets=[s['synset'] for s in sets if s['pos']==pos]
        else:
            sets=[s['synset'] for s in sets]

    return sets

if __name__ == '__main__':
    import fire
    fire.Fire(OmwExtended)

