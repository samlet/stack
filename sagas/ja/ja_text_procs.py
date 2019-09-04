from sudachipy import tokenizer
class JaTextProcs(object):
    def __init__(self):
        import icu
        self.tr = icu.Transliterator.createInstance('Any-Latin; Latin-ASCII').transliterate
        self._tokenizer_obj = None

    @property
    def tokenizer_inst(self):
        from sudachipy import dictionary
        from sudachipy import config
        import json
        if self._tokenizer_obj is None:
            with open(config.SETTINGFILE, "r", encoding="utf-8") as f:
                settings = json.load(f)
                self._tokenizer_obj = dictionary.Dictionary(settings).create()
        return self._tokenizer_obj

    def translit(self, sents):
        """
        $ python -m sagas.ja.ja_text_procs translit "試合はいつですか？"
        :param sents:
        :return:
        """
        sents = sents.translate({ord(i): None for i in '、。！？'})
        mode = tokenizer.Tokenizer.SplitMode.B
        return ' '.join([self.tr(m.reading_form()) for m in self.tokenizer_inst.tokenize(mode, sents)])

text_procs=JaTextProcs()

if __name__ == '__main__':
    import fire
    fire.Fire(JaTextProcs)

