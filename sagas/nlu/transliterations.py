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
        self.tr_el=icu.Transliterator.createInstance('Greek-Latin').transliterate
        self.lang_maps={'iw':'he'}
        self.transliters={('ko'):lambda s,_: kroman.parse(s),
                          ('sr', 'me', 'mk', 'ru'): lambda s,lang:cyrtranslit.to_latin(s, lang),
                          ('he', 'fa', 'ur'): lambda s,lang:translit(s,lang),
                          # ('hi', 'ar'): lambda s,_:self.tr_icu(s),
                          ('hi'): lambda s, _: self.tr_icu(s),
                          ('ar'): lambda s,_: self.trans_ar(s),
                          ('el'): lambda s,_:self.tr_el(s),
                          # ('el'): lambda s, _: self.tr_icu(s),
                          ('zh'): lambda s,_:self.tr_title(s),
                          # ('ja'): lambda s,_:self.trans_ja(s),
                          ('ja'): lambda s, _: self.tr_icu(s),
                          }

    def trans_ar(self, sents):
        from sagas.nlu.translit_ar import ar_translit
        return ar_translit.transliterate(sents, vocalize=True, trac_unk=True)

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

    def trans_polyglot(self, sents, lang):
        """
        $ python -m sagas.nlu.transliterations trans_polyglot 'وہ امیر ہے۔' ur
        $ python -m sagas.nlu.transliterations trans_polyglot 'वह धनी है।' hi
        $ python -m sagas.nlu.transliterations trans_polyglot 'الان تنیس بازی میکنم' fa

        :param sents:
        :param lang:
        :return:
        """
        return translit(sents, lang)

    def trans_polyglot_from_clip(self, lang, force_ployglot=False):
        """
        Merge sentence from clipboard and do translit
        $ python -m sagas.nlu.transliterations trans_polyglot_from_clip fa
        $ tra fa
        :param lang:
        :return:
        """
        from sagas.nlu.common import get_from_clip
        text=get_from_clip()
        if force_ployglot:
            print('.. force ployglot')
            return self.trans_polyglot(text, lang)
        else:
            return self.translit(text, lang)

    def available_langs(self):
        return ['iw', 'he', 'ko', 'sr', 'me', 'mk',
                'ru', 'ar', 'fa', 'hi', 'ur',
                'el', 'zh', 'ja'
                ]

    def is_available_lang(self, lang):
        return lang in self.available_langs()

    def translit(self, sents:str, lang:str):
        """
        $ python -m sagas.nlu.transliterations translit '내 친구들은 멍청하다.' ko
        $ python -m sagas.nlu.transliterations translit '試合はいつですか？' ja
        $ python -m sagas.nlu.transliterations translit "医薬品安全管理責任者" ja
        $ python -m sagas.nlu.transliterations translit "医薬品安全管理責任者" zh
        $ python -m sagas.nlu.transliterations translit 'صباح الخير' ar
        $ python -m sagas.nlu.transliterations translit 'शुभ प्रभात' hi
        $ python -m sagas.nlu.transliterations translit 'وہ امیر ہے۔' ur
        $ python -m sagas.nlu.transliterations translit 'Εμείς είμαστε εδώ.' el
        $ python -m sagas.nlu.transliterations translit 'Αυτός είναι εδώ και αυτή είναι εδώ.' el

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

