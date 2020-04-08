from typing import Text, Any, Dict, List, Union

# 列举在dataset中使用转写方式填写的语种
translit_langs={'ar','fa','ko'}

negative_maps={
    'en': ['not'],
    'da': ['ikke'],
    'de': ['nicht'],
    'id': ['tidak', 'tak bisa', 'tak boleh'],
    'pt': ['não'],
    'ar': ['lā', 'la'],
    'ja': ['ない'],
}

interrogative_maps={
    'id': {
        'who': ['siapa'],
        'what': ['apa'],
        'be': ['apa'],  # am/is/are
        'will': ['mau'], # would/will
        'can': ['bisa']
    },
    'es': {
        'what': ['qué'],
    },
    'it': {
        'where': ['dove'],
    },
    'pt': {
        'where': ['onde'],
        'why': ['por que'],
        'since_when': ['desde quando'],
    },
    'fa': {
        'have': ['darm', 'darid'],
        'fav': ['dost'],
    },
    'ja': {
        'fav': ['好きだ'],
    },
    'ko': {
        'have': ['iss-eo-yo'],
        'act': ['gar-gga-yo'],
    },
    'ru': {
        'can': ['можно'],
    },
    'lt': {
        'when': ['kada'],
    },
    'no': {
        'when': ['når'],
    },
    'et': {
        'when': ['millal'],
    },
    'hu': {
        'but': ['hanem'],
    },
}


def trans_val(cnt, lang):
    from sagas.nlu.transliterations import translits
    if lang in translit_langs:
        # index 0 is word, 1 is lemma
        return translits.translit(cnt.split('/')[0], lang)
    return cnt.split('/')[-1].lower()

def get_interrogative(word:Text, lang:Text):
    """
    >>> get_interrogative('можно', 'ru')
    :param word:
    :param lang:
    :return:
    """
    word=word.split('/')[-1].lower()
    if lang in interrogative_maps:
        data_map = interrogative_maps[lang]
        for k,v in data_map.items():
            if word in v:
                return k
    return None

def is_negative(word: Text, lang: Text):
    data_map = negative_maps[lang]
    word_val=trans_val(word, lang)
    return word_val in data_map

class DataSetCli(object):
    def interr(self, word, lang):
        """
        $ python -m sagas.nlu.inspectors_dataset interr 'можно' ru
        $ python -m sagas.nlu.inspectors_dataset interr 'por que' pt
        :param word:
        :param lang:
        :return:
        """
        return get_interrogative(word, lang)

if __name__ == '__main__':
    import fire
    fire.Fire(DataSetCli)

