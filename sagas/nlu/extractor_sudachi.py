from natasha.markup import format_markup_css
class Matches(object):
    __attributes__ = ['text', 'matches']

    def __init__(self, text, matches):
        self.text = text
        self.matches = matches

    def __iter__(self):
        return iter(self.matches)

    def __getitem__(self, index):
        return self.matches[index]

    def __len__(self):
        return len(self.matches)

    def __bool__(self):
        return bool(self.matches)

    def _repr_html_(self):
        spans = [(_[0],_[1]) for _ in self.matches]
        return ''.join(format_markup_css(self.text, spans))

class SudachiExtractor(object):
    def __init__(self):
        import json
        from sudachipy import tokenizer, dictionary, config
        with open(config.SETTINGFILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
        self.tokenizer_obj = dictionary.Dictionary(settings).create()
        self.mode = tokenizer.Tokenizer.SplitMode.C

    def print_entities(self, sents):
        for m in self.tokenizer_obj.tokenize(self.mode, sents):
            print("(%d-%d)" % (m.begin(), m.end()),
                  m.dictionary_form(),
                  m.part_of_speech(),
                  m.part_of_speech()[2]
                  )

    def get_entities(self, sents):
        entities = [(m.begin(), m.end(), m.part_of_speech()[2])
                    for m in self.tokenizer_obj.tokenize(self.mode, sents)
                    if m.part_of_speech()[2] != '*']
        matches = sorted(entities, key=lambda _: _[0])
        return matches

    def entities_df(self, sents):
        import sagas
        rs = []
        for m in self.tokenizer_obj.tokenize(self.mode, sents):
            rs.append((m.begin(), m.end(),
                       m.dictionary_form(),
                       m.part_of_speech(),
                       m.part_of_speech()[2]
                       ))
        return sagas.to_df(rs, ['start', 'end', 'word', 'pos', 'entity'])

    def get_segs(self, sents):
        matches = self.get_entities(sents)
        return [ent[2] + '_' + sents[ent[0]:ent[1]] for ent in matches]

    def to_df(self, text):
        """
        $ python -m sagas.nlu.extractor_sudachi to_df 'その博物館はまだ開いていません。'
        :param text:
        :return:
        """
        # text = 'その博物館はまだ開いていません。'
        # print_entities(text)
        print("(%s)" % '; '.join(self.get_segs(text)))
        print(self.entities_df(text))

if __name__ == '__main__':
    import fire
    fire.Fire(SudachiExtractor)
