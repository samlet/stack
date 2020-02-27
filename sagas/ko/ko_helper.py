from typing import Text, Any, Dict, List, Union

def get_word_sets(word, lang='en', pos='*'):
    import requests
    from sagas.conf.conf import cf
    response = requests.post(f'{cf.ensure("words_servant")}/word_sets',
                             json={'word':word, 'lang':lang, 'pos':pos})
    if response.status_code == 200:
        sets= response.json()
        if sets:
            return sets[0]
    return None

class KoreaHelper(object):
    def __init__(self):
        from konlpy.tag import Mecab
        self.mecab = Mecab()

    def pos(self, phrase: Text):
        return self.mecab.pos(phrase)

    def nouns(self, phrase: Text):
        """
        $ python -m sagas.ko.ko_helper nouns '피자와 스파게티가'
        :param phrase:
        :return:
        """
        return self.mecab.nouns(phrase)

    def translit(self, word):
        """
        $ python -m sagas.ko.ko_helper translit '피자와 스파게티가'

        See also: procs-ko-konlpy.ipynb
        :param word:
        :return:
        """
        from sagas.nlu.transliterations import translits
        for w, p in self.mecab.pos(word):
            expl = '_'
            if p in ('NNG', 'VV'):
                ws = get_word_sets(w, 'ko')
                if ws:
                    expl = f"{ws['name']}({ws['definition']})"
            print(w, translits.translit(w, 'ko'), p, expl)

ko_helper=KoreaHelper()

if __name__ == '__main__':
    import fire
    fire.Fire(KoreaHelper)

