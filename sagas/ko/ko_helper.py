from typing import Text, Any, Dict, List, Union

from sagas.nlu.utils import get_word_sets


class KoreaHelper(object):
    def __init__(self):
        from konlpy.tag import Mecab
        self.mecab = Mecab()

    def pos(self, phrase: Text):
        """
        $ python -m sagas.ko.ko_helper pos '계획이'
        :param phrase:
        :return:
        """
        return self.mecab.pos(phrase)

    def nouns(self, phrase: Text):
        """
        $ python -m sagas.ko.ko_helper nouns '피자와 스파게티가'
        $ python -m sagas.ko.ko_helper nouns '계획이'
        :param phrase:
        :return:
        """
        from sagas.nlu.transliterations import translits
        from sagas.ko.kwn_procs import kwn
        ns= self.mecab.nouns(phrase)
        rs=[]
        for w in ns:
            # ws = get_word_sets(w, 'ko')
            ws=kwn.get_synsets(w, first=True)
            if ws:
                rs.append({'spec':ws[0].name(),
                           'text':w,
                           'translit': translits.translit(w, 'ko'),
                           'definition': ws[0].definition()})
            else:
                rs.append({'text': w,
                           'translit': translits.translit(w, 'ko'),})
        return rs

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

