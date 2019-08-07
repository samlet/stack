langsets={'bg': 'bul', 'ca': 'cat', 'cs': 'ces', 'da': 'dan', 'de': 'deu', 'el': 'ell',
          'en': 'eng', 'eu': 'eus', 'fa': 'fas', 'fi': 'fin', 'fr': 'fra', 'hr': 'hrv',
          'id': 'ind', 'is': 'isl', 'it': 'ita', 'ja': 'jpn', 'nl': 'nld', 'nn': 'nno',
          'nb': 'nob', 'pl': 'pol', 'pt': 'por', 'ro': 'ron', 'ru': 'rus', 'sk': 'slk',
          'sl': 'slv', 'es': 'spa', 'sv': 'swe', 'th': 'tha',
          # fixed
          'zh': 'cmn', 'ar': 'arb', 'ms': 'zsm'
          }

class OmwExtended(object):
    def __init__(self):
        self.data_tables={}

    def load_dicts(self, lang):
        import pandas as pd
        import json
        prefix = '/pi/ai/nltk/data/wikt/'
        if lang not in langsets:
            raise Exception("No dict data for language %s"%lang)

        if lang not in self.data_tables:
            df = pd.read_csv(prefix + 'wn-wikt-%s.tab'%langsets[lang], sep='\t')
            tab = df.to_json(orient='split')
            json_tab = json.loads(tab)
            data = json_tab['data']
            self.data_tables[lang]=data
            print(lang, 'total:', len(data))

        return self.data_tables[lang]

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

if __name__ == '__main__':
    import fire
    fire.Fire(OmwExtended)
