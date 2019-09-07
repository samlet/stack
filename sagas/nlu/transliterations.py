def translit(sents, lang):
    from polyglot.transliteration import Transliterator
    from polyglot.text import Text
    text = Text(sents, hint_language_code=lang)
    return ' '.join([x for x in text.transliterate("en")])

class Transliterations(object):
    def __init__(self):
        import kroman
        import cyrtranslit
        import icu

        self.tr_icu = icu.Transliterator.createInstance('Any-Latin; Latin-ASCII').transliterate
        self.tr_title = icu.Transliterator.createInstance('Any-Latin; Title').transliterate
        self.tr_el=icu.Transliterator.createInstance('Greek-Latin')
        self.lang_maps={'iw':'he'}
        self.transliters={('ko'):lambda s,_: kroman.parse(s),
                          ('sr', 'me', 'mk', 'ru'): lambda s,lang:cyrtranslit.to_latin(s, lang),
                          ('he', 'fa'): lambda s,lang:translit(s,lang),
                          ('hi', 'ar'): lambda s,_:self.tr_icu(s),
                          ('el'): lambda s,_:self.tr_el(s),
                          ('zh'): lambda s,_:self.tr_title(s),
                          ('ja'): lambda s,_:self.trans_ja(s),
                          }

    def trans_ja(self, sents):
        from sagas.ja.ja_text_procs import text_procs
        return text_procs.translit(sents)

    def trans_icu(self, sents):
        """
        $ python -m sagas.nlu.transliterations trans_icu '試合はいつですか？'
        $ python -m sagas.nlu.transliterations trans_icu ガ
        :param sents:
        :return:
        """
        return self.tr_icu(sents)

    def available_langs(self):
        return ['iw', 'he', 'ko', 'sr', 'me', 'mk',
                'ru', 'ar', 'fa', 'hi',
                'el', 'zh', 'ja'
                ]

    def translit(self, sents:str, lang:str):
        """
        $ python -m sagas.nlu.transliterations translit '내 친구들은 멍청하다.' ko
        $ python -m sagas.nlu.transliterations translit '試合はいつですか？' ja
        $ python -m sagas.nlu.transliterations translit "医薬品安全管理責任者" ja
        $ python -m sagas.nlu.transliterations translit "医薬品安全管理責任者" zh
        $ python -m sagas.nlu.transliterations translit 'صباح الخير' ar
        $ python -m sagas.nlu.transliterations translit 'शुभ प्रभात' hi
        :param sents:
        :param lang:
        :return:
        """
        if lang in self.lang_maps:
            lang=self.lang_maps[lang]
        for k,v in self.transliters.items():
            if lang in k:
                return v(sents, lang)
        return ''

translits=Transliterations()

if __name__ == '__main__':
    import fire
    fire.Fire(Transliterations)

