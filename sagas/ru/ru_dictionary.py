import pandas as pd
import re

dict_maps={'v':'verbs', 'n':'nouns', 'a':'adjectives', 'o':'others'}
class RuDictionary(object):
    def __init__(self, pos='v', accented=False):
        if accented:
            self.word_col='accented'
        else:
            self.word_col='bare'
        dict_name=dict_maps[pos]
        verbs = '/pi/nlp/russian-dictionary/%s.csv'%dict_name
        self.df = pd.read_csv(verbs, delimiter='\t')

    def lookup(self, word_pat, enable_de=True):
        """
        :param word_pat: is a regex expression, like 'thank|appreciate'
        :return:
        """
        rs_df = self.df[self.df['translations_en'].str.contains(word_pat, flags=re.IGNORECASE, regex=True, na=False)]
        if enable_de:
            return rs_df[[self.word_col, 'translations_en', 'translations_de']].head()
        return rs_df[[self.word_col, 'translations_en']].head()



