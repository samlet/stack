from typing import Text, Any, Dict, List, Union

# 列举在dataset中使用转写方式填写的语种
translit_langs={'ar','fa','ko'}

nagative_maps={
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
}

def get_interrogative(word:Text, lang:Text):
    """
    >>> get_interrogative('можно', 'ru')
    :param word:
    :param lang:
    :return:
    """
    if lang in interrogative_maps:
        data_map = interrogative_maps[lang]
        for k,v in data_map.items():
            if word in v:
                return k
    return None


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

