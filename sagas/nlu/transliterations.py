def translit(sents, lang):
    from polyglot.transliteration import Transliterator
    from polyglot.text import Text
    text = Text(sents, hint_language_code=lang)
    return ' '.join([x for x in text.transliterate("en")])

class Transliterations(object):
    def __init__(self):
        import kroman
        import cyrtranslit

        self.lang_maps={'iw':'he'}
        self.transliters={('ko'):lambda s,_: kroman.parse(s),
                          ('sr', 'me', 'mk', 'ru'): lambda s,lang:cyrtranslit.to_latin(s, lang),
                          ('he', 'ar', 'fa', 'hi'): lambda s,lang:translit(s,lang),
                          }

    def translit(self, sents, lang):
        """
        $ python -m sagas.nlu.transliterations translit '내 친구들은 멍청하다.' ko
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

if __name__ == '__main__':
    import fire
    fire.Fire(Transliterations)

